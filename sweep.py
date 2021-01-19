# from tello import Tello
import time

# billy is the tello object


def run(billy, event):
    # if event has checkpoint, print the message
    if "msg" in event:
        print(event["msg"] + "\n")
    else:
        # billy.send_command(command=event["cmd"], d=event["delay"])
        billy.send_command(command=event["cmd"], d=1)
        if "checkpoint" in event:
            print("%s checkpoint is reached!\n" % event["checkpoint"])


def execute(billy, index: int = 0):
    route = [
        {
            "cmd": "command",
            "delay": 0
        },
        {
            "cmd": "takeoff",
            "delay": 7
        },
        {
            "msg": "From the charging base to the starting checkpoint of sweep pattern."
        },
        {
            "cmd": "forward 50",
            "delay": 4
        },
        {
            "cmd": "ccw 150",
            "delay": 4
        },
        {
            "msg": "Current location: Checkpoint 0"
        },
        # one sweep starts
        {

            "cmd": "cw 90",
            "delay": 4
        },
        {
            "checkpoint": 1,
            "cmd": "forward 100",
            "delay": 4
        },
        {

            "cmd": "ccw 90",
            "delay": 4
        },
        {
            "checkpoint": 2,
            "cmd": "forward 80",
            "delay": 4
        },
        {

            "cmd": "ccw 90",
            "delay": 4
        },
        {
            "checkpoint": 3,
            "cmd": "forward 40",
            "delay": 4
        },
        {

            "cmd": "ccw 90",
            "delay": 4
        },
        {
            "checkpoint": 4,
            "cmd": "forward 40",
            "delay": 4
        },
        {

            "cmd": "cw 90",
            "delay": 4
        },
        {
            "checkpoint": 5,
            "cmd": "forward 60",
            "delay": 4
        },
        {
            "checkpoint": 0,
            "cmd": "ccw 90",
            "delay": 4
        },
        {
            "cmd": "forward 40",
            "delay": 4
        },
        # one sweep complete
        {
            "msg": "Complete sweep. Return to charging base."
        },
        {
            "cmd": "ccw 150",
            "delay": 4
        },
        {
            "cmd": "forward 50",
            "delay": 4
        },
        {
            "msg": "Turn to original direction before land."
        },
        {
            "cmd": "cw 180",
            "delay": 4
        },
        {
            "cmd": "land",
            "delay": 4
        }
    ]

    for i in range(index, len(route)):
        # print("index is %d" % i)
        if not billy.get_isInterruptd():
            run(billy, route[i])
        else:
            billy.saveStateIndex(i)
            break
