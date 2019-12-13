#ifndef COST_H
#define COST_H

#include "vehicle.h"

using std::map;
using std::string;
using std::vector;

float calculate_cost(const Vehicle &vehicle,
                     const map<int, vector<Vehicle>> &predictions,
                     const vector<Vehicle> &trajectory);

float goal_distance_cost(const Vehicle &vehicle,
                         const vector<Vehicle> &trajectory,
                         const map<int, vector<Vehicle>> &predictions,
                         map<string, float> &data);

float inefficiency_cost(const Vehicle &vehicle,
                        const vector<Vehicle> &trajectory,
                        const map<int, vector<Vehicle>> &predictions,
                        map<string, float> &data);

float lane_speed(const map<int, vector<Vehicle>> &predictions, int lane);

map<string, float> get_helper_data(const Vehicle &vehicle,
                                   const vector<Vehicle> &trajectory,
                                   const map<int, vector<Vehicle>> &predictions);

#endif  // COST_H
