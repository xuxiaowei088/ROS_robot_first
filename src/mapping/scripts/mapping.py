#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose, Point, Quaternion
from tf.transformations import quaternion_from_euler
from gmapping import GMapping

class Mapping:
    def __init__(self):
        rospy.init_node('mapping')
        self.gmapper = GMapping()
        self.gmapper.laser_callback = self.laser_callback
        self.gmapper.odom_callback = self.odom_callback
        self.laser_data = None
        self.odom_data = None
        self.pose = Pose()
        self.pose.position = Point(0.0, 0.0, 0.0)
        self.pose.orientation = Quaternion(0.0, 0.0, 0.0, 1.0)
        self.pub = rospy.Publisher('/map', OccupancyGrid, queue_size=10)
        self.gmapper.start()

    def laser_callback(self, data):
        self.laser_data = data

    def odom_callback(self, data):
        self.odom_data = data

    def update_pose(self):
        if self.odom_data is not None:
            self.pose.position.x = self.odom_data.pose.pose.position.x
            self.pose.position.y = self.odom_data.pose.pose.position.y
            self.pose.position.z = self.odom_data.pose.pose.position.z
            self.pose.orientation = self.odom_data.pose.pose.orientation

    def publish_map(self):
        if self.laser_data is not None:
            self.update_pose()
            self.gmapper.update(self.laser_data, self.pose)
            self.pub.publish(self.gmapper.map_msg)

if __name__ == '__main__':
    try:
        mp = Mapping()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
