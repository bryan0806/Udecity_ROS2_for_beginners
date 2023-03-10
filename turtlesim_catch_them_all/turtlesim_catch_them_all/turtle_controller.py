#!/usr/bin/env python3
import rclpy
import math
from rclpy.node import Node

from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from my_robot_interfaces.msg import Turtle
from my_robot_interfaces.msg import TurtleArray
from my_robot_interfaces.srv import CatchTurtle
from functools import partial
 
class TurtleControllerNode(Node): 
    def __init__(self):
        super().__init__("turtle_controller") 
        #self.target_x_ = 8.0 #temp used for target position
        #self.target_y_ = 4.0 #temp used for target position
        self.turtle_to_catch = None
        self.pose_ = None
        self.pose_subcriber_ = self.create_subscription(
            Pose,"turtle1/pose",self.callback_turtle_pose,10)
        self.cmd_vel_publisher_ = self.create_publisher(
            Twist,"/turtle1/cmd_vel",10)
        self.alive_turtles_subcriber_ = self.create_subscription(
            TurtleArray, "alive_turtles", self.callback_alive_turtles,10)
        self.control_loop_timer_ = self.create_timer(0.01,self.control_loop)


    def callback_turtle_pose(self,msg):
        self.pose_ = msg

    def callback_alive_turtles(self,msg):
        self.get_logger().info("length of msg.turtles = " + str(len(msg.turtles)))
        if(len(msg.turtles)>0):
            self.turtle_to_catch = msg.turtles[0]

    def control_loop(self):
        if(self.pose_==None or self.turtle_to_catch==None):
            return
        
        dist_x = self.turtle_to_catch.x - self.pose_.x
        dist_y = self.turtle_to_catch.y - self.pose_.y

        distance = math.sqrt(dist_x*dist_x + dist_y*dist_y)

        msg = Twist()

        if(distance > 0.5):
            #position
            msg.linear.x = 2*distance #teahcer's experience after tuning 

            #orientation
            goal_theta = math.atan2(dist_y,dist_x)
            diff = goal_theta - self.pose_.theta

            #normalization
            if (diff > math.pi):
                diff -= 2*math.pi
            elif (diff < -math.pi):
                diff += 2*math.pi

            msg.angular.z = 6*diff #teahcer's experience after tuning

        else:
            #reach catch turtle
            self.get_logger().info("reach catch turtle....turtle to kill: "+ self.turtle_to_catch.name)
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.call_catch_turtle_server(self.turtle_to_catch.name)
            self.turtle_to_catch = None


        self.cmd_vel_publisher_.publish(msg)


    def call_catch_turtle_server(self, turtle_name):
        client = self.create_client(CatchTurtle, "catch_turtle")
        while not client.wait_for_service(1.0):
            self.get_logger().warn("waiting for service serve ..")

        request = CatchTurtle.Request()
        request.name = turtle_name


        future = client.call_async(request)
        future.add_done_callback(partial(self.callback_call_catch_turtle,turtle_name = turtle_name))

    def callback_call_catch_turtle(self,future, turtle_name):
        try:
            response = future.result()
            if not response.success:
                self.get_logger().info("Turtle " + str(turtle_name) + " count not be caught.")

        except Exception as e:
            self.get_logger().error("serice call failed %r" % (e,))
 
def main(args=None):
    rclpy.init(args=args)
    node = TurtleControllerNode() 
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()