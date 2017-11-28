import random

class RoutePlanner(object):
    """ Complex route planner that is meant for a perpendicular grid network. """

    def __init__(self, env, agent):
        self.env = env
        self.agent = agent
        self.destination = None

    def route_to(self, destination=None):
        """ Select the destination if one is provided, otherwise choose a random intersection. """

        self.destination = destination if destination is not None else random.choice(list(self.env.intersections.keys()))

    def next_waypoint(self):
        """ Creates the next waypoint based on current heading, location,
            intended destination and L1 distance from destination. """

        # Collect global location details
        bounds = self.env.grid_size
        location = self.env.agent_states[self.agent]['location']
        heading = self.env.agent_states[self.agent]['heading']

        delta_a = (self.destination[0] - location[0], self.destination[1] - location[1])
        delta_b = (bounds[0] + delta_a[0] if delta_a[0] <= 0 else delta_a[0] - bounds[0], \
                   bounds[1] + delta_a[1] if delta_a[1] <= 0 else delta_a[1] - bounds[1])

        # Calculate true difference in location based on world-wrap
        # This will pre-determine the need for U-turns from improper headings
        dx = delta_a[0] if abs(delta_a[0]) < abs(delta_b[0]) else delta_b[0]
        dy = delta_a[1] if abs(delta_a[1]) < abs(delta_b[1]) else delta_b[1]

        # First check if destination is at location
        if dx == 0 and dy == 0:
            return None
        
        # Next check if destination is cardinally East or West of location    
        elif dx != 0:

            if dx * heading[0] > 0:  # Heading the correct East or West direction
                return 'forward'
            elif dx * heading[0] < 0 and heading[0] < 0: # Heading West, destination East
                if dy > 0: # Destination also to the South
                    return 'left'
                else:
                    return 'right'
            elif dx * heading[0] < 0 and heading[0] > 0: # Heading East, destination West
                if dy < 0: # Destination also to the North
                    return 'left'
                else:
                    return 'right'
            elif dx * heading[1] > 0: # Heading North destination West; Heading South destination East
                return 'left'
            else:
                return 'right'

        # Finally, check if destination is cardinally North or South of location
        elif dy != 0:

            if dy * heading[1] > 0:  # Heading the correct North or South direction
                return 'forward'
            elif dy * heading[1] < 0 and heading[1] < 0: # Heading North, destination South
                if dx < 0: # Destination also to the West
                    return 'left'
                else:
                    return 'right'
            elif dy * heading[1] < 0 and heading[1] > 0: # Heading South, destination North
                if dx > 0: # Destination also to the East
                    return 'left'
                else:
                    return 'right'
            elif dy * heading[0] > 0: # Heading West destination North; Heading East destination South
                return 'right'
            else:
                return 'left'