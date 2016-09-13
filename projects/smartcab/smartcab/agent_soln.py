import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'white'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.Q = dict()  # (state, action) => Q value map, nested dict instead of table
        self.policy = dict()  # state => best action map
        self.alpha = 0.1  # learning rate
        self.epsilon = 0.5  # exploration factor - fraction of time to select random action
    
    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        self.epsilon = 0.75 * self.epsilon  # reduce exploration

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        self.state = (self.next_waypoint, inputs['light'], inputs['oncoming'])

        # TODO: Select action according to your policy
        action = None
        if (self.state not in self.policy) or (random.random() < self.epsilon):
            print "LearningAgent.update(): Random action"  # [debug]
            action = random.choice(['forward', 'left', 'right', None])
        else:
            action = self.policy[self.state]
        
        # Execute action and get reward
        reward = self.env.act(self, action)

        # TODO: Learn policy based on state, action, reward
        if self.state not in self.Q:
            self.Q[self.state] = dict()
        if action not in self.Q[self.state]:
            self.Q[self.state][action] = 0
        self.Q[self.state][action] = (1.0 - self.alpha) * self.Q[self.state][action] + self.alpha * reward  # current reward only
        best_action = None
        best_Q = - float('inf')
        for action, Q in self.Q[self.state].iteritems():
            if Q > best_Q:
                best_Q = Q
                best_action = action
        self.policy[self.state] = best_action
        
        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=2, display=True, log_metrics = True)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=20)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    run()
