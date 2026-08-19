#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.msg import LedPanelStatus
from my_robot_interfaces.srv import SetLedState


class LedPanelNode(Node): 
    def __init__(self):
        super().__init__("led_panel")
        self.ledpanel = [False, False, False]
        self.lp_status_pub_ = self.create_publisher(LedPanelStatus, "led_panel_state", 10)
        self.server_ = self.create_service(SetLedState, "set_led", self.callback_set_led)
        self.get_logger().info("Led Panel node has been started.")

    def callback_set_led(self,request: SetLedState.Request, response: SetLedState.Response):
        ln = request.led_number
        state = request.state

        if ln not in [1, 2, 3] or state not in [True, False]:
            response.success = False
            return response

        self.ledpanel[ln-1] = state
        msg = LedPanelStatus()
        msg.led_states = self.ledpanel
        self.lp_status_pub_.publish(msg)

        response.success = True
        return response
 
def main(args=None):
    rclpy.init(args=args)
    node = LedPanelNode() 
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()