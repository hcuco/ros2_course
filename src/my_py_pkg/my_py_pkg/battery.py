#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.srv import SetLedState
from functools import partial
 
 
class BatteryNode(Node):
    def __init__(self):
        super().__init__("battery")
        self.bateria = 100.0
        self.client_ = self.create_client(SetLedState, "set_led")
        self.ts = 1
        self.timer_ = self.create_timer(self.ts, self.atualiza_bateria)
        self.carregando = False

    def call_set_led(self,ln,state):
        while not self.client_.wait_for_service(1.0):
            self.get_logger().warn("Waiting for Set Led server...")

        request = SetLedState.Request()
        request.led_number = ln
        request.state = state

        future = self.client_.call_async(request)
        future.add_done_callback(
            partial(self.callback_call_set_led,request=request))

    def atualiza_bateria(self):
        if self.carregando:
            self.bateria += 100*self.ts/6
            if self.bateria >= 100.0:
                self.bateria = 100.0
                self.carregando = False
                self.call_set_led(3,False)

        else:
            self.bateria -= 100*self.ts/4
            if self.bateria <= 0.0:
                self.bateria = 0.0
                self.carregando = True
                self.call_set_led(3,True)

        self.get_logger().info("Nivel da bateria em: " + str(self.bateria))


    def callback_call_set_led(self,future, request):
        response = future.result()
        self.get_logger().info(str(request.led_number) + str(request.state) + str(response.success))
 
 
def main(args=None):
    rclpy.init(args=args)
    node = BatteryNode()
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()