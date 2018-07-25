import numpy as np
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

        # Goal
        self.target_pos = target_pos if target_pos is not None else np.array([0., 0., 10.])

    def get_reward(self):
        """Uses current pose of sim to return reward."""
        reward = 1. - .3 * (abs(self.sim.pose[:3] - self.target_pos)).sum()
        return reward

    def step(self, rotor_speeds):
        """Uses action to obtain next state, reward, done."""
        reward = 0
        pose_all = []
        for _ in range(self.action_repeat):
            # update the sim pose and velocities
            done = self.sim.next_timestep(rotor_speeds)
            reward += self.get_reward()
            pose_all.append(self.sim.pose)
        next_state = np.concatenate(pose_all)
        return next_state, reward, done

    def reset(self):
        """Reset the sim to start a new episode."""
        self.sim.reset()
        state = np.concatenate([self.sim.pose] * self.action_repeat)
        return state


class MyTask():
    """Task (environment) that defines the goal and provides feedback to the agent."""

    def __init__(self, init_pose=None, init_velocities=None, init_angle_velocities=None, runtime=5., target_pos=None):
        self.sim = PhysicsSim(init_pose, init_velocities, init_angle_velocities, runtime)
        self.action_repeat = 3

        self.state_size = self.action_repeat * (6 + 3)
        self.action_low = 0
        self.action_high = 900
        self.action_size = 4
        self.target_pos = target_pos if target_pos is not None else np.array([0., 0., 10.])
        self.init_distance = abs(self.target_pos - init_pose[:3]).sum()
        self.previous_direction = self.target_pos - init_pose[:3]
        self.done = False

    def get_reward(self):
        """Uses current pose of sim to return reward."""
        reward = 10.0
        # distance
        current_direction = self.target_pos - self.sim.pose[:3]
        for i in range(3):
            if abs(current_direction)[i] < abs(self.previous_direction)[i]:
                reward -= 0.3 * abs(current_direction[i] / self.previous_direction[i])
            else:
                reward -= 0.3 * abs(current_direction)[i]
        self.previous_direction = current_direction

        # direction
        reward += ([0.01, 0.01, 0.07] * np.multiply(current_direction, self.sim.v)).sum()

        # close enough or too far away
        current_distance = abs(current_direction).sum()
        if current_distance < 1:
            reward = max(100, reward)
            self.done = True
        if current_distance > 2.0 * self.init_distance:
            reward -= 50
        return reward

    def step(self, rotor_speeds):
        reward = 0
        pose_all = []
        for _ in range(self.action_repeat):
            # update the sim pose and velocities
            self.done = self.sim.next_timestep(rotor_speeds)
            reward += self.get_reward()
            pose_all.append(self.sim.pose)
            pose_all.append(self.sim.v)
        next_state = np.concatenate(pose_all)
        return next_state, reward, self.done

    def reset(self):
        """Reset the sim to start a new episode."""
        self.sim.reset()
        state = np.concatenate(([self.sim.pose] + [self.sim.v]) * self.action_repeat)
        return state
