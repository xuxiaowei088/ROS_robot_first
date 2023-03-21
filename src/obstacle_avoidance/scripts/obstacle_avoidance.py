#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class ObstacleAvoidance:
    def __init__(self):
        rospy.init_node('obstacle_avoidance')
        self.sub = rospy.Subscriber('/scan', LaserScan, self.scan_callback)
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.twist = Twist()

    def scan_callback(self, msg):
        # Get the distance to the closest obstacle
        closest_distance = min(msg.ranges)
        if closest_distance < 0.5: # if the obstacle is too close
            # Turn to avoid the obstacle
            self.twist.linear.x = 0.0
            self.twist.angular.z = 0.5
        else:
            # Move forward
            self.twist.linear.x = 0.5
            self.twist.angular.z = 0.0

        # Publish the twist message
        self.pub.publish(self.twist)

if __name__ == '__main__':
    try:
        oa = ObstacleAvoidance()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
