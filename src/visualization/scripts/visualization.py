#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point

class Visualization:
    def __init__(self):
        rospy.init_node('visualization')
        self.pub = rospy.Publisher('/visualization', Marker, queue_size=10)
        rospy.Subscriber('/laser', LaserScan, self.callback)

    def callback(self, data):
        marker = Marker()
        marker.header.frame_id = "laser_frame"
        marker.type = Marker.POINTS
        marker.action = Marker.ADD
        marker.scale.x = 0.1
        marker.scale.y = 0.1
        marker.color.a = 1.0
        marker.color.r = 1.0
        marker.color.g = 0.0
        marker.color.b = 0.0

        for i, r in enumerate(data.ranges):
            if r < data.range_max:
                p = Point()
                p.x = r * math.cos(data.angle_min + i * data.angle_increment)
                p.y = r * math.sin(data.angle_min + i * data.angle_increment)
                marker.points.append(p)

        self.pub.publish(marker)

if __name__ == '__main__':
    try:
        vis = Visualization()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
