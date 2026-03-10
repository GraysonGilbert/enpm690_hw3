#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import sys
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Range
import time

class AutonomyNode(Node):
    def __init__(self):  
        # Initiate with name of your node
        super().__init__("autonomous_nav_node")
        
        # Establish Obstacle Avoidance Parameter
        self.declare_parameter('threshold', 0.1)
        self.distance_threshold = self.get_parameter('threshold').get_parameter_value().double_value
        
        # Create Publishers and Subscribers
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.create_subscription(Range, '/left_sensor', self.left_sensor_callback, 10)
        self.create_subscription(Range, '/right_sensor', self.right_sensor_callback, 10)
        
        # Vehicle Movement Parameters
        self.forward_speed = 0.15
        self.turn_speed = 0.75
        
        # Initialize Sensor Ranges
        self.left_sensor_range = None
        self.right_sensor_range = None
        
        # Robot States
        self.need_extended_turn = False
        self.turn_start_time = None
        self.extended_turn_duration = 2.0 # in seconds
        
        # Initialize counter for time
        self.timer =self.create_timer(0.1, self.autonomy_loop)
        self.get_logger().info(f"[Starting Autonomous Navigation] Distance threshold: {self.distance_threshold}")
        
    # Callback to collect left sensor readings
    def left_sensor_callback(self, msg):
        self.left_sensor_range = msg.range
    
    # Callback to collect right sensor readings
    def right_sensor_callback(self, msg):
        self.right_sensor_range = msg.range
               
    # Autonomous control loop           
    def autonomy_loop(self):
        
        # Checks sensor readings are available
        if self.left_sensor_range is None or self.right_sensor_range is None:
            return
        
        msg = Twist()
        now = self.get_clock().now()
        
        # Checks if robot needs to complete an extended turn (i.e. stuck in corner or hitting obstacle straight on)
        if self.need_extended_turn:
            elapsed = (now - self.turn_start_time).nanoseconds / 1e9
            if elapsed < self.extended_turn_duration:
                msg.angular.z = self.turn_speed
                msg.linear.x = 0.0
                self.cmd_vel_pub.publish(msg)
                return
            else:
                self.need_extended_turn = False
                self.get_logger().info("Extended Turn Complete.")
         
        # Obstacle Avoidance Logic
        left_sensor_blocked = self.left_sensor_range < self.distance_threshold
        right_sensor_blocked = self.right_sensor_range < self.distance_threshold
        
        # Beging extended turn when both sensors read below threshold
        if left_sensor_blocked and right_sensor_blocked:
            self.get_logger().info("Both sensors blocked, starting extended turn.")
            self.need_extended_turn = True
            self.turn_start_time = now
            return
        
        # Single sensor reading below threshold logic 
        if left_sensor_blocked:
            msg.linear.x = 0.0
            msg.angular.z = -self.turn_speed
        elif right_sensor_blocked:
            msg.linear.x = 0.0
            msg. angular.z = self.turn_speed
        # If both sensors do not register obstacle, move forward
        else:
            msg.linear.x = self.forward_speed
        

        if rclpy.ok():
            self.cmd_vel_pub.publish(msg)
        
        # Log sensor readings and robot velocities to terminal
        self.get_logger().info(f'Left Range: {self.left_sensor_range} Right Range: {self.right_sensor_range} Linear Veloicty: {msg.linear.x} Angular Velocity: {msg.angular.z}')
        


def main(args=None):
    print('Running Autonomous Navigation')
    rclpy.init(args=args)

    node = AutonomyNode()

    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()