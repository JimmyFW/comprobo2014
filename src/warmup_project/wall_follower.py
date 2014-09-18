#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
from sensor_msgs.msg import LaserScan

distance_to_wall = -1.0

def scan_received(msg):
    """ Callback function for msg of type sensor_msgs/LaserScan """
    global distance_to_wall
    valid_measurements = []
    for i in range(5):
        if msg.ranges[i] != 0 and msg.ranges[i] < 7:
            valid_measurements.append(msg.ranges[i])
    if len(valid_measurements):
        distance_to_wall = sum(valid_measurements)/float(len(valid_measurements))
    else:
        distance_to_wall = -1.0
    print distance_to_wall

def wall():
    """ Run loop for the wall node """
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    sub = rospy.Subscriber('/scan', LaserScan, scan_received)
    rospy.init_node('wall', anonymous=True)
    r = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        if distance_to_wall == -1:
            msg = Twist()
        else:
            msg = Twist(linear=Vector3(x=(distance_to_wall-1)*.02))
        pub.publish(msg)
        r.sleep()
        
if __name__ == '__main__':
    try:
        wall()
    except rospy.ROSInterruptException: pass
