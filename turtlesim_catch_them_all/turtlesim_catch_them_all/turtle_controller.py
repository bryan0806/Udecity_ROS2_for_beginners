#!/usr/bin/env python3
import rclpy
import math
from rclpy.node import Node

from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
 
 
class TurtleControllerNode(Node): 
    def __init__(self):
        super().__init__("turtle_controller") 
        self.target_x_ = 8.0 #temp used for target position
        self.target_y_ = 4.0 #temp used for target position
        self.pose_ = None
        self.pose_subcriber_ = self.create_subscription(
            Pose,"turtle1/pose",self.callback_turtle_pose,10)
        self.cmd_vel_publisher_ = self.create_publisher(Twist,"/turtle1/cmd_vel",10)
        self.control_loop_timer_ = self.create_timer(0.01,self.control_loop)


    def callback_turtle_pose(self,msg):
        self.pose_ = msg

    def control_loop(self):
        if(self.pose_==None):
            return
        
        dist_x = self.target_x_ - self.pose_.x
        dist_y = self.target_y_ - self.pose_.y

        distance = math.sqrt(dist_x*dist_x + dist_y*dist_y)

        msg = Twist()

        if(distance > 0.5):
            #position
            msg.linear.x = distance

            #orientation
            goal_theta = math.atan2(dist_y,dist_x)
            diff = goal_theta - self.pose_.theta

            #normalization
            if (diff > math.pi):
                diff -= 2*math.pi
            elif (diff < -math.pi):
                diff += 2*math.pi

            msg.angular.z = diff

        else:
            msg.linear.x = 0.0
            msg.angular.z = 0.0

        self.cmd_vel_publisher_.publish(msg)
 
def main(args=None):
    rclpy.init(args=args)
    node = TurtleControllerNode() 
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()