"""CSC111 Project 1: Text Adventure Game - Game Manager

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

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
import json
from typing import Optional

from game_entities import Location, Item, Player
from proj1_event_logger import Event, EventList


# Note: You may add in other import statements here as needed

# Note: You may add helper functions, classes, etc. below as needed


class AdventureGame:
    """A text adventure game class storing all location, item and map data.

    Instance Attributes:
    - _locations: every locations of game, the map
    - _items: conditional items that is needed to access this area
    - current_location_id: the location you are in in this step
    - ongoing: whether this game is continue
    - player: the information of player in this step
    Representation Invariants:
    - # TODO add any appropriate representation invariants as needed
    """

    # Private Instance Attributes (do NOT remove these two attributes):
    #   - _locations: a mapping from location id to Location object.
    #                       This represents all the locations in the game.
    #   - _items: a list of Item objects, representing all items in the game.

    _locations: dict[int, Location]
    _items: list[Item]
    current_location_id: int  # Suggested attribute, can be removed
    ongoing: bool  # Suggested attribute, can be removed
    player: Player

    def __init__(self, game_data_file: str, initial_location_id: int, player: Player) -> None:
        """
        Initialize a new text adventure game, based on the data in the given file, setting starting location of game
        at the given initial location ID.
        (note: you are allowed to modify the format of the file as you see fit)

        Preconditions:
        - game_data_file is the filename of a valid game data JSON file
        """

        # NOTES:
        # You may add parameters/attributes/methods to this class as you see fit.

        # Requirements:
        # 1. Make sure the Location class is used to represent each location.
        # 2. Make sure the Item class is used to represent each item.

        # Suggested helper method (you can remove and load these differently if you wish to do so):
        self._locations, self._items = self._load_game_data(game_data_file)

        # Suggested attributes (you can remove and track these differently if you wish to do so):
        self.current_location_id = initial_location_id  # game begins at this location
        self.ongoing = True  # whether the game is ongoing
        self.player = player  # player obj in game

    @staticmethod
    def _load_game_data(filename: str) -> tuple[dict[int, Location], list[Item]]:
        """Load locations and items from a JSON file with the given filename and
        return a tuple consisting of (1) a dictionary of locations mapping each game location's ID to a Location object,
        and (2) a list of all Item objects."""

        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        locations = {}
        for loc_data in data['locations']:  # Go through each element associated with the 'locations' key in the file
            location_obj = Location(loc_data['id'], loc_data['brief_description'], loc_data['long_description'],
                                    loc_data['available_commands'], loc_data['items'])
            locations[loc_data['id']] = location_obj

        items = []
        # TODO: Add Item objects to the items list; your code should be structured similarly to the loop above
        # YOUR CODE BELOW
        for loc_data in data['items']:
            item_obj = Item(loc_data['name'], loc_data['target_points'])
            items.append(item_obj)
        # Load items done
        return locations, items

    def get_location(self, loc_id: Optional[int] = None) -> Location:
        """Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the current location.
        """

        # TODO: Complete this method as specified
        # YOUR CODE BELOW
        if loc_id is None:
            return self._locations[self.current_location_id]
        else:
            return self._locations[loc_id]

    def get_item(self, item_name: str) -> item:
        """
        return items whose name is item_name, return "" if not found
        """
        for item in self._items:
            if item.name == item_name:
                return item
        return ""


if __name__ == "__main__":

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })

    # game flow and logic
    # 1 initiate every information and game itself
    # default time provided: 200    ***
    time = 200
    curr_time = 0
    player = Player(time)

    game_log = EventList()  # This is REQUIRED as one of the baseline requirements
    game = AdventureGame('game_data.json', 1, player)  # load data, setting initial location ID to 1
    menu = ["look", "inventory", "score", "undo", "log", "quit"]  # Regular menu options available at each location
    choice = None

    # Note: You may modify the code below as needed; the following starter code is just a suggestion
    while game.ongoing:
        # Note: If the loop body is getting too long, you should split the body up into helper functions
        # for better organization. Part of your marks will be based on how well-organized your code is.

        location = game.get_location(game.current_location_id)

        # TODO: Add new Event to game log to represent current game location
        #  Note that the <choice> variable should be the command which led to this event
        # YOUR CODE HERE
        event = Event(location.id_num, location.brief_description, game.player)
        game_log.add_event(event)
        # TODO: Depending on whether or not it's been visited before,
        #  print either full description (first time visit) or brief description (every subsequent visit) of location
        # YOUR CODE HERE
        if location.visited:
            print(location.brief_description)
        else:
            print(location.long_description)
            location.visited = True

        # Display possible actions at this location
        print("What to do? Choose from: look, inventory, score, undo, log, quit")
        print("At this location, you can also:")
        for action in location.available_commands:
            print("-", action)

        # Validate choice
        choice = input("\nEnter action: ").lower().strip()
        while choice not in location.available_commands and choice not in menu:
            print("That was an invalid option; try again.")
            choice = input("\nEnter action: ").lower().strip()

        print("========")
        print("You decided to:", choice)

        if choice in menu:
            # TODO: Handle each menu command as appropriate
            # Note: For the "undo" command, remember to manipulate the game_log event list to keep it up-to-date
            if choice == "log":
                print("user command: log")
                game_log.display_events()
            # ENTER YOUR CODE BELOW to handle other menu commands (remember to use helper functions as appropriate)
            if choice == 'look':
                print("user command: look")
                print(location.long_description)
            if choice == 'inventory':
                print("user command: inventory")
                print(game.player.inventory)
            if choice == 'score':
                print("user command: score")
                print(game.player.curr_score())
            if choice == 'undo':
                if curr_time == 0:
                    # must have at least one step done
                    print("Error: there is no more step made")
                else:
                    print("User command: undo")
                    game_log.remove_last_event()
                    game.current_location_id = game_log.get_id_log()[-1]
                    game.player = game_log.last.player
                    curr_time -= 1
            if choice == 'quit':
                print("user command: quit, game is ended")
                print("final score gained:" + str(game.player.curr_score()))
                exit()
        else:
            # Handle non-menu actions
            # TODO: Add in code to deal with special locations (e.g. puzzles) as needed for your game
            if choice.__contains__("go"):
                if all(item in game.player.inventory for item in location.items):
                    # move fit condition
                    result = location.available_commands[choice]
                    game.current_location_id = result
                else:
                    # fail to move, no change in location
                    print("ops, you may need below items to move to this area")
                    print([item for item in location.items if item not in game.player.inventory])
            # TODO: Add in code to deal with actions which do not change the location (e.g. taking or using an item)
            else:
                game.player.inventory.add(game.get_item(choice[5:len(choice)]))
            curr_time += 1
            print()
            # related to go some places
        game.ongoing = not game.player.check_win()
        if curr_time > time:
            game.ongoing = False

    # ending: print score of game
    print("you win this game!" if game.player.check_win() else "you lose, try next time")
    print(game.player.final_score(curr_time))
