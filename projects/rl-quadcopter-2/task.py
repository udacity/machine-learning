import numpy as np
import math
from physics_sim import PhysicsSim

class Task():
    """Task (environment) that defines the goal and provides feedback to the agent."""
    def __init__(self, init_pose=None, init_velocities=None, 
        init_angle_velocities=None, runtime=5., target_pos=None):
        """Initialize a Task object.
        Params
        ======
            init_pose: initial position of the quadcopter in (x,y,z) dimensions and the Euler angles
            init_velocities: initial velocity of the quadcopter in (x,y,z) dimensions
            init_angle_velocities: initial radians/second for each of the three Euler angles
            runtime: time limit for each episode
            target_pos: target/goal (x,y,z) position for the agent
        """
        # Simulation
        self.sim = PhysicsSim(init_pose, init_velocities, init_angle_velocities, runtime) 
        self.action_repeat = 3

        self.state_size = self.action_repeat * 6
        self.action_low = 0
        self.action_high = 900
        self.action_size = 4

        self.prev_v = [0, 0, 0]
        self.prev_angle_v = 0
        self.prev_rotor = [0,0,0,0]
        # Goal
        self.target_pos = target_pos if target_pos is not None else np.array([0., 0., 10.]) 

    def get_reward(self):
        """Uses current pose of sim to return reward."""
        reward = 1.- (abs(self.sim.pose[:3] - self.target_pos)).sum()
        return reward

    def get_distance(self):
        distance_x = (self.target_pos[0] - abs(self.sim.pose[0])) ** 2
        distance_y = (self.target_pos[1] - abs(self.sim.pose[1])) ** 2
        distance_z = (self.target_pos[2] - abs(self.sim.pose[2])) ** 2
        distance = math.sqrt(distance_x + distance_y + distance_z)
#         distance = (distance_x + distance_y + distance_z) # Squared Euclidean difference
        return distance
    
    def calc_reward(self, prev_v, prev_angle_v, rotor_speeds):
        """Calculate Take off rewards"""
        distance_reward = 0
#       Basic working function which generates increasing rewards
#         distance_x = (self.target_pos[0] - abs(self.sim.pose[0])) ** 2
#         distance_y = (self.target_pos[0] - abs(self.sim.pose[0])) ** 2
#         distance_z = (self.target_pos[2] - abs(self.sim.pose[2])) ** 2
#         distance = math.sqrt(distance_x + distance_y + distance_z)
#         distance = (distance_x + distance_y + distance_z) # Squared Euclidean difference
#         distance = max(abs(self.target_pos[0] - self.sim.pose[0]), abs(self.target_pos[1] - self.sim.pose[1]) , abs(self.target_pos[2] - self.sim.pose[2])) #Chebyshev Distance
#         distance = abs(self.target_pos[0] - self.sim.pose[0]) + abs(self.target_pos[1] - self.sim.pose[1]) + 1.2 * abs(self.target_pos[2] - self.sim.pose[2]) #Mahattan Distance
        distance = self.get_distance()
        if distance == 0 or ( self.sim.pose[2] >=9 and self.sim.pose[2] <= 11):
#             print("\ndistance == 0")
            distance_reward += 100
        else:
            if self.sim.pose[0] == self.target_pos[0] and self.target_pos[1] == self.sim.pose[1]:
                distance_reward += 0.2
            else:
                distance_reward += -0.025
            if self.sim.pose[2] > 0:
                distance_reward += 0.5
            else:
                distance_reward += -0.75
            if abs(self.sim.v[0]) + abs(self.sim.v[1]) > 0:
                distance_reward += -2
            else:
                distance_reward += 0.5
                
            if self.sim.v[2] > 0:
                distance_reward += 0.5
            else:
                distance_reward += -0.75
            if sum(abs(self.sim.angular_v)) > 0:
                distance_reward += -2
            else:
                distance_reward += 1
            
#         elif self.sim.pose[2] > 0:
#             distance_reward += 2
#             if self.sim.v[2] > 0:
#                 distance_reward += 2
#             elif self.sim.v[2] == 0:
#                 distance_reward += -1
# #         elif self.sim.pose[0] != self.target_pos[0] and self.sim.pose[1] != self.target.pos[1]:
#         else: 
#             distance_reward += -5
#                 distance_reward = np.tanh(1-distance)
#         Calculate velocity rewards
#         velocity_diff = [ min(prev_v[x],self.sim.v[x]) for x in range(len(self.sim.v)) ] 
#         velocity_reward = (sum(velocity_diff) * 0.0075)
#         velocity_reward = sum(velocity_diff)

        return np.clip(distance_reward,-1,1)
#         return distance_reward


    def step(self, rotor_speeds):
        """Uses action to obtain next state, reward, done."""
        reward = 0
        pose_all = []
        for _ in range(self.action_repeat):
            done = self.sim.next_timestep(rotor_speeds) # update the sim pose and velocities
            reward += self.get_reward() 
            pose_all.append(self.sim.pose)

        next_state = np.concatenate(pose_all)
        return next_state, reward, done
    
    def move_step(self, rotor_speeds):
        """Uses action to obtain next state, reward, done."""
        reward = 0
        pose_all = []
        pose_speed = []

        for _ in range(self.action_repeat):
            done = self.sim.next_timestep(rotor_speeds) # update the sim pose and velocities
#                 print("move_step: {}".format(done))
#             if pose_speed:
#                 max_v = self.get_max_v(pose_speed)

            reward += self.calc_reward(prev_v=self.prev_v, prev_angle_v=self.prev_angle_v, rotor_speeds=rotor_speeds) 
            pose_all.append(self.sim.pose)
            pose_speed.append(self.sim.v)

            self.prev_v = self.sim.v
            self.prev_angle_v = self.sim.angular_v
            self.prev_rotor = rotor_speeds
            if self.get_distance == 0 or ( self.sim.pose[2] >=9 and self.sim.pose[2] <= 11):
#                 print("distance == 0")
                done = True
                
        next_state = np.concatenate(pose_all)
        return next_state, reward, done
            
    def get_max_v(self, pose_speeds):
            max_v = np.max(pose_speeds, axis=0)
            return max_v
            
    def reset(self):
        """Reset the sim to start a new episode."""
        self.sim.reset()
        state = np.concatenate([self.sim.pose] * self.action_repeat) 
        return state
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))