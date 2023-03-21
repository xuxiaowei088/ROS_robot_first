#!/usr/bin/env python

import rospy
from can_msgs.msg import Frame

class LowerControl:
    def __init__(self):
        rospy.init_node('lower_control')
        self.pub = rospy.Publisher('/can_bus', Frame, queue_size=10)
        rospy.Subscriber('/cmd_vel', Twist, self.callback)

    def callback(self, data):
        frame = Frame()
        frame.id = 0x01  # 设置帧ID
        frame.dlc = 8  # 数据长度为8字节
        frame.data[0] = int(data.linear.x * 100)  # 线速度乘以100，转换为整数型
        frame.data[1] = int(data.angular.z * 100)  # 角速度乘以100，转换为整数型
        # 其他数据字节根据需要设置
        self.pub.publish(frame)

if __name__ == '__main__':
    try:
        lc = LowerControl()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
