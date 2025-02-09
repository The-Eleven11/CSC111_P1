"""CSC111 Project 1: Text Adventure Game - Simulator

Instructions (READ THIS FIRST!)
===============================

This Python module contains code for Project 1 that allows a user to simulate an entire
playthrough of the game. Please consult the project handout for instructions and details.

You can copy/paste your code from the ex1_simulation file into this one, and modify it as needed
to work with your game.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""
from __future__ import annotations
from proj1_event_logger import Event, EventList
from adventure import AdventureGame
from game_entities import Item, Location, Player


class AdventureGameSimulation:
    """A simulation of an adventure game playthrough.
    """
    # Private Instance Attributes:
    #   - _game: The AdventureGame instance that this simulation uses.
    #   - _events: A collection of the events to process during the simulation.
    _game: AdventureGame
    _events: EventList
    _player = Player

    # TODO: Copy/paste your code from ex1_simulation below, and make adjustments as needed
    def __init__(self, game_data_file: str, initial_location_id: int, commands: list[str], time: int) -> None:
        """Initialize a new game simulation based on the given game data, that runs through the given commands.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands at each associated location in the game
        """

        # TODO: Add first event (initial location, no previous command)
        # Hint: self._game.get_location() gives you back the current location

        # TODO: Generate the remaining events based on the commands and initial location
        # Hint: Call self.generate_events with the appropriate arguments
        self._player = Player(time)

        self._events = EventList()
        self._game = AdventureGame(game_data_file, initial_location_id, self._player)

        # Add first event (initial location, no previous command)
        # Hint: self._game.get_location() gives you back the current location
        initial_location = self._game.get_location()
        initial_event = Event(
            id_num=initial_location.id_num,
            description=initial_location.brief_description,
            player=self._player,
            next_command=None,
            next=None,
            prev=None
        )
        self._events.add_event(initial_event)
        # Generate the remaining events based on the commands and initial location
        # Hint: Call self.generate_events with the appropriate arguments
        self.generate_events(commands, initial_location)

    def generate_events(self, commands: list[str], current_location: Location) -> None:
        """Generate all events in this simulation.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands at each associated location in the game
        """

        # TODO: Complete this method as specified. For each command, generate the event and add
        #  it to self._events.
        # Hint: current_location.available_commands[command] will return the next location ID
        # which executing <command> while in <current_location_id> leads to
        for command in commands:
            if command.__contains__("go"):
                conditional_item = [x.name for x in self._game.player.inventory]
                target_location = self._game.get_location(current_location.available_commands[command])
                if all(item in conditional_item for item in target_location.items):
                    # move fit condition
                    current_location = target_location
                else:
                    # fail to move, no change in location
                    print("ops, you may need below items to move to this area")
                    print([item for item in current_location.items if item not in self._game.player.inventory])
            else:
                self._game.player.inventory.append(self._game.get_item(command[5:len(command)]))
            event = Event(current_location.id_num, current_location.brief_description, self._game.player)
            self._events.add_event(event, command)

    def get_id_log(self) -> list[int]:
        """
        Get back a list of all location IDs in the order that they are visited within a game simulation
        that follows the given commands.
        """

        # Note: We have completed this method for you. Do NOT modify it for ex1.

        return self._events.get_id_log()

    def run(self) -> None:
        """Run the game simulation and log location descriptions."""

        # Note: We have completed this method for you. Do NOT modify it for ex1.

        current_event = self._events.first  # Start from the first event in the list

        while current_event:
            print(current_event.description)
            if current_event is not self._events.last:
                print("You choose:", current_event.next_command)

            # Move to the next event in the linked list
            current_event = current_event.next

    def get_curr_inventory(self) -> list:
        """
        return inventory of player
        """
        return self._game.player.check_invertory()

    def get_curr_score(self) -> list:
        """
        return the current score
        """
        return [self._game.player.curr_score()]


if __name__ == "__main__":
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })

    # TODO: Modify the code below to provide a walkthrough of commands needed to win and lose the game
    win_walkthrough = ["go west", "pick csc111 syllabus", "go east", "go east", "go north", "go 1", "go north",
                       "go west", "go west", "go west", "go north", "take assignment extension"]
    # Create a list of all the commands needed to walk through your game to win it
    expected_log = [1, 3, 3, 1, 4, 6, 7, 8, 21, 22, 24, 25, 25]
    # Update this log list to include the IDs of all locations that would be visited
    # Uncomment the line below to test your walkthrough
    assert expected_log == AdventureGameSimulation('game_data.json', 1, win_walkthrough,
                                                   60).get_id_log()

    # Create a list of all the commands needed to walk through your game to reach a 'game over' state
    lose_demo = ["go west", "go east", "go west", "go east", "go west"]
    expected_log = [1, 3, 1, 3, 1, 3]  # Update this log list to include the IDs of all locations that would be visited
    # Uncomment the line below to test your demo
    assert expected_log == AdventureGameSimulation('game_data.json', 1, lose_demo,
                                                   5).get_id_log()

    # TODO: Add code below to provide walkthroughs that show off certain features of the game
    # TODO: Create a list of commands involving visiting locations, picking up items, and then
    #   checking the inventory, your list must include the "inventory" command at least once
    inventory_demo = ['go west', 'pick t-card']
    expected_log = [Item(name='t-card', target_points=5)]
    assert expected_log == AdventureGameSimulation('game_data.json', 1, inventory_demo,
                                                   5).get_curr_inventory()

    scores_demo = ['go west', 'pick t-card']
    expected_log = [5]
    assert expected_log == AdventureGameSimulation('game_data.json', 1, scores_demo,
                                                   5).get_curr_score()

    # Add more enhancement_demos if you have more enhancements
    enhancement1_demo = ['go east', 'go north', 'go 1', 'go north', 'go east', 'go east', 'go east']
    # generate will meet a place that cannot be access unless player have certain item
    expected_log = [1, 4, 6, 7, 8, 9, 10, 10]
    assert expected_log == AdventureGameSimulation('game_data.json', 1, enhancement1_demo,
                                                   5).get_id_log()

    # Note: You can add more code below for your own testing purposes
