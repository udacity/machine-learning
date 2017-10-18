import time
import random
import math
from collections import OrderedDict
from simulator import Simulator


class TrafficLight(object):
    """A traffic light that switches periodically."""

    valid_states = [True, False]  # True = NS open; False = EW open

    def __init__(self, state=None, period=None):
        self.state = state if state is not None else random.choice(self.valid_states)
        self.period = period if period is not None else random.choice([2, 3, 4, 5])
        self.last_updated = 0

    def reset(self):
        self.last_updated = 0

    def update(self, t):
        if t - self.last_updated >= self.period:
            self.state = not self.state  # Assuming state is boolean
            self.last_updated = t


class Environment(object):
    """Environment within which all agents operate."""

    valid_actions = [None, 'forward', 'left', 'right']
    valid_inputs = {'light': TrafficLight.valid_states, 'oncoming': valid_actions, 'left': valid_actions, 'right': valid_actions}
    valid_headings = [(1, 0), (0, -1), (-1, 0), (0, 1)]  # E, N, W, S
    hard_time_limit = -100  # Set a hard time limit even if deadline is not enforced.

    def __init__(self, verbose=False, num_dummies=100, grid_size = (8, 6)):
        self.num_dummies = num_dummies  # Number of dummy driver agents in the environment
        self.verbose = verbose # If debug output should be given

        # Initialize simulation variables
        self.done = False
        self.t = 0
        self.agent_states = OrderedDict()
        self.step_data = {}
        self.success = None

        # Road network
        self.grid_size = grid_size  # (columns, rows)
        self.bounds = (1, 2, self.grid_size[0], self.grid_size[1] + 1)
        self.block_size = 100
        self.hang = 0.6
        self.intersections = OrderedDict()
        self.roads = []
        for x in xrange(self.bounds[0], self.bounds[2] + 1):
            for y in xrange(self.bounds[1], self.bounds[3] + 1):
                self.intersections[(x, y)] = TrafficLight()  # A traffic light at each intersection

        for a in self.intersections:
            for b in self.intersections:
                if a == b:
                    continue
                if (abs(a[0] - b[0]) + abs(a[1] - b[1])) == 1:  # L1 distance = 1
                    self.roads.append((a, b))

        # Add environment boundaries
        for x in xrange(self.bounds[0], self.bounds[2] + 1):
            self.roads.append(((x, self.bounds[1] - self.hang), (x, self.bounds[1])))
            self.roads.append(((x, self.bounds[3] + self.hang), (x, self.bounds[3])))
        for y in xrange(self.bounds[1], self.bounds[3] + 1):
            self.roads.append(((self.bounds[0] - self.hang, y), (self.bounds[0], y)))
            self.roads.append(((self.bounds[2] + self.hang, y), (self.bounds[2], y)))    

        # Create dummy agents
        for i in xrange(self.num_dummies):
            self.create_agent(DummyAgent)

        # Primary agent and associated parameters
        self.primary_agent = None  # to be set explicitly
        self.enforce_deadline = False

        # Trial data (updated at the end of each trial)
        self.trial_data = {
            'testing': False, # if the trial is for testing a learned policy
            'initial_distance': 0,  # L1 distance from start to destination
            'initial_deadline': 0,  # given deadline (time steps) to start with
            'net_reward': 0.0,  # total reward earned in current trial
            'final_deadline': None,  # deadline value (time remaining) at the end
            'actions': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}, # violations and accidents
            'success': 0  # whether the agent reached the destination in time
        }

    def create_agent(self, agent_class, *args, **kwargs):
        """ When called, create_agent creates an agent in the environment. """

        agent = agent_class(self, *args, **kwargs)
        self.agent_states[agent] = {'location': random.choice(self.intersections.keys()), 'heading': (0, 1)}
        return agent

    def set_primary_agent(self, agent, enforce_deadline=False):
        """ When called, set_primary_agent sets 'agent' as the primary agent.
            The primary agent is the smartcab that is followed in the environment. """

        self.primary_agent = agent
        agent.primary_agent = True
        self.enforce_deadline = enforce_deadline

    def reset(self, testing=False):
        """ This function is called at the beginning of a new trial. """

        self.done = False
        self.t = 0

        # Reset status text
        self.step_data = {}

        # Reset traffic lights
        for traffic_light in self.intersections.itervalues():
            traffic_light.reset()

        # Pick a start and a destination
        start = random.choice(self.intersections.keys())
        destination = random.choice(self.intersections.keys())

        # Ensure starting location and destination are not too close
        while self.compute_dist(start, destination) < 4:
            start = random.choice(self.intersections.keys())
            destination = random.choice(self.intersections.keys())

        start_heading = random.choice(self.valid_headings)
        distance = self.compute_dist(start, destination)
        deadline = distance * 5 # 5 time steps per intersection away
        if(self.verbose == True): # Debugging
            print "Environment.reset(): Trial set up with start = {}, destination = {}, deadline = {}".format(start, destination, deadline)

        # Create a map of all possible initial positions
        positions = dict()
        for location in self.intersections:
            positions[location] = list()
            for heading in self.valid_headings:
                positions[location].append(heading)

        # Initialize agent(s)
        for agent in self.agent_states.iterkeys():

            if agent is self.primary_agent:
                self.agent_states[agent] = {
                    'location': start,
                    'heading': start_heading,
                    'destination': destination,
                    'deadline': deadline
                }
            # For dummy agents, make them choose one of the available 
            # intersections and headings still in 'positions'
            else:
                intersection = random.choice(positions.keys())
                heading = random.choice(positions[intersection])
                self.agent_states[agent] = {
                    'location': intersection,
                    'heading': heading,
                    'destination': None,
                    'deadline': None
                }
                # Now delete the taken location and heading from 'positions'
                positions[intersection] = list(set(positions[intersection]) - set([heading]))
                if positions[intersection] == list(): # No headings available for intersection
                    del positions[intersection] # Delete the intersection altogether

    
            agent.reset(destination=(destination if agent is self.primary_agent else None), testing=testing)
            if agent is self.primary_agent:
                # Reset metrics for this trial (step data will be set during the step)
                self.trial_data['testing'] = testing
                self.trial_data['initial_deadline'] = deadline
                self.trial_data['final_deadline'] = deadline
                self.trial_data['net_reward'] = 0.0
                self.trial_data['actions'] = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
                self.trial_data['parameters'] = {'e': agent.epsilon, 'a': agent.alpha}
                self.trial_data['success'] = 0

    def step(self):
        """ This function is called when a time step is taken turing a trial. """

        # Pretty print to terminal
        print ""
        print "/-------------------"
        print "| Step {} Results".format(self.t)
        print "\-------------------"
        print ""

        if(self.verbose == True): # Debugging
            print "Environment.step(): t = {}".format(self.t)

        # Update agents, primary first
        if self.primary_agent is not None:
            self.primary_agent.update()

        for agent in self.agent_states.iterkeys():
            if agent is not self.primary_agent:
                agent.update()

        # Update traffic lights
        for intersection, traffic_light in self.intersections.iteritems():
            traffic_light.update(self.t)

        if self.primary_agent is not None:
            # Agent has taken an action: reduce the deadline by 1
            agent_deadline = self.agent_states[self.primary_agent]['deadline'] - 1
            self.agent_states[self.primary_agent]['deadline'] = agent_deadline

            if agent_deadline <= self.hard_time_limit:
                self.done = True
                self.success = False
                if self.verbose: # Debugging
                    print "Environment.step(): Primary agent hit hard time limit ({})! Trial aborted.".format(self.hard_time_limit)
            elif self.enforce_deadline and agent_deadline <= 0:
                self.done = True
                self.success = False
                if self.verbose: # Debugging
                    print "Environment.step(): Primary agent ran out of time! Trial aborted."

        self.t += 1

    def sense(self, agent):
        """ This function is called when information is requested about the sensor
            inputs from an 'agent' in the environment. """

        assert agent in self.agent_states, "Unknown agent!"

        state = self.agent_states[agent]
        location = state['location']
        heading = state['heading']
        light = 'green' if (self.intersections[location].state and heading[1] != 0) or ((not self.intersections[location].state) and heading[0] != 0) else 'red'

        # Populate oncoming, left, right
        oncoming = None
        left = None
        right = None
        for other_agent, other_state in self.agent_states.iteritems():
            if agent == other_agent or location != other_state['location'] or (heading[0] == other_state['heading'][0] and heading[1] == other_state['heading'][1]):
                continue
            # For dummy agents, ignore the primary agent
            # This is because the primary agent is not required to follow the waypoint
            if other_agent == self.primary_agent:
                continue
            other_heading = other_agent.get_next_waypoint()
            if (heading[0] * other_state['heading'][0] + heading[1] * other_state['heading'][1]) == -1:
                if oncoming != 'left':  # we don't want to override oncoming == 'left'
                    oncoming = other_heading
            elif (heading[1] == other_state['heading'][0] and -heading[0] == other_state['heading'][1]):
                if right != 'forward' and right != 'left':  # we don't want to override right == 'forward or 'left'
                    right = other_heading
            else:
                if left != 'forward':  # we don't want to override left == 'forward'
                    left = other_heading

        return {'light': light, 'oncoming': oncoming, 'left': left, 'right': right}

    def get_deadline(self, agent):
        """ Returns the deadline remaining for an agent. """

        return self.agent_states[agent]['deadline'] if agent is self.primary_agent else None

    def act(self, agent, action):
        """ Consider an action and perform the action if it is legal.
            Receive a reward for the agent based on traffic laws. """

        assert agent in self.agent_states, "Unknown agent!"
        assert action in self.valid_actions, "Invalid action!"

        state = self.agent_states[agent]
        location = state['location']
        heading = state['heading']
        light = 'green' if (self.intersections[location].state and heading[1] != 0) or ((not self.intersections[location].state) and heading[0] != 0) else 'red'
        inputs = self.sense(agent)

        # Assess whether the agent can move based on the action chosen.
        # Either the action is okay to perform, or falls under 4 types of violations:
        # 0: Action okay
        # 1: Minor traffic violation
        # 2: Major traffic violation
        # 3: Minor traffic violation causing an accident
        # 4: Major traffic violation causing an accident
        violation = 0

        # Reward scheme
        # First initialize reward uniformly random from [-1, 1]
        reward = 2 * random.random() - 1

        # Create a penalty factor as a function of remaining deadline
        # Scales reward multiplicatively from [0, 1]
        fnc = self.t * 1.0 / (self.t + state['deadline']) if agent.primary_agent else 0.0
        gradient = 10
        
        # No penalty given to an agent that has no enforced deadline
        penalty = 0

        # If the deadline is enforced, give a penalty based on time remaining
        if self.enforce_deadline:
            penalty = (math.pow(gradient, fnc) - 1) / (gradient - 1)

        # Agent wants to drive forward:
        if action == 'forward':
            if light != 'green': # Running red light
                violation = 2 # Major violation
                if inputs['left'] == 'forward' or inputs['right'] == 'forward': # Cross traffic
                    violation = 4 # Accident
        
        # Agent wants to drive left:
        elif action == 'left':
            if light != 'green': # Running a red light
                violation = 2 # Major violation
                if inputs['left'] == 'forward' or inputs['right'] == 'forward': # Cross traffic
                    violation = 4 # Accident
                elif inputs['oncoming'] == 'right': # Oncoming car turning right
                    violation = 4 # Accident
            else:# Green light
                if inputs['oncoming'] == 'right' or inputs['oncoming'] == 'forward': # Incoming traffic
                    violation = 3 # Accident
                else: # Valid move!
                    heading = (heading[1], -heading[0])

        # Agent wants to drive right:
        elif action == 'right':
            if light != 'green' and inputs['left'] == 'forward': # Cross traffic
                violation = 3 # Accident
            else: # Valid move!
                heading = (-heading[1], heading[0])

        # Agent wants to perform no action:
        elif action == None:
            if light == 'green': 
                violation = 1 # Minor violation


        # Did the agent attempt a valid move?
        if violation == 0:
            if action == agent.get_next_waypoint(): # Was it the correct action?
                reward += 2 - penalty # (2, 1)
            elif action == None and light != 'green' and agent.get_next_waypoint() == 'right':
                # valid action but incorrect (idling at red light, when we should have gone right on red)
                reward += 1 - penalty # (1, 0)
            elif action == None and light != 'green': # Was the agent stuck at a red light?
                reward += 2 - penalty # (2, 1)
            else: # Valid but incorrect
                reward += 1 - penalty # (1, 0)

            # Move the agent
            if action is not None:
                location = ((location[0] + heading[0] - self.bounds[0]) % (self.bounds[2] - self.bounds[0] + 1) + self.bounds[0],
                            (location[1] + heading[1] - self.bounds[1]) % (self.bounds[3] - self.bounds[1] + 1) + self.bounds[1])  # wrap-around
                state['location'] = location
                state['heading'] = heading
        # Agent attempted invalid move
        else:
            if violation == 1: # Minor violation
                reward += -5
            elif violation == 2: # Major violation
                reward += -10
            elif violation == 3: # Minor accident
                reward += -20
            elif violation == 4: # Major accident
                reward += -40

        # Did agent reach the goal after a valid move?
        if agent is self.primary_agent:
            if state['location'] == state['destination']:
                # Did agent get to destination before deadline?
                if state['deadline'] >= 0:
                    self.trial_data['success'] = 1
                
                # Stop the trial
                self.done = True
                self.success = True

                if(self.verbose == True): # Debugging
                    print "Environment.act(): Primary agent has reached destination!"

            if(self.verbose == True): # Debugging
                print "Environment.act() [POST]: location: {}, heading: {}, action: {}, reward: {}".format(location, heading, action, reward)

            # Update metrics
            self.step_data['t'] = self.t
            self.step_data['violation'] = violation
            self.step_data['state'] = agent.get_state()
            self.step_data['deadline'] = state['deadline']
            self.step_data['waypoint'] = agent.get_next_waypoint()
            self.step_data['inputs'] = inputs
            self.step_data['light'] = light
            self.step_data['action'] = action
            self.step_data['reward'] = reward
            
            self.trial_data['final_deadline'] = state['deadline'] - 1
            self.trial_data['net_reward'] += reward
            self.trial_data['actions'][violation] += 1

            if(self.verbose == True): # Debugging
                print "Environment.act(): Step data: {}".format(self.step_data)
        return reward

    def compute_dist(self, a, b):
        """ Compute the Manhattan (L1) distance of a spherical world. """

        dx1 = abs(b[0] - a[0])
        dx2 = abs(self.grid_size[0] - dx1)
        dx = dx1 if dx1 < dx2 else dx2

        dy1 = abs(b[1] - a[1])
        dy2 = abs(self.
            grid_size[1] - dy1)
        dy = dy1 if dy1 < dy2 else dy2

        return dx + dy


