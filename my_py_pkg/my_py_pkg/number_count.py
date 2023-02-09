#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from example_interfaces.msg import Int64
 
 
class NumberCounterNode(Node): 
    def __init__(self):
        self.counter_ = 0
        super().__init__("number_counter") 
        self.number_counter_publisher_ = self.create_publisher(Int64, "number_count",10)
        self.number_counter_ = self.create_subscription(Int64,"number",self.callback_number,10)
        
    
    def callback_number(self,msg):
        self.counter_ += msg.data
        self.new_msg = Int64()
        self.new_msg.data = self.counter_
        self.get_logger().info(str(self.counter_)) 
        self.number_counter_publisher_.publish(self.new_msg)



 
def main(args=None):
    rclpy.init(args=args)
    node = NumberCounterNode() 
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()