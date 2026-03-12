#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/joy.hpp>
#include <chrono>

using namespace std::chrono_literals;

class DeplacementRobotNode : public rclcpp::Node
{
public:
  DeplacementRobotNode()
  : Node("republish_joy_node"), is_first_message_(true)
  {
    joy_pub_ = this->create_publisher<sensor_msgs::msg::Joy>("/joy_out", 10);
    joy_sub_ = this->create_subscription<sensor_msgs::msg::Joy>(
      "/joy_ihm", 10, std::bind(&DeplacementRobotNode::joyCallback, this, std::placeholders::_1));
    
    timer_ = this->create_wall_timer(200ms, std::bind(&DeplacementRobotNode::timerCallback, this));
    
    RCLCPP_INFO(this->get_logger(), "DeplacementRobotNode has been started.");
  }

private:
  void joyCallback(const sensor_msgs::msg::Joy::SharedPtr msg)
  {
    if (is_first_message_ || !are_joy_msgs_equal(*msg, last_joy_msg_)) {
      last_joy_msg_ = *msg;
      is_first_message_ = false;
    }
  }

  void timerCallback()
  {
    if (!is_first_message_) {
      joy_pub_->publish(last_joy_msg_);
    }
  }

  bool are_joy_msgs_equal(const sensor_msgs::msg::Joy & a, const sensor_msgs::msg::Joy & b)
  {
    if (a.axes.size() != b.axes.size() || a.buttons.size() != b.buttons.size()) {
      return false;
    }
    for (size_t i = 0; i < a.axes.size(); ++i) {
      if (a.axes[i] != b.axes[i]) return false;
    }
    for (size_t i = 0; i < a.buttons.size(); ++i) {
      if (a.buttons[i] != b.buttons[i]) return false;
    }
    return true;
  }

  rclcpp::Publisher<sensor_msgs::msg::Joy>::SharedPtr joy_pub_;
  rclcpp::Subscription<sensor_msgs::msg::Joy>::SharedPtr joy_sub_;
  rclcpp::TimerBase::SharedPtr timer_;
  sensor_msgs::msg::Joy last_joy_msg_;
  bool is_first_message_;
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<DeplacementRobotNode>());
  rclcpp::shutdown();
  return 0;
}