class Agent(object):
    """Base class for all agents."""

    def __init__(self, env):
        self.env = env
        self.state = None
        self.next_waypoint = None
        self.color = 'white'
        self.primary_agent = False

    def reset(self, destination=None, testing=False):
        pass

    def update(self):
        pass

    def get_state(self):
        return self.state

    def get_next_waypoint(self):
        return self.next_waypoint  


class DummyAgent(Agent):
    color_choices = ['cyan', 'red', 'blue', 'green', 'orange', 'magenta', 'yellow']

    def __init__(self, env):
        super(DummyAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.next_waypoint = random.choice(Environment.valid_actions[1:])
        self.color = random.choice(self.color_choices)

    def update(self):
        """ Update a DummyAgent to move randomly under legal traffic laws. """

        inputs = self.env.sense(self)

        # Check if the chosen waypoint is safe to move to.
        action_okay = True
        if self.next_waypoint == 'right':
            if inputs['light'] == 'red' and inputs['left'] == 'forward':
                action_okay = False
        elif self.next_waypoint == 'forward':
            if inputs['light'] == 'red':
                action_okay = False
        elif self.next_waypoint == 'left':
            if inputs['light'] == 'red' or (inputs['oncoming'] == 'forward' or inputs['oncoming'] == 'right'):
                action_okay = False

        # Move to the next waypoint and choose a new one.
        action = None
        if action_okay:
            action = self.next_waypoint
            self.next_waypoint = random.choice(Environment.valid_actions[1:])
        reward = self.env.act(self, action)