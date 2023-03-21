#!/usr/bin/env python

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Pose, Point, Quaternion

class Navigation:
    def __init__(self):
        rospy.init_node('navigation')
        self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        self.client.wait_for_server()

    def navigate_to(self, x, y, theta):
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position = Point(x, y, 0.0)
        q = Quaternion()
        q.set_from_euler(0.0, 0.0, theta)
        goal.target_pose.pose.orientation = q

        self.client.send_goal(goal)
        self.client.wait_for_result()

if __name__ == '__main__':
    try:
        nav = Navigation()
        # Navigate to a point (x, y, theta)
        nav.navigate_to(2.0, 2.0, 0.0)
    except rospy.ROSInterruptException:
        pass
