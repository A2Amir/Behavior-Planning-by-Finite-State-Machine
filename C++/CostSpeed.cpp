#include <iostream>
#include <vector>
#include <cmath>

using std::cout;
using std::endl;

double inefficiency_cost(int target_speed, int intended_lane, int final_lane, const std::vector<int> &lane_speeds);
int main()
{
  // Target speed of our vehicle
   int target_speed = 10;

   // Lane speeds for each lane
   std::vector<int> lane_speeds = {6, 7, 8, 9};

   // Test cases used for grading - do not change.
   double cost;
   cout << "Costs for (intended_lane, final_lane):" << endl;
   cout << "---------------------------------------------------------" << endl;
   cost = inefficiency_cost(target_speed, 3, 3, lane_speeds);
   cout << "The cost is " << cost << " for " << "(3, 3)" << endl;
   cost = inefficiency_cost(target_speed, 2, 3, lane_speeds);
   cout << "The cost is " << cost << " for " << "(2, 3)" << endl;
   cost = inefficiency_cost(target_speed, 2, 2, lane_speeds);
   cout << "The cost is " << cost << " for " << "(2, 2)" << endl;
   cost = inefficiency_cost(target_speed, 1, 2, lane_speeds);
   cout << "The cost is " << cost << " for " << "(1, 2)" << endl;
   cost = inefficiency_cost(target_speed, 1, 1, lane_speeds);
   cout << "The cost is " << cost << " for " << "(1, 1)" << endl;
   cost = inefficiency_cost(target_speed, 0, 1, lane_speeds);
   cout << "The cost is " << cost << " for " << "(0, 1)" << endl;
   cost = inefficiency_cost(target_speed, 0, 0, lane_speeds);
   cout << "The cost is " << cost << " for " << "(0, 0)" << endl;
   return 0;
}
double inefficiency_cost(int target_speed, int intended_lane, int final_lane, const std::vector<int> &lane_speeds)
{
    // Cost becomes higher for trajectories with intended lane and final lane
  //   that have traffic slower than target_speed.

  double cost=0;
  double speed_intended=lane_speeds[intended_lane];
  double speed_final=lane_speeds[final_lane];
  cost=(2.0*target_speed-speed_intended-speed_final)/target_speed;
  return cost;
}
