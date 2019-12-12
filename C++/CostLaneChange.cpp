#include <iostream>
#include <vector>
#include <cmath>
using std::endl;
using std::cout;


double goal_distance_cost(int goal_lane, int intended_lane,int final_lane,double distance_to_goal);


int main() {
  int goal_lane=0;
  // Test cases used for grading - do not change.
  double cost;
  cout << "Costs for (intended_lane, final_lane, goal_distance):" << endl;
  cout << "---------------------------------------------------------" << endl;
  cost = goal_distance_cost(goal_lane, 2, 2, 1.0);
  cout << "The cost is " << cost << " for " << "(2, 2, 1.0)" << endl;
  cost = goal_distance_cost(goal_lane, 2, 2, 10.0);
  cout << "The cost is " << cost << " for " << "(2, 2, 10.0)" << endl;
  cost = goal_distance_cost(goal_lane, 2, 2, 100.0);
  cout << "The cost is " << cost << " for " << "(2, 2, 100.0)" << endl;
  cost = goal_distance_cost(goal_lane, 1, 2, 100.0);
  cout << "The cost is " << cost << " for " << "(1, 2, 100.0)" << endl;
  cost = goal_distance_cost(goal_lane, 1, 1, 100.0);
  cout << "The cost is " << cost << " for " << "(1, 1, 100.0)" << endl;
  cost = goal_distance_cost(goal_lane, 0, 1, 100.0);
  cout << "The cost is " << cost << " for " << "(0, 1, 100.0)" << endl;
  cost = goal_distance_cost(goal_lane, 0, 0, 100.0);
  cout << "The cost is " << cost << " for " << "(0, 0, 100.0)" << endl;


  return 0;
}

double goal_distance_cost(int goal_lane, int intended_lane,int final_lane,double distance_to_goal)
{
  double cost=0;
  int delta_d=2.0*goal_lane-intended_lane-final_lane;
  cost=1-exp(-(std::abs(delta_d)/distance_to_goal));
  return cost;

}
