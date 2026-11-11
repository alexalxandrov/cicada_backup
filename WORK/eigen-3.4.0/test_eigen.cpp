#include <Eigen/Dense>
#include <iostream>

int main() {
  Eigen::Matrix3d m = Eigen::Matrix3d::Random();
  std::cout << "Random matrix:\n" << m << std::endl;
  return 0;
}