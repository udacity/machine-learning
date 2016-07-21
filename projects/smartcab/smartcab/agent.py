from __future__ import division
import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
import numpy as np
import pandas as pd


#global variables
success_times = 0
trials_times = 100
total_reward = []
k_var = 100



class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here

        #Initialize the Q-value table
        all_states = [(intention, light, oncoming, left, right)
                      for intention in self.env.valid_actions
                      for light in ['red', 'green']
                      for oncoming in self.env.valid_actions
                      for left in self.env.valid_actions
                      for right in self.env.valid_actions]
        self.Qtable = {state: {action: 0 for action in self.env.valid_actions} for state in all_states}# all items in the table is 0
        self.transition_list = [] # state and action of every step
        #print self.Qtable

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        self.transition_list = []

    def get_action_probability(self, state, k):
        self.prob_list = []
        row_of_Qtable = pd.Series(self.Qtable[state])
        self.prob_list = [ (x / row_of_Qtable.rpow(k).sum() ) for x in row_of_Qtable.rpow(k)]
        #print self.prob_list
        return self.prob_list

    def reward_of_a_trial(self):
        sum_reward = 0
        for step in self.transition_list:
            sum_reward += step[2]
        return sum_reward

    def select_action_with_maxQvalue(self, state):
        row = self.Qtable[state]
        max_value = max(row.values())
        p1 = {key: value for key, value in row.items() if value == max_value} # considering there are more than one max
        action_list = []
        for action in p1:
            action_list.append(action)
        return random.choice(action_list)

    def select_action(self, actions, probs): # select an action by its probability
        x = random.uniform(0, 1)
        #print 'random x is {}'.format(x)
        cumulative_probability = 0.0
        for item, item_probability in zip(actions, probs):
            cumulative_probability += item_probability
            #print 'cumulative_probability is {}'.format(cumulative_probability)
            if x < cumulative_probability:
                break
        return item

    def update_Qtable(self, gamma, alpha):# gamma: the discounting factor, alpha: the learning rate
        for i, step in enumerate(self.transition_list[::-1]):   #back propogation
            old_value = self.Qtable[step[0]][step[1]]
            row_of_Qtable = pd.Series(self.Qtable[self.transition_list[-i][0]])
            learned_value = step[2] + gamma * row_of_Qtable.max()
            new_value = old_value + alpha * ( learned_value - old_value )
            self.Qtable[step[0]][step[1]] = new_value
            #print 'state {} action {} reward {} old_Qvalue: {} new_Qvalue: {}'\
                   # .format(step[0],step[1],step[2],old_value, new_value )




    def update(self, t):
        global k_var
        global success_times
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        #self.state = {'location': self.env.agent_states[self]['location'], 'heading': self.env.agent_states[self]['heading']}
        self.state = ( self.next_waypoint,
                       inputs['light'],
                       inputs['oncoming'],
                       inputs['left'],
                       inputs['right'])

        # TODO: Select action according to your policy
        #action = None
        #action = self.next_waypoint
        #action = random.choice(self.env.valid_actions)
        #action = self.select_action_with_maxQvalue(self.state)
        action = self.select_action(self.env.valid_actions, self.get_action_probability(self.state, k= k_var))# select an action with greatest Q-value

        # Execute action and get reward
        reward = self.env.act(self, action)

        # TODO: Record every step's state , action and reward
        self.transition_list.append((self.state, action, reward))

        # TODO: Learn policy based on state, action, reward

        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]
        #if self.state['location'] == self.env.agent_states[self]['destination']:
        if self.env.done:
            self.update_Qtable(gamma=0.7, alpha=0.15)
            total_reward.append(self.reward_of_a_trial())
            #print self.Qtable.items()
            #k_var += 0.5
            success_times += 1
            print success_times


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.001, display=False)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=trials_times)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line
    print 'Agent reached destination for {} times.'.format(success_times)
    for i, trial in enumerate(total_reward):
        print 'Successful Trial No. {} final reward is {}.'.format(i+1, trial)

if __name__ == '__main__':
    run()
