from collections import namedtuple
from math import sqrt, exp

TrajectoryData = namedtuple("TrajectoryData", [
    'intended_lane',
    'final_lane',
    'end_distance_to_goal',
    ])

#weights for costs
REACH_GOAL = 10 ** 6
EFFICIENCY = 10 ** 5

DEBUG = False


def goal_distance_cost(vehicle, trajectory, predictions, data):
    """
    Cost increases based on distance of intended lane (for planning a lane change) and final lane of trajectory.
    Cost of being out of goal lane also becomes larger as vehicle approaches goal distance.
    """
    distance = abs(data.end_distance_to_goal)
    if distance:
        cost = 1 - 2*exp(-(abs(2.0*vehicle.goal_lane - data.intended_lane - data.final_lane) / distance))
    else:
        cost = 1
    return cost


def inefficiency_cost(vehicle, trajectory, predictions, data):
    """
    Cost becomes higher for trajectories with intended lane and final lane that have slower traffic. 
    """

    proposed_speed_intended = velocity(predictions, data.intended_lane) or vehicle.target_speed
    proposed_speed_final = velocity(predictions, data.final_lane) or vehicle.target_speed
    
    cost = float(2.0*vehicle.target_speed - proposed_speed_intended - proposed_speed_final)/vehicle.target_speed

    return cost


def calculate_cost(vehicle, trajectory, predictions, verbose=False):
    """
    Sum weighted cost functions to get total cost for trajectory.
    """
    trajectory_data = get_helper_data(vehicle, trajectory, predictions)
    #print(trajectory_data)
    cost = 0.0
    cf_list = [goal_distance_cost, inefficiency_cost]
    weight_list = [REACH_GOAL, EFFICIENCY]

    for weight, cf in zip(weight_list, cf_list):
        new_cost = weight*cf(vehicle, trajectory, predictions, trajectory_data)
        if DEBUG or verbose:
            print ("{} has cost {} for lane {}".format(cf.__name__, new_cost, trajectory[-1].lane))
        cost += new_cost
    return cost

def get_helper_data(vehicle, trajectory, predictions):
    """
    Generate helper data to use in cost functions:
    indended_lane: the current lane +/- 1 if vehicle is planning or executing a lane change.
    final_lane: the lane of the vehicle at the end of the trajectory.
    distance_to_goal: the distance of the vehicle to the goal.

    Note that indended_lane and final_lane are both included to help differentiate between planning and executing
    a lane change in the cost functions.
    """

    last = trajectory[1]

    if last.state == "PLCL":
        intended_lane = last.lane + 1
    elif last.state == "PLCR":
        intended_lane = last.lane - 1
    else:
        intended_lane = last.lane

    distance_to_goal = vehicle.goal_s - last.s
    final_lane = last.lane

    return TrajectoryData(
        intended_lane,
        final_lane,
        distance_to_goal)


def velocity(predictions, lane):
    """
    All non ego vehicles in a lane have the same speed, so to get the speed limit for a lane,
    we can just find one vehicle in that lane.
    """
    for v_id, predicted_traj in predictions.items():
        if predicted_traj[0].lane == lane and v_id != -1:
            return predicted_traj[0].v
