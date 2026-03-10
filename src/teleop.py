#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys, select, termios, tty

class TeleOpNode(Node):
    def __init__(self):
        # Initialize the node with a name
        super().__init__('TeleopNode')
        
        # Create a publisher on the /cmd_vel topic
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.settings = termios.tcgetattr(sys.stdin)
        
        # Create a timer that calls the callback every 0.1 seconds (10Hz)
        self.timer_period = 0.1  
        self.timer = self.create_timer(self.timer_period, self.teleop_callback)
        
        self.get_logger().info('TeleOp Node has started!')
        
        # List of acceptable key presses
        self.accepted_keys = ['w', 's', 'd', 'a', ' ']

    def teleop_callback(self):
        msg = Twist()
        key = self.get_key_input()
        
        if key == "\x03":
            raise KeyboardInterrupt
        if key in self.accepted_keys:
            
            if key == "w":
                msg.linear.x = 0.5
                msg.angular.z = 0.0 
            elif key == "s":
                msg.linear.x = -0.5
                msg.angular.z = 0.0
            elif key == "a":
                msg.linear.x = 0.0
                msg.angular.z = 0.5 
            elif key == "d":
                msg.linear.x = 0.0
                msg.angular.z = -0.5 
            else:
                msg.linear.x = 0.0
                msg.angular.z = 0.0
            
            self.get_logger().info(f'Key Pressed: {key} Linear={msg.linear.x}, Angular={msg.angular.z}') # Log valid key press 
        else:
            self.get_logger().info(f'Key not accepted! Press one of the following keys: [a,s,w,d, or space bar]') # Log invalid key press
            
        # Publish the message
        if rclpy.ok():
            self.publisher_.publish(msg)
            
    # Read in key presses
    def get_key_input(self):
        
        tty.setraw(sys.stdin.fileno())
        select.select([sys.stdin], [], [], 0)
        key = sys. stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)   
        
        return key     
        

def main(args=None):
    rclpy.init(args=args)
    node = TeleOpNode()
    
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt):
        pass
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, node.settings)
        node.get_logger().info('Shutting down...') # Handle node shutdown gracefully
        if rclpy.ok():
            node.destroy_node()
            rclpy.shutdown()

if __name__ == '__main__':
    main()