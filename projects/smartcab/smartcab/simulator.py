###########################################
# Suppress matplotlib user warnings
# Necessary for newer version of matplotlib
import warnings
warnings.filterwarnings("ignore", category = UserWarning, module = "matplotlib")
###########################################

import os
import time
import random
import importlib
import csv

class Simulator(object):
    """Simulates agents in a dynamic smartcab environment.

    Uses PyGame to display GUI, if available.
    """

    colors = {
        'black'   : (  0,   0,   0),
        'white'   : (255, 255, 255),
        'red'     : (255,   0,   0),
        'green'   : (  0, 255,   0),
        'dgreen'  : (  0, 228,   0),
        'blue'    : (  0,   0, 255),
        'cyan'    : (  0, 200, 200),
        'magenta' : (200,   0, 200),
        'yellow'  : (255, 255,   0),
        'mustard' : (200, 200,   0),
        'orange'  : (255, 128,   0),
        'maroon'  : (200,   0,   0),
        'crimson' : (128,   0,   0),
        'gray'    : (155, 155, 155)
    }

    def __init__(self, env, size=None, update_delay=2.0, display=True, log_metrics=False, optimized=False):
        self.env = env
        self.size = size if size is not None else ((self.env.grid_size[0] + 1) * self.env.block_size, (self.env.grid_size[1] + 2) * self.env.block_size)
        self.width, self.height = self.size
        self.road_width = 44

        self.bg_color = self.colors['gray']
        self.road_color = self.colors['black']
        self.line_color = self.colors['mustard']
        self.boundary = self.colors['black']
        self.stop_color = self.colors['crimson']

        self.quit = False
        self.start_time = None
        self.current_time = 0.0
        self.last_updated = 0.0
        self.update_delay = update_delay  # duration between each step (in seconds)

        self.display = display
        if self.display:
            try:
                self.pygame = importlib.import_module('pygame')
                self.pygame.init()
                self.screen = self.pygame.display.set_mode(self.size)
                self._logo = self.pygame.transform.smoothscale(self.pygame.image.load(os.path.join("images", "logo.png")), (self.road_width, self.road_width))

                self._ew = self.pygame.transform.smoothscale(self.pygame.image.load(os.path.join("images", "east-west.png")), (self.road_width, self.road_width))
                self._ns = self.pygame.transform.smoothscale(self.pygame.image.load(os.path.join("images", "north-south.png")), (self.road_width, self.road_width))

                self.frame_delay = max(1, int(self.update_delay * 1000))  # delay between GUI frames in ms (min: 1)
                self.agent_sprite_size = (32, 32)
                self.primary_agent_sprite_size = (42, 42)
                self.agent_circle_radius = 20  # radius of circle, when using simple representation
                for agent in self.env.agent_states:
                    if agent.color == 'white':
                        agent._sprite = self.pygame.transform.smoothscale(self.pygame.image.load(os.path.join("images", "car-{}.png".format(agent.color))), self.primary_agent_sprite_size)
                    else:
                        agent._sprite = self.pygame.transform.smoothscale(self.pygame.image.load(os.path.join("images", "car-{}.png".format(agent.color))), self.agent_sprite_size)
                    agent._sprite_size = (agent._sprite.get_width(), agent._sprite.get_height())

                self.font = self.pygame.font.Font(None, 20)
                self.paused = False
            except ImportError as e:
                self.display = False
                print "Simulator.__init__(): Unable to import pygame; display disabled.\n{}: {}".format(e.__class__.__name__, e)
            except Exception as e:
                self.display = False
                print "Simulator.__init__(): Error initializing GUI objects; display disabled.\n{}: {}".format(e.__class__.__name__, e)

        # Setup metrics to report
        self.log_metrics = log_metrics
        self.optimized = optimized
        
        if self.log_metrics:
            a = self.env.primary_agent

            # Set log files
            if a.learning:
                if self.optimized: # Whether the user is optimizing the parameters and decay functions
                    self.log_filename = os.path.join("logs", "sim_improved-learning.csv")
                    self.table_filename = os.path.join("logs","sim_improved-learning.txt")
                else: 
                    self.log_filename = os.path.join("logs", "sim_default-learning.csv")
                    self.table_filename = os.path.join("logs","sim_default-learning.txt")

                self.table_file = open(self.table_filename, 'wb')
            else:
                self.log_filename = os.path.join("logs", "sim_no-learning.csv")
            
            self.log_fields = ['trial', 'testing', 'parameters', 'initial_deadline', 'final_deadline', 'net_reward', 'actions', 'success']
            self.log_file = open(self.log_filename, 'wb')
            self.log_writer = csv.DictWriter(self.log_file, fieldnames=self.log_fields)
            self.log_writer.writeheader()

    def run(self, tolerance=0.05, n_test=0):
        """ Run a simulation of the environment. 

        'tolerance' is the minimum epsilon necessary to begin testing (if enabled)
        'n_test' is the number of testing trials simulated

        Note that the minimum number of training trials is always 20. """

        self.quit = False

        # Get the primary agent
        a = self.env.primary_agent

        total_trials = 1
        testing = False
        trial = 1

        while True:

            # Flip testing switch
            if not testing:
                if total_trials > 20: # Must complete minimum 20 training trials
                    if a.learning:
                        if a.epsilon < tolerance: # assumes epsilon decays to 0
                            testing = True
                            trial = 1
                    else:
                        testing = True
                        trial = 1
                        
            # Break if we've reached the limit of testing trials
            else:
                if trial > n_test:
                    break

            # Pretty print to terminal
            print 
            print "/-------------------------"
            if testing:
                print "| Testing trial {}".format(trial)
            else:
                print "| Training trial {}".format(trial)

            print "\-------------------------"
            print 

            self.env.reset(testing)
            self.current_time = 0.0
            self.last_updated = 0.0
            self.start_time = time.time()
            while True:
                try:
                    # Update current time
                    self.current_time = time.time() - self.start_time

                    # Handle GUI events
                    if self.display:
                        for event in self.pygame.event.get():
                            if event.type == self.pygame.QUIT:
                                self.quit = True
                            elif event.type == self.pygame.KEYDOWN:
                                if event.key == 27:  # Esc
                                    self.quit = True
                                elif event.unicode == u' ':
                                    self.paused = True

                        if self.paused:
                            self.pause()

                    # Update environment
                    if self.current_time - self.last_updated >= self.update_delay:
                        self.env.step()
                        self.last_updated = self.current_time
                    
                    # Render text
                    self.render_text(trial, testing)

                    # Render GUI and sleep
                    if self.display:
                        self.render(trial, testing)
                        self.pygame.time.wait(self.frame_delay)

                except KeyboardInterrupt:
                    self.quit = True
                finally:
                    if self.quit or self.env.done:
                        break

            if self.quit:
                break

            # Collect metrics from trial
            if self.log_metrics:
                self.log_writer.writerow({
                    'trial': trial,
                    'testing': self.env.trial_data['testing'],
                    'parameters': self.env.trial_data['parameters'],
                    'initial_deadline': self.env.trial_data['initial_deadline'],
                    'final_deadline': self.env.trial_data['final_deadline'],
                    'net_reward': self.env.trial_data['net_reward'],
                    'actions': self.env.trial_data['actions'],
                    'success': self.env.trial_data['success']
                })

            # Trial finished
            if self.env.success == True:
                print "\nTrial Completed!"
                print "Agent reached the destination."
            else:
                print "\nTrial Aborted!"
                print "Agent did not reach the destination."

            # Increment
            total_trials = total_trials + 1
            trial = trial + 1

        # Clean up
        if self.log_metrics:

            if a.learning:
                f = self.table_file
                
                f.write("/-----------------------------------------\n")
                f.write("| State-action rewards from Q-Learning\n")
                f.write("\-----------------------------------------\n\n")

                for state in a.Q:
                    f.write("{}\n".format(state))
                    for action, reward in a.Q[state].iteritems():
                        f.write(" -- {} : {:.2f}\n".format(action, reward))
                    f.write("\n")  
                self.table_file.close()

            self.log_file.close()

        print "\nSimulation ended. . . "

        # Report final metrics
        if self.display:
            self.pygame.display.quit()  # shut down pygame

    def render_text(self, trial, testing=False):
        """ This is the non-GUI render display of the simulation. 
            Simulated trial data will be rendered in the terminal/command prompt. """

        status = self.env.step_data
        if status and status['waypoint'] is not None: # Continuing the trial

            # Previous State
            if status['state']:
                print "Agent previous state: {}".format(status['state'])
            else:
                print "!! Agent state not been updated!"

            # Result
            if status['violation'] == 0: # Legal
                if status['waypoint'] == status['action']: # Followed waypoint
                    print "Agent followed the waypoint {}. (rewarded {:.2f})".format(status['action'], status['reward'])
                elif status['action'] == None:
                    if status['light'] == 'red': # Stuck at red light
                        print "Agent properly idled at a red light. (rewarded {:.2f})".format(status['reward'])
                    else:
                        print "Agent idled at a green light with oncoming traffic. (rewarded {:.2f})".format(status['reward'])
                else: # Did not follow waypoint
                    print "Agent drove {} instead of {}. (rewarded {:.2f})".format(status['action'], status['waypoint'], status['reward'])
            else: # Illegal
                if status['violation'] == 1: # Minor violation
                    print "Agent idled at a green light with no oncoming traffic. (rewarded {:.2f})".format(status['reward'])
                elif status['violation'] == 2: # Major violation
                    print "Agent attempted driving {} through a red light. (rewarded {:.2f})".format(status['action'], status['reward'])
                elif status['violation'] == 3: # Minor accident
                    print "Agent attempted driving {} through traffic and cause a minor accident. (rewarded {:.2f})".format(status['action'], status['reward'])
                elif status['violation'] == 4: # Major accident
                    print "Agent attempted driving {} through a red light with traffic and cause a major accident. (rewarded {:.2f})".format(status['action'], status['reward'])
           
            # Time Remaining
            if self.env.enforce_deadline:
                time = (status['deadline'] - 1) * 100.0 / (status['t'] + status['deadline'])
                print "{:.0f}% of time remaining to reach destination.".format(time)
            else:
                print "Agent not enforced to meet deadline."

        # Starting new trial
        else:
            a = self.env.primary_agent
            print "Simulating trial. . . "
            if a.learning:
                print "epsilon = {:.4f}; alpha = {:.4f}".format(a.epsilon, a.alpha)
            else:
                print "Agent not set to learn."

                
    def render(self, trial, testing=False):
        """ This is the GUI render display of the simulation. 
            Supplementary trial data can be found from render_text. """
        
        # Reset the screen.
        self.screen.fill(self.bg_color)

        # Draw elements
        # * Static elements

        # Boundary
        self.pygame.draw.rect(self.screen, self.boundary, ((self.env.bounds[0] - self.env.hang)*self.env.block_size, (self.env.bounds[1]-self.env.hang)*self.env.block_size, (self.env.bounds[2] + self.env.hang/3)*self.env.block_size, (self.env.bounds[3] - 1 + self.env.hang/3)*self.env.block_size), 4)
        
        for road in self.env.roads:
            # Road
            self.pygame.draw.line(self.screen, self.road_color, (road[0][0] * self.env.block_size, road[0][1] * self.env.block_size), (road[1][0] * self.env.block_size, road[1][1] * self.env.block_size), self.road_width)
            # Center line
            self.pygame.draw.line(self.screen, self.line_color, (road[0][0] * self.env.block_size, road[0][1] * self.env.block_size), (road[1][0] * self.env.block_size, road[1][1] * self.env.block_size), 2)
        
        for intersection, traffic_light in self.env.intersections.iteritems():
            self.pygame.draw.circle(self.screen, self.road_color, (intersection[0] * self.env.block_size, intersection[1] * self.env.block_size), self.road_width/2)
            
            if traffic_light.state: # North-South is open
                self.screen.blit(self._ns,
                    self.pygame.rect.Rect(intersection[0]*self.env.block_size - self.road_width/2, intersection[1]*self.env.block_size - self.road_width/2, intersection[0]*self.env.block_size + self.road_width, intersection[1]*self.env.block_size + self.road_width/2))
                self.pygame.draw.line(self.screen, self.stop_color, (intersection[0] * self.env.block_size - self.road_width/2, intersection[1] * self.env.block_size - self.road_width/2), (intersection[0] * self.env.block_size - self.road_width/2, intersection[1] * self.env.block_size + self.road_width/2), 2)
                self.pygame.draw.line(self.screen, self.stop_color, (intersection[0] * self.env.block_size + self.road_width/2 + 1, intersection[1] * self.env.block_size - self.road_width/2), (intersection[0] * self.env.block_size + self.road_width/2 + 1, intersection[1] * self.env.block_size + self.road_width/2), 2)            
            else:
                self.screen.blit(self._ew,
                    self.pygame.rect.Rect(intersection[0]*self.env.block_size - self.road_width/2, intersection[1]*self.env.block_size - self.road_width/2, intersection[0]*self.env.block_size + self.road_width, intersection[1]*self.env.block_size + self.road_width/2))
                self.pygame.draw.line(self.screen, self.stop_color, (intersection[0] * self.env.block_size - self.road_width/2, intersection[1] * self.env.block_size - self.road_width/2), (intersection[0] * self.env.block_size + self.road_width/2, intersection[1] * self.env.block_size - self.road_width/2), 2)
                self.pygame.draw.line(self.screen, self.stop_color, (intersection[0] * self.env.block_size + self.road_width/2, intersection[1] * self.env.block_size + self.road_width/2 + 1), (intersection[0] * self.env.block_size - self.road_width/2, intersection[1] * self.env.block_size + self.road_width/2 + 1), 2)            
            
        # * Dynamic elements
        self.font = self.pygame.font.Font(None, 20)
        for agent, state in self.env.agent_states.iteritems():
            # Compute precise agent location here (back from the intersection some)
            agent_offset = (2 * state['heading'][0] * self.agent_circle_radius + self.agent_circle_radius * state['heading'][1] * 0.5, \
                            2 * state['heading'][1] * self.agent_circle_radius - self.agent_circle_radius * state['heading'][0] * 0.5)


            agent_pos = (state['location'][0] * self.env.block_size - agent_offset[0], state['location'][1] * self.env.block_size - agent_offset[1])
            agent_color = self.colors[agent.color]

            if hasattr(agent, '_sprite') and agent._sprite is not None:
                # Draw agent sprite (image), properly rotated
                rotated_sprite = agent._sprite if state['heading'] == (1, 0) else self.pygame.transform.rotate(agent._sprite, 180 if state['heading'][0] == -1 else state['heading'][1] * -90)
                self.screen.blit(rotated_sprite,
                    self.pygame.rect.Rect(agent_pos[0] - agent._sprite_size[0] / 2, agent_pos[1] - agent._sprite_size[1] / 2,
                        agent._sprite_size[0], agent._sprite_size[1]))
            else:
                # Draw simple agent (circle with a short line segment poking out to indicate heading)
                self.pygame.draw.circle(self.screen, agent_color, agent_pos, self.agent_circle_radius)
                self.pygame.draw.line(self.screen, agent_color, agent_pos, state['location'], self.road_width)
            

            if state['destination'] is not None:
                self.screen.blit(self._logo,
                    self.pygame.rect.Rect(state['destination'][0] * self.env.block_size - self.road_width/2, \
                        state['destination'][1]*self.env.block_size - self.road_width/2, \
                        state['destination'][0]*self.env.block_size + self.road_width/2, \
                        state['destination'][1]*self.env.block_size + self.road_width/2))

        # * Overlays
        self.font = self.pygame.font.Font(None, 50)
        if testing:
            self.screen.blit(self.font.render("Testing Trial %s"%(trial), True, self.colors['black'], self.bg_color), (10, 10))
        else:
            self.screen.blit(self.font.render("Training Trial %s"%(trial), True, self.colors['black'], self.bg_color), (10, 10))

        self.font = self.pygame.font.Font(None, 30)

        # Status text about each step
        status = self.env.step_data
        if status:

            # Previous State
            if status['state']:
                self.screen.blit(self.font.render("Previous State: {}".format(status['state']), True, self.colors['white'], self.bg_color), (350, 10))
            if not status['state']:
                self.screen.blit(self.font.render("!! Agent state not updated!", True, self.colors['maroon'], self.bg_color), (350, 10))

            # Action
            if status['violation'] == 0: # Legal
                if status['action'] == None:
                    self.screen.blit(self.font.render("No action taken. (rewarded {:.2f})".format(status['reward']), True, self.colors['dgreen'], self.bg_color), (350, 40))
                else:
                    self.screen.blit(self.font.render("Agent drove {}. (rewarded {:.2f})".format(status['action'], status['reward']), True, self.colors['dgreen'], self.bg_color), (350, 40))
            else: # Illegal
                if status['action'] == None:
                    self.screen.blit(self.font.render("No action taken. (rewarded {:.2f})".format(status['reward']), True, self.colors['maroon'], self.bg_color), (350, 40))
                else:
                    self.screen.blit(self.font.render("{} attempted (rewarded {:.2f})".format(status['action'], status['reward']), True, self.colors['maroon'], self.bg_color), (350, 40))

            # Result
            if status['violation'] == 0: # Legal
                if status['waypoint'] == status['action']: # Followed waypoint
                    self.screen.blit(self.font.render("Agent followed the waypoint!", True, self.colors['dgreen'], self.bg_color), (350, 70))
                elif status['action'] == None:
                    if status['light'] == 'red': # Stuck at a red light
                        self.screen.blit(self.font.render("Agent idled at a red light!", True, self.colors['dgreen'], self.bg_color), (350, 70))
                    else:
                        self.screen.blit(self.font.render("Agent idled at a green light with oncoming traffic.", True, self.colors['mustard'], self.bg_color), (350, 70))
                else: # Did not follow waypoint
                    self.screen.blit(self.font.render("Agent did not follow the waypoint.", True, self.colors['mustard'], self.bg_color), (350, 70))
            else: # Illegal
                if status['violation'] == 1: # Minor violation
                    self.screen.blit(self.font.render("There was a green light with no oncoming traffic.", True, self.colors['maroon'], self.bg_color), (350, 70))
                elif status['violation'] == 2: # Major violation
                    self.screen.blit(self.font.render("There was a red light with no traffic.", True, self.colors['maroon'], self.bg_color), (350, 70))
                elif status['violation'] == 3: # Minor accident
                    self.screen.blit(self.font.render("There was traffic with right-of-way.", True, self.colors['maroon'], self.bg_color), (350, 70))
                elif status['violation'] == 4: # Major accident
                    self.screen.blit(self.font.render("There was a red light with traffic.", True, self.colors['maroon'], self.bg_color), (350, 70))

            # Time Remaining
            if self.env.enforce_deadline:
                time = (status['deadline'] - 1) * 100.0 / (status['t'] + status['deadline'])
                self.screen.blit(self.font.render("{:.0f}% of time remaining to reach destination.".format(time), True, self.colors['black'], self.bg_color), (350, 100))
            else:
                self.screen.blit(self.font.render("Agent not enforced to meet deadline.", True, self.colors['black'], self.bg_color), (350, 100))
            
            # Denote whether a trial was a success or failure
            if (state['destination'] != state['location'] and state['deadline'] > 0) or (self.env.enforce_deadline is not True and state['destination'] != state['location']):
                self.font = self.pygame.font.Font(None, 40)
                if self.env.success == True:
                    self.screen.blit(self.font.render("Previous Trial: Success", True, self.colors['dgreen'], self.bg_color), (10, 50))
                if self.env.success == False:
                    self.screen.blit(self.font.render("Previous Trial: Failure", True, self.colors['maroon'], self.bg_color), (10, 50))

                if self.env.primary_agent.learning:
                    self.font = self.pygame.font.Font(None, 22)
                    self.screen.blit(self.font.render("epsilon = {:.4f}".format(self.env.primary_agent.epsilon), True, self.colors['black'], self.bg_color), (10, 80))
                    self.screen.blit(self.font.render("alpha = {:.4f}".format(self.env.primary_agent.alpha), True, self.colors['black'], self.bg_color), (10, 95))

        # Reset status text
        else:
            self.pygame.rect.Rect(350, 10, self.width, 200)
            self.font = self.pygame.font.Font(None, 40)
            self.screen.blit(self.font.render("Simulating trial. . .", True, self.colors['white'], self.bg_color), (400, 60))


        # Flip buffers
        self.pygame.display.flip()

    def pause(self):
        """ When the GUI is enabled, this function will pause the simulation. """
        
        abs_pause_time = time.time()
        self.font = self.pygame.font.Font(None, 30)
        pause_text = "Simulation Paused. Press any key to continue. . ."
        self.screen.blit(self.font.render(pause_text, True, self.colors['red'], self.bg_color), (400, self.height - 30))
        self.pygame.display.flip()
        print pause_text
        while self.paused:
            for event in self.pygame.event.get():
                if event.type == self.pygame.KEYDOWN:
                    self.paused = False
            self.pygame.time.wait(self.frame_delay)
        self.screen.blit(self.font.render(pause_text, True, self.bg_color, self.bg_color), (400, self.height - 30))
        self.start_time += (time.time() - abs_pause_time)
