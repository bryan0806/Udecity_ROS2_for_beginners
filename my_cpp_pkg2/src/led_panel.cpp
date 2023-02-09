#include "rclcpp/rclcpp.hpp"

#include  "my_robot_interfaces/msg/led_state_array.hpp" //here, cpp seems to have problem with building . can only use python to use self interfaces
#include "my_robot_interfaces/srv/set_led.hpp"
 
class LedPanelNode : public rclcpp::Node 
{
public:
    LedPanelNode() : Node("led_panel") 
    {
        this->declare_parameter("led_states", std::vector<int64_t>{0,0,0});
        led_state_ = this->get_parameter("led_states").as_integer_array();

        pub_ = this->create_publisher<my_robot_interfaces::msg::LedStateArray>("publish_led_states",10);
        timer_ = this->create_wall_timer(std::chrono::seconds(4),std::bind(&LedPanelNode::publishLedStates,this));
        set_led_service_ = this->create_service<my_robot_interfaces::srv::SetLed>("set_led",std::bind(&LedPanelNode::callbackSetLed,this,std::placeholders::_1,std::placeholders::_2));
        RCLCPP_INFO(this->get_logger(),"led panel has been started.");
    }
 
private:

    void publishLedStates()
    {
        auto msg = my_robot_interfaces::msg::LedStateArray();
        msg.led_states = led_state_;
        pub_->publish(msg);

    }

    void callbackSetLed(const my_robot_interfaces::srv::SetLed::Request::SharedPtr request,const my_robot_interfaces::srv::SetLed::Response::SharedPtr response)
    {
        int64_t led_number = request->led_number;
        int64_t state = request->state;

        if(led_number > (int64_t)led_state_.size() || led_number <= 0)
        {
            response->success = false;
            return;
        }

        if(state != 0 && state!= 1)
        {
            response->success = false;
            return;
        }

        led_state_[led_number-1]=state;
        response->success = true;
        publishLedStates();

    }

    std::vector<int64_t> led_state_;
    rclcpp::Publisher<my_robot_interfaces::msg::LedStateArray>::SharedPtr pub_;
    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Service<my_robot_interfaces::srv::SetLed>::SharedPtr set_led_service_;
};
 
int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<LedPanelNode>(); 
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}