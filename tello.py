import socket
import threading
import time
from stats import Stats
import sweep
from cv2 import cv2


class Tello:
    def __init__(self):
        self.local_ip = ''
        self.local_port = 8889
        self.socket = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM)  # socket for sending cmd
        self.socket.bind((self.local_ip, self.local_port))

        # thread for receiving cmd ack
        self.receive_thread = threading.Thread(target=self._receive_thread)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        self.tello_ip = '192.168.10.1'
        self.tello_port = 8889
        self.tello_adderss = (self.tello_ip, self.tello_port)
        self.log = []

        self.isInterruptd = False
        self.stateIndex = 0
        self.stream_state = False
        self.last_frame = None
        self.MAX_TIME_OUT = 0.1  # fail fast since there's no drone
        self.send_command('command', 0)

    def _video_thread(self):
        # from https://github.com/Virodroid/easyTello/blob/master/easytello/tello.py
        # Creating stream capture object
        # cap = cv2.VideoCapture('udp://'+self.tello_ip+':11111')
        # Runs while 'stream_state' is True
        cap = cv2.VideoCapture(0)
        while self.stream_state:
            ret, self.last_frame = cap.read()
            cv2.imshow('DJI Tello', self.last_frame)

            # Video Stream is closed if escape key is pressed
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                break
        cap.release()
        cv2.destroyAllWindows()

    def streamon(self):
        self.send_command('streamon')
        self.stream_state = True
        self.video_thread = threading.Thread(target=self._video_thread)
        self.video_thread.daemon = True
        self.video_thread.start()

    def streamoff(self):
        self.stream_state = False
        self.send_command('streamoff')

    def printStats(self):
        self.get_speed()
        self.get_battery()
        self.get_time()
        self.get_height()
        self.get_temp()
        self.get_attitude()
        # get_baro
        # get_acceleration
        # get_tof
        # get_wifi

    # def streamVID(self):
    #     print("Started Streaming video from drone ....")
    #     self.send_command('streamon', 0)
    #     self.isStreamingVideo = True

    def Interrupt(self):
        self.isInterruptd = True

    def unlockInterrupt(self):
        self.isInterruptd = False

    def saveStateIndex(self, index):
        self.stateIndex = index

    def get_isInterruptd(self):
        return self.isInterruptd

    def sweep(self):
        print("Going autonomus ...")
        sweep.execute(self)

    def start_manual_control(self):
        self.Interrupt()
        # interrupt the sweep, this should be called on a switch
        print("start manual control")

    def continue_sweep(self):
        # continue the sweep
        self.unlockInterrupt()
        sweep.execute(self, self.stateIndex)
        print("continue autonomus mode ...")

    def send_command(self, command, d: int = 1):
        self.log.append(Stats(command, len(self.log)))

        self.socket.sendto(command.encode('utf-8'), self.tello_adderss)
        print('sending command: %s to drone' % command)

        start = time.time()
        while not self.log[-1].got_response():
            now = time.time()
            diff = now - start
            if diff > self.MAX_TIME_OUT:
                # print("Timedout with no response")
                time.sleep(d)
                return
        print('Done!!! sent command: %s to %s' % (command, self.tello_ip))

    def _receive_thread(self):
        """Listen to responses from the Tello.

        Runs as a thread, sets self.response to whatever the Tello last returned.

        """
        while True:
            try:
                self.response, ip = self.socket.recvfrom(1024)
                print('from %s: %s' % (ip, self.response))

                self.log[-1].add_response(self.response)
            except socket.error as exc:
                print("Caught exception socket.error : %s" % (exc))

    def on_close(self):
        pass
        # for ip in self.tello_ip_list:
        #     self.socket.sendto('land'.encode('utf-8'), (ip, 8889))
        # self.socket.close()

    def get_log(self):
        return self.log

    # Read Commands
    # Dear Dr Nazean, I copied some code from this file
    # https://github.com/Virodroid/easyTello/blob/master/easytello/tello.py
    def get_speed(self):
        self.send_command('speed?', True)
        return self.log[-1].get_response()

    def get_battery(self):
        self.send_command('battery?', True)
        return self.log[-1].get_response()

    def get_time(self):
        self.send_command('time?', True)
        return self.log[-1].get_response()

    def get_height(self):
        self.send_command('height?', True)
        return self.log[-1].get_response()

    def get_temp(self):
        self.send_command('temp?', True)
        return self.log[-1].get_response()

    def get_attitude(self):
        self.send_command('attitude?', True)
        return self.log[-1].get_response()

    def get_baro(self):
        self.send_command('baro?', True)
        return self.log[-1].get_response()

    def get_acceleration(self):
        self.send_command('acceleration?', True)
        return self.log[-1].get_response()

    def get_tof(self):
        self.send_command('tof?', True)
        return self.log[-1].get_response()

    def get_wifi(self):
        self.send_command('wifi?', True)
        return self.log[-1].get_response()
