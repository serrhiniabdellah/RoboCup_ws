#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/float64_multi_array.hpp>
#include <std_msgs/msg/int16_multi_array.hpp>
#include <sensor_msgs/msg/joint_state.hpp>
#include <cmath>
#include <vector>

struct Vector3D {
  float x;
  float y;
  float z;
};

class BrasManuelNode : public rclcpp::Node
{
public:
  BrasManuelNode()
  : Node("bras_manuel_node")
  {
    // Publishers
    pub_joints_ = this->create_publisher<sensor_msgs::msg::JointState>("joint_states", 10);
    pub_angle_ = this->create_publisher<std_msgs::msg::Int16MultiArray>("retour_angles", 10);

    // Subscriber
    sub_data_ = this->create_subscription<std_msgs::msg::Float64MultiArray>(
      "data", 10, std::bind(&BrasManuelNode::chatterCallback, this, std::placeholders::_1));

    // Initialize joint state
    joint_state_.name = {
      "base_link_to_double_shoulder",
      "double_shoulder_to_arm",
      "arm_to_upper_forearm",
      "upper_forearm_to_lower_forearm",
      "lower_forearm_to_wrist",
      "wrist_to_gripper_body"
    };
    joint_state_.position.resize(6, 0.0);

    L1 = 0.06f; L2 = 0.3f; L3 = 0.0f; L4 = 0.2f; L5 = 0.077f; L6 = 0.014f;
    
    for (int i = 0; i < 7; i++) {
        theta[i] = 0.0f;
        anc_theta[i] = 0.0f;
    }

    RCLCPP_INFO(this->get_logger(), "BrasManuelNode has been started.");
  }

private:
  void chatterCallback(const std_msgs::msg::Float64MultiArray::SharedPtr msg)
  {
    if (msg->data.size() < 8) return;

    Vector3D pos = { (float)msg->data[0], (float)msg->data[1], (float)msg->data[2] };
    Vector3D orient = { (float)msg->data[3], (float)msg->data[4], (float)msg->data[5] };
    float gripper = (float)msg->data[6];
    // msg->data[7] is reboot in some versions

    CalcIk(&pos, &orient, anc_theta);

    joint_state_.header.stamp = this->now();
    for (int i = 0; i < 6; i++) {
        if (i == 2) {
            joint_state_.position[2] = (theta[2] - 90.0f) * M_PI / 180.0f;
        } else {
            joint_state_.position[i] = theta[i] * M_PI / 180.0f;
        }
        theta[i] = joint_state_.position[i] * 180.0f / M_PI; // Sync back for mapping
    }

    // Mapping for hardware (Int16MultiArray)
    std_msgs::msg::Int16MultiArray retour_angle;
    std::vector<int16_t> theta_int(7);
    
    theta_int[0] = static_cast<int16_t>((joint_state_.position[0] + M_PI) * (4095.0 / (2.0 * M_PI)));
    theta_int[1] = static_cast<int16_t>((joint_state_.position[1] + M_PI) * ((3072.0 - 1024.0) / (2.0 * M_PI)) + 1024.0);
    theta_int[2] = static_cast<int16_t>((joint_state_.position[2] + M_PI) * ((3072.0 - 1024.0) / (2.0 * M_PI)) + 1024.0);
    theta_int[3] = static_cast<int16_t>((joint_state_.position[3] + M_PI) * ((3072.0 - 1024.0) / (2.0 * M_PI)) + 1024.0);
    theta_int[4] = static_cast<int16_t>((joint_state_.position[4] + M_PI) * ((3072.0 - 1024.0) / (2.0 * M_PI)) + 1024.0);
    theta_int[5] = static_cast<int16_t>((joint_state_.position[5] + M_PI) * (1024.0) / (2.0 * M_PI));
    theta_int[6] = static_cast<int16_t>((gripper * 512.0) + 500.0);

    retour_angle.data.assign(theta_int.begin(), theta_int.end());

    pub_joints_->publish(joint_state_);
    pub_angle_->publish(retour_angle);
  }

  bool CalcIk(Vector3D* position, Vector3D* orientation, float anc_theta_in[])
  {
    float px = position->x;
    float py = position->y;
    float pz = position->z;
           
    float rx = -orientation->x * M_PI / 180.0f;
    float ry = -orientation->y * M_PI / 180.0f;
    float rz = orientation->z * M_PI / 180.0f;

    float ax = -sin(rz);
    float ay = cos(rx) * cos(rz);
    float az = cos(rz) * sin(rx);

    // Simple IK logic implementation (simplified version of the provided code)
    float p5x = px - (L5 + L6) * ax;
    float p5y = py - (L5 + L6) * ay;
    float p5z = pz - (L5 + L6) * az;

    theta[0] = atan2(p5x, p5z);
    float A = pow(p5x * p5x + p5z * p5z, 0.5f);
    float B = p5y - L1;
    float C2 = (pow(A, 2) + pow(B, 2) - pow(L2, 2) - pow(L3 + L4, 2))/(2 * L2 * (L3 + L4));

    if (C2 > 1.0f) C2 = 1.0f;
    if (C2 < -1.0f) C2 = -1.0f;

    theta[2] = atan2(pow(1 - pow(C2, 2), 0.5f), C2);
    float M = L2 + (L3 + L4) * C2;
    float N = (L3 + L4) * sin(theta[2]);
    theta[1] = atan2(M * A - N * B, N * A + M * B);

    float C1 = cos(theta[0]);
    float C23 = cos(theta[1] + theta[2]);
    float S1 = sin(theta[0]);
    float S23 = sin(theta[1] + theta[2]);
    
    float asx = ax * C1 - az * S1;
    float asy = ay * C23 + az * C1 * S23 + ax * S1 * S23;
    float asz = az * C1 * C23 - ay * S23 + ax * C23 * S1;

    theta[3] = atan2(asx, asz);
    theta[4] = atan2(sin(theta[3]) * asx + cos(theta[3]) * asz, asy);
    
    // Convert to degrees for output consistency
    for(int i=0; i<6; i++) {
        theta[i] *= 180.0f / M_PI;
        if (std::isnan(theta[i])) {
            theta[i] = anc_theta_in[i];
        } else {
            anc_theta_in[i] = theta[i];
        }
    }
    return true;
  }

  rclcpp::Subscription<std_msgs::msg::Float64MultiArray>::SharedPtr sub_data_;
  rclcpp::Publisher<sensor_msgs::msg::JointState>::SharedPtr pub_joints_;
  rclcpp::Publisher<std_msgs::msg::Int16MultiArray>::SharedPtr pub_angle_;
  sensor_msgs::msg::JointState joint_state_;

  float L1, L2, L3, L4, L5, L6;
  float theta[7];
  float anc_theta[7];
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<BrasManuelNode>());
  rclcpp::shutdown();
  return 0;
}
