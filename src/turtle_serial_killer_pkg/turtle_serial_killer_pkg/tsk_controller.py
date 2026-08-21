#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from example_interfaces.msg import String
from tsk_interfaces.msg import Turtle
import math

class Tartaruga:
    def __init__(self, name, x, y, theta):
        self.turtle_name = name
        self.x = x
        self.y = y
        self.theta = theta

class TskControllerNode(Node):
    def __init__(self):
        super().__init__("tsk_controller")
        self.declare_parameter("kp",value=3.0)
        self.declare_parameter("ki",value=10.0)
        self.kp_ = self.get_parameter("kp").value
        self.ki_ = self.get_parameter("ki").value

        self.waiting_kill_ = False
        self.last_obj_ = []
        self.linx_error_accum_ = 0
        self.angz_error_accum_ = 0

        self.turtles_alive_ = []

        self.create_subscription(Turtle,
             "/spawn_register", self.callback_spawn_register,10)
        self.create_subscription(String, 
            "/kill_register", self.callback_kill_register,10)
        self.create_subscription(Pose, 
            "/turtle1/pose", self.callback_turtle1_pose,10)

        self.publisher_cmd_ = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)

        self.publisher_target_reached_ = self.create_publisher(String, "/target_reached",10)

        self.get_logger().info("Turtle Serial Killer controller node has been started.")

    def callback_spawn_register(self, msg: Turtle):
        t = Tartaruga(msg.turtle_name,msg.x,msg.y,msg.theta)
        self.turtles_alive_.append(t)

    def callback_kill_register(self, msg: String):
        for t in self.turtles_alive_:
            if t.turtle_name == msg.data:
                self.turtles_alive_.remove(t)
                self.waiting_kill_ = False
                break  # Interrompe o loop assim que encontrar e remover

    def callback_turtle1_pose(self,msgr: Pose):
        msg_new = Twist()

        pos = [msgr.x, msgr.y]

        dist_obj = 999
        for t in self.turtles_alive_:
            dist = math.dist([t.x,t.y],pos)
            if  dist < dist_obj:
                dist_obj = dist
                obj = [t.x,t.y]
                t_name = t.turtle_name

        if dist_obj == 999:
            obj = pos

        linx_error = math.dist(obj,pos)

        angz_error = math.atan2(obj[1]-pos[1],obj[0]-pos[0]) - msgr.theta
        angz_error = math.atan2(math.sin(angz_error), math.cos(angz_error))

        if linx_error < 0.1:
            msg_new.linear.x = 0.0
            msg_new.angular.z = 0.0
            if dist_obj != 999 and not self.waiting_kill_:
                msg = String()
                msg.data = t_name
                self.publisher_target_reached_.publish(msg)
                self.waiting_kill_ = True
        else:
            msg_new.linear.x = self.kp_*linx_error 
            + self.ki_*self.linx_error_accum_

            msg_new.angular.z = 5*self.kp_*angz_error 
            + self.ki_*self.angz_error_accum_

        if self.last_obj_ == obj:
            self.linx_error_accum_ += linx_error*0.016 
            self.angz_error_accum_ += angz_error*0.016
            # 0.016 obtained from a ros2 topic hz /turtle1/cmd_vel test
        else:
            self.linx_error_accum_ = linx_error*0.016 
            self.angz_error_accum_ = angz_error*0.016

        self.last_obj_ = obj
        
        self.publisher_cmd_.publish(msg_new)
        pass

 
def main(args=None):
    rclpy.init(args=args)
    node = TskControllerNode()
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()