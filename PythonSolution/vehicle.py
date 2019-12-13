from cost_functions import calculate_cost

lane_direction = {"PLCL": 1, "LCL": 1, "LCR": -1, "PLCR": -1}

class Vehicle(object):
    preferred_buffer = 6 # impacts "keep lane" behavior.

    def __init__(self, lane, s, v, a, state="CS"):
        self.lane = lane
        self.s = s 
        self.v = v
        self.a = a
        self.state = state #constant speed

        # The following are set when configure() is called.
        # All of them are integers.
        self.max_acceleration = None 
        self.target_speed = None     
        self.lanes_available = None  
        self.goal_lane = None        
        self.goal_s = None


    def choose_next_state(self, predictions):
        """
        Implement the transition_function code from the Behavior Planning Pseudocode
        classroom concept. 

        INPUTS: A predictions dictionary. This is a dictionary of vehicle id keys with predicted
            vehicle trajectories as values. Trajectories are a list of Vehicle objects representing
            the vehicle at the current timestep and one timestep in the future.
        OUTPUT: The the best (lowest cost) trajectory corresponding to the next ego vehicle state.
        """

        states = self.successor_states()
        costs = []
        for state in states:
            trajectory = self.generate_trajectory(state, predictions)
            if trajectory:
                
                cost = calculate_cost(self, trajectory, predictions)
                costs.append({"cost" : cost, "state": state, "trajectory": trajectory})

        best = min(costs, key=lambda s: s['cost'])
        return best["trajectory"]


    def successor_states(self):
        """
        Provides the possible next states given the current state for the FSM discussed in the course,
        with the exception that lane changes happen instantaneously, so LCL and LCR can only transition back to KL.
        """
        if self.state == "KL":
            states = ["KL", "PLCL", "PLCR"]
        elif self.state == "PLCL":
            states = ["KL"]
            if self.lane != (self.lanes_available-1):
                states.append("PLCL")
                states.append("LCL")
        elif self.state == "PLCR":
            states = ["KL"]
            if self.lane != 0:
                states.append("PLCR")
                states.append("LCR")
        elif self.state in ("LCL", "LCR"):
            states = ["KL"]
        return states


    def generate_trajectory(self, state, predictions):
        """
        Given a possible next state, generate a trajectory to realize the next state.
        """
        if   state == "CS"  : trajectory = self.constant_speed_trajectory()
        elif state == "KL"  : trajectory = self.keep_lane_trajectory(predictions)
        elif state in ("LCL", "LCR") : trajectory = self.lane_change_trajectory(predictions, state)
        elif state in ("PLCL", "PLCR"): trajectory = self.prep_lane_change_trajectory(predictions, state)
        return trajectory


    def get_kinematics(self, predictions, lane):
        """
        Gets next timestep kinematics (position, velocity, acceleration) for a given lane.
        Tries to choose the maximum velocity and acceleration, given other vehicle positions and accel/velocity constraints.
        """
        max_velocity_accel_limit = self.max_acceleration + self.v
        vehicle_ahead = self.get_vehicle_ahead(predictions, lane)
        vehicle_behind = self.get_vehicle_behind(predictions, lane)

        if vehicle_ahead: 

            if vehicle_behind:
                #must travel at the speed of traffic, regardless of preferred buffer
                new_velocity = vehicle_ahead.v
            else:
                #choose max velocity and acceleration that leaves desired buffer in front
                #Equation: front buffer <= (vcl.s - ego.s) + (vcl.v - ego.v)*t + 0.5 * (vcl.a - ego.a)*t*t
                max_velocity_in_front = (vehicle_ahead.s - self.s - self.preferred_buffer) + vehicle_ahead.v - 0.5 * self.a
                new_velocity = min(max_velocity_in_front, max_velocity_accel_limit, self.target_speed)

        else:
            new_velocity = min(max_velocity_accel_limit, self.target_speed)

        new_accel = new_velocity - self.v #Equation: (v_1 - v_0)/t = acceleration
        new_position = self.s + new_velocity + new_accel / 2.0
        return new_position, new_velocity, new_accel


    def constant_speed_trajectory(self):
        trajectory = [Vehicle(self.lane, self.s, self.v, self.a, self.state), 
                      Vehicle(self.lane, self.position_at(1), self.v, 0, self.state)]
        return trajectory

    def keep_lane_trajectory(self, predictions):
        trajectory = [Vehicle(self.lane, self.s, self.v, self.a, self.state)]
        s, v, a = self.get_kinematics(predictions, self.lane)
        trajectory.append(Vehicle(self.lane, s, v, a, "KL"))
        return trajectory

    def prep_lane_change_trajectory(self, predictions, state):
        new_lane = self.lane + lane_direction[state]
        trajectory = [Vehicle(self.lane, self.s, self.v, self.a, self.state)]

        curr_lane_new_kinematics = self.get_kinematics(predictions, self.lane)
        if self.get_vehicle_behind(predictions, self.lane):
            s, v, a = curr_lane_new_kinematics #keep speed of current lane so as not to collide with car behind
        else: 
            next_lane_new_kinematics = self.get_kinematics(predictions, new_lane)
            s, v, a = min([next_lane_new_kinematics, curr_lane_new_kinematics], key=lambda x: x[1]) #choose kinematics with lowest velocity

        trajectory.append(Vehicle(self.lane, s, v, a, state))
        return trajectory

    def lane_change_trajectory(self, predictions, state):
        #check to make sure the space is free
        new_lane = self.lane + lane_direction[state]
        for vehicle_id, prediction in predictions.items():
            if prediction[0].s == self.s and prediction[0].lane == new_lane:
                return None

        trajectory = [Vehicle(self.lane, self.s, self.v, self.a, self.state)]
        s, v, a = self.get_kinematics(predictions, new_lane)
        trajectory.append(Vehicle(new_lane, s, v, a, state))
        return trajectory

    def increment(self, dt=1):
        """
        Sets vehicle position one step ahead.
        """
        self.s = self.position_at(dt)
            
    def position_at(self, t):
        """
        Predicts position of vehicle in t seconds. Used in incrementing
        vehicle positions and also trajectory generation.
        """
        return self.s + self.v * t + self.a * t * t / 2.0

    def get_vehicle_behind(self, predictions, lane):
        vehicles_behind = [v[0] for (v_id, v) in predictions.items() if v[0].lane == lane and v[0].s < self.s]
        if vehicles_behind:
            return max(vehicles_behind, key=lambda v: v.s)

    def get_vehicle_ahead(self, predictions, lane):
        vehicles_ahead = [v[0] for (v_id, v) in predictions.items() if v[0].lane == lane and v[0].s > self.s]
        if vehicles_ahead:
            return min(vehicles_ahead, key=lambda v: v.s)

    def generate_predictions(self, horizon=2):
        """
        Generates predictions for non-ego vehicles to be used
        in trajectory generation for ego vehicle.
        """
        predictions = []
        for i in range(horizon):
            s = self.position_at(i)
            v = 0
            if(i < horizon-1):
                v = self.position_at(i+1) - s
            predictions.append(Vehicle(self.lane, s, v, 0))
        return predictions

    def realize_next_state(self, trajectory):
        """
        Sets state and kinematics for ego vehicle using the last state of the trajectory.
        """
        next_state = trajectory[1]
        self.state = next_state.state
        self.lane = next_state.lane
        self.s = next_state.s
        self.v = next_state.v
        self.a = next_state.a

    def configure(self, road_data):
        """
        Called by simulator before simulation begins. Sets various
        parameters which will impact the ego vehicle. 
        """
        self.target_speed = road_data['speed_limit']
        self.lanes_available = road_data["num_lanes"]
        self.max_acceleration = road_data['max_acceleration']
        goal = road_data['goal']
        self.goal_lane = goal[1]
        self.goal_s = goal[0]
                            



