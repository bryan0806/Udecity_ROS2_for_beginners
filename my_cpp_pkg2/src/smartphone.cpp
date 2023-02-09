#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/msg/string.hpp"
 
class SMartphoneNode : public rclcpp::Node 
{
public:
    SMartphoneNode() : Node("smartphone") 
    {
        subcriber_ = this->create_subscription<example_interfaces::msg::String>(
            "robot_news",10,
            std::bind(&SMartphoneNode::callbackRobotNews,this,std::placeholders::_1)
        );
        RCLCPP_INFO(this->get_logger(),"smartphone has been started.");

    }
 
private:
    void callbackRobotNews(const example_interfaces::msg::String::SharedPtr msg)
    {
        RCLCPP_INFO(this->get_logger(),"%s", msg->data.c_str());
    }

    rclcpp::Subscription<example_interfaces::msg::String>::SharedPtr subcriber_;
};
 
int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<SMartphoneNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}