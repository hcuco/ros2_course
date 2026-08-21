#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn, Kill
from turtlesim.msg import Pose
import random
from functools import partial
import math
from example_interfaces.msg import String
from tsk_interfaces.msg import Turtle

class TurtleSpawnerNode(Node):
    def __init__(self):
        super().__init__("turtle_spawner")
        self.turtles_alive = []

        self.declare_parameter("spawn_period",value=1.0)
        self.spawn_period_ = self.get_parameter("spawn_period").value

        self.create_subscription(String,"target_reached",self.callback_target_reached,10)

        self.publisher_spawn_ = self.create_publisher(Turtle, "/spawn_register",10)
        self.publisher_kill_ = self.create_publisher(String, "/kill_register",10)

        self.client_spawn_ = self.create_client(Spawn,"/spawn")
        self.client_kill_ = self.create_client(Kill,"/kill")

        self.timer_spawn_ = self.create_timer(self.spawn_period_,self.callback_timer_spawn_turtle)

        self.get_logger().info("Turtle Spawner node has been started.")

    def callback_timer_spawn_turtle(self):
        while not self.client_spawn_.wait_for_service(1.0):
            self.get_logger().warn("Waiting for spawn turtle server...")

        request = Spawn.Request()
        request.x = random.uniform(0.5,10.5)
        request.y = random.uniform(0.5,10.5)
        request.theta = random.uniform(0,2*math.pi)

        future = self.client_spawn_.call_async(request)
        future.add_done_callback(
            partial(self.callback_finished_spawn_turtle,request=request))
        pass

    def callback_finished_spawn_turtle(self,future,request):
        msg = Turtle()
        msg.turtle_name = future.result().name
        msg.x = request.x
        msg.y = request.y
        msg.theta = request.theta 
        self.publisher_spawn_.publish(msg)


    def callback_target_reached(self, msg: String):
        request = Kill.Request()

        request.name = msg.data

        future = self.client_kill_.call_async(request)
        future.add_done_callback(
            partial(self.callback_finished_kill_turtle,request=request))

    def callback_finished_kill_turtle(self, future, request):
        msg = String()
        msg.data = request.name
        self.publisher_kill_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = TurtleSpawnerNode()
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()