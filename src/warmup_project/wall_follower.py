#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
from sensor_msgs.msg import LaserScan
#from PIDController import PIDController

target_distance = .5
front_distance = -1.0
right_distance = -1.0
left_distance = -1.0
state = 4 #begin

def avg_scans(ranges, start, stop):
    valid_measurements = []
    for i in range(start, stop):
        if ranges[i] != 0 and ranges[i] < 7:
            valid_measurements.append(ranges[i])
    if len(valid_measurements):
        return sum(valid_measurements)/float(len(valid_measurements))
    else:
        return -1.0

def scan_received(msg):
    """ Callback function for msg of type sensor_msgs/LaserScan """
    global front_distance
    global right_distance
    global left_distance
    global state
    front_distance = avg_scans(msg.ranges, 0, 5)
    right_distance = avg_scans(msg.ranges, 270, 275)
    left_distance = avg_scans(msg.ranges, 85, 90)
    north_left_leg = avg_scans(msg.ranges, 40, 45)
    north_right_leg = avg_scans(msg.ranges, 330, 335)
    east_left_leg = avg_scans(msg.ranges, 295, 300)
    east_right_leg = avg_scans(msg.ranges, 240, 245)
    #print msg.header.stamp.secs
    #print front_distance
    if state == 4 and front_distance != -1.0:
        if left_distance < front_distance or right_distance < front_distance:
            state = 5
        else:
            state = 0
    if state == 0 or state == 1:
        if front_distance - target_distance > .2:
            state = 0 # linear approach
        elif abs(front_distance - target_distance) >= .05:
            state = 1 # proportional control
        elif abs(front_distance - target_distance) < .05:
            state = 2 # turn
    elif state == 2:
        print "!!!EAST LEGS!!!"
        print east_left_leg
        print east_right_leg
        if abs(east_left_leg - east_right_leg) < .05 and right_distance != -1.0 and abs(right_distance - target_distance) < .1:
            state = 3
        else:
            print east_right_leg
            print east_left_leg
    elif state == 5:
        print "!!!NORTH LEGS!!!"
        print north_left_leg
        print north_right_leg
        if abs(north_left_leg - north_right_leg) < .05:
            state = 1

def wall():
    """ Run loop for the wall node """
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    sub = rospy.Subscriber('/scan', LaserScan, scan_received)
    rospy.init_node('wall', anonymous=True)
    r = rospy.Rate(10) # 10hz
    
    while not rospy.is_shutdown():
        if state == 0: # move forward to wall
            print "STATE 0 (move to a wall)"
            print "FRONT DISTANCE " + str(front_distance)
            print "RIGHT DISTANCE " + str(right_distance)
            msg = Twist(linear=Vector3(x=.15))
            pub.publish(msg)
            r.sleep()
        elif state == 1:
            print "STATE 1 (settle at target_distance)"
            print "FRONT DISTANCE " + str(front_distance)
            print "RIGHT DISTANCE " + str(right_distance)
            if front_distance == -1:
                msg = Twist()
            else:
                cart_vector = Vector3(x=(front_distance-target_distance)*.2)
                msg = Twist(linear=cart_vector)
                #print msg
            pub.publish(msg)
            r.sleep()
        elif state == 2:
            print "STATE 2 (spin until parallel to wall)"
            print "FRONT DISTANCE " + str(front_distance)
            print "RIGHT DISTANCE " + str(right_distance)
            msg = Twist(angular=Vector3(z=.4))
            #print msg
            pub.publish(msg)
            r.sleep()
        elif state == 3:
            print "STATE 3 (move along wall)"
            print "FRONT DISTANCE " + str(front_distance)
            print "RIGHT DISTANCE " + str(right_distance)
            msg = Twist(linear=Vector3(x=.1))
            pub.publish(msg)
            r.sleep()
        elif state == 4: # initial spin to make the ros face a wall
            print "STATE 4 (point to a wall)"
            print "FRONT DISTANCE " + str(front_distance)
            print "RIGHT DISTANCE " + str(right_distance)
            msg = Twist(angular=Vector3(z=.2))
            #print msg
            pub.publish(msg)
            r.sleep()
        elif state == 5:
            print "STATE 5 (spin until perpendicular to wall)"
            print "FRONT DISTANCE " + str(front_distance)
            print "RIGHT DISTANCE " + str(right_distance)
            msg = Twist(angular=Vector3(z=.2))
            #print msg
            pub.publish(msg)
            r.sleep()

if __name__ == '__main__':
    try:
        wall()
    except rospy.ROSInterruptException: pass
