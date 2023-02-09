#include "rclcpp/rclcpp.hpp"

#include "my_robot_interfaces/msg/hardware_status.hpp"
 
class HardwareStatusPublisherNode : public rclcpp::Node 
{
public:
    HardwareStatusPublisherNode() : Node("hardware_status_publisher") 
    {
        pub_ = this->create_publisher<my_robot_interfaces::msg::HardwareStatus>("hardware_status",10);
        timer_ = this->create_wall_timer(
                                        std::chrono::seconds(4),
                                        std::bind(&HardwareStatusPublisherNode::publish_hw_status,this));
        RCLCPP_INFO(this->get_logger(),"Hw publisher has been started.");
    }
 
private:
    void publish_hw_status()
    {
        auto msg = my_robot_interfaces::msg::HardwareStatus();
        msg.temperature = 40;
        msg.are_motors_ready = true;
        msg.debug_message = "nothing special...";
        this->pub_->publish(msg);
    }
    rclcpp::Publisher<my_robot_interfaces::msg::HardwareStatus>::SharedPtr pub_;
    rclcpp::TimerBase::SharedPtr timer_;

};
 
int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<HardwareStatusPublisherNode>(); 
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}