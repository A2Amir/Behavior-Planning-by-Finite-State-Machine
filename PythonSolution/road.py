import random
from vehicle import Vehicle
import pdb

class Road(object):
    ego_rep = " *** "
    ego_key = -1
    
    def __init__(self, speed_limit, traffic_density, lane_speeds, visible_length):
        self.visible_length = visible_length
        self.num_lanes = len(lane_speeds)
        self.lane_speeds = lane_speeds
        self.speed_limit = speed_limit
        self.density = traffic_density
        self.camera_center = self.visible_length / 2
        self.vehicles = {}
        self.num_vehicles_added = 0
        self.goal_lane = None
        self.goal_s = None
        self.timestep = 0
                
    def get_ego(self):
        return self.vehicles[self.ego_key]
        
    def populate_traffic(self):
        for lane_num in range(self.num_lanes):
            lane_speed = self.lane_speeds[lane_num]
            iterator = iter(range(self.visible_length))
            for s in iterator:
                if random.random() < self.density:
                    vehicle = Vehicle(lane_num, s, lane_speed, 0)
                    vehicle.state = "CS"
                    self.num_vehicles_added += 1
                    self.vehicles[self.num_vehicles_added] = vehicle
                    #skip the next s distance so cars aren't added too closely
                    s = next(iterator)

    def advance(self):
        predictions = {}
        # Generate predictions
        for v_id, v in self.vehicles.items():
            if v_id != self.ego_key:
                preds = v.generate_predictions()
                predictions[v_id] = preds

        # Choose next state based on predictions and
        # update kinematics/state for all vehicles.
        for v_id, v in self.vehicles.items():
            if v_id == self.ego_key:
                trajectory = v.choose_next_state(predictions)
                v.realize_next_state(trajectory)
            else:
                v.increment()

        self.timestep += 1

    def add_ego(self, lane_num, s, config_data):
        to_delete_id = None
        for v_id, v in self.vehicles.items():
            if v.lane == lane_num and v.s == s:
                to_delete_id = v_id
        if to_delete_id:
            del self.vehicles[to_delete_id]

        ego = Vehicle(lane_num, s, self.lane_speeds[lane_num], 0)
        ego.configure(config_data)
        self.goal_lane = ego.goal_lane
        self.goal_s = ego.goal_s
        ego.state = "KL"
        self.vehicles[self.ego_key] = ego


    def __repr__(self):
        s = self.vehicles.get(self.ego_key).s
        self.camera_center = max(s, self.visible_length / 2)
        s_min = max(int(self.camera_center - self.visible_length /2), 0)
        s_max = s_min + self.visible_length
        road = [["     " if i % 3 == 0 else "     "for ln in range(self.num_lanes)] for i in range(self.visible_length)]
        if s_min <= self.goal_s < s_max:
            # print "goal_s is {}".format(self.goal_s)
            # pdb.set_trace()
            road[self.goal_s - s_min][self.goal_lane] = " -G- "
        for v_id, v in self.vehicles.items():
            if s_min <= v.s < s_max:
                if v_id == self.ego_key:
                    marker = self.ego_rep
                else:
                    marker = " %03d " % v_id
                try:
                    road[int(v.s) - s_min][v.lane] = marker
                except IndexError:
                    print (v.s, s_min, v.lane)

                    print ("IndexError")
                    pdb.set_trace()
                    continue
        s = ""
        i = s_min
        for l in road:
            if i % 20 == 0:
                s += "%03d - " % i
            else:
                s += "      "
            i += 1
            s += "|" + "|".join(l) + "|"
            s += "\n"
        return s