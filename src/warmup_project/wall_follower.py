#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
from sensor_msgs.msg import LaserScan

front_distance = -1.0
distance_to_wall = -1.0
state = 0 #begin

def scan_received(msg):
    """ Callback function for msg of type sensor_msgs/LaserScan """
    global front_distance
    global state
    valid_measurements = []
    for i in range(5):
        if msg.ranges[i] != 0 and msg.ranges[i] < 7:
            valid_measurements.append(msg.ranges[i])
    if len(valid_measurements):
        front_distance = sum(valid_measurements)/float(len(valid_measurements))
    else:
        front_distance = -1.0
    print msg.header.stamp.secs
    print front_distance
    if abs((front_distance - 1.0)) < .05:
        state = 1
    else:
        state = 0

def wall():
    """ Run loop for the wall node """
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    sub = rospy.Subscriber('/scan', LaserScan, scan_received)
    rospy.init_node('wall', anonymous=True)
    r = rospy.Rate(10) # 10hz
    
    while not rospy.is_shutdown():
        if state == 0:
            print "FIND THE WALL"
            if front_distance == -1:
                msg = Twist()
            else:
                msg = Twist(linear=Vector3(x=(front_distance-1)*.2))
                print msg
            pub.publish(msg)
            r.sleep()
        elif state == 1:
            print "spin around"
            if front_distance == -1:
                msg = Twist()
            else:
                msg = Twist(linear=Vector3(x=0),angular=Vector3(z=.2))
                print msg
            pub.publish(msg)
            r.sleep()


if __name__ == '__main__':
    try:
        wall()
    except rospy.ROSInterruptException: pass
