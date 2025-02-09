"""CSC111 Project 1: Text Adventure Game - Game Entities

Instructions (READ THIS FIRST!)
===============================

This Python module contains the entity classes for Project 1, to be imported and used by
 the `adventure` module.
 Please consult the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Location:
    """A location in our text adventure game world.

    Instance Attributes:
    - id_num: id of location
    - brief_description: brief description of location
    - long_description: complete description of location
    - available commands: a dictionary of commands that is available in this location
    - items: items that can be found/interact in this location
    - visited: whether this location is arrived

    Representation Invariants:
    - self.id_num > 0
    - self.brief_description != ""
    - self.long_description != ""
    - len(self.available commands) > 0

    """

    # This is just a suggested starter class for Location.
    # You may change/add parameters and the data available for each Location object as you see fit.
    #
    # The only thing you must NOT change is the name of this class: Location.
    # All locations in your game MUST be represented as an instance of this class.
    id_num: int
    brief_description: str
    long_description: str
    available_commands: dict[str, int]
    items: list
    visited: bool

    def __init__(self, location_id, brief_description, long_description, available_commands, items,
                 visited=False) -> None:
        """Initialize a new location.

        # TODO Add more details here about the initialization if needed
        """

        self.id_num = location_id
        self.brief_description = brief_description
        self.long_description = long_description
        self.available_commands = available_commands
        self.items = items
        self.visited = visited


@dataclass
class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - # TODO Describe each instance attribute here

    Representation Invariants:
        - # TODO
    """

    # NOTES:
    # This is just a suggested starter class for Item.
    # You may change these parameters and the data available for each Item object as you see fit.
    # (The current parameters correspond to the example in the handout).
    #
    # The only thing you must NOT change is the name of this class: Item.
    # All item objects in your game MUST be represented as an instance of this class.

    name: str
    start_position: int
    target_position: int
    target_points: int


# Note: Other entities you may want to add, depending on your game plan:
# - Puzzle class to represent special locations (could inherit from Location class if it seems suitable)
# - Player class
# etc.
class Player:
    """
    this class represent the player in this game

    Instance Attribute:

    Representation Invariant:

    """
    inventory: set
    time: int

    def __init__(self, time) -> None:
        self.inventory = set()
        self.time = time

    def curr_score(self) -> int:
        """
        method to return curent score earned by player during the game
        """
        # the score coefficient of inventory number
        item_coe = 1
        return  item_coe * len(self.inventory)

    def final_score(self) -> int:
        """
        method to return the total score earned by player in the end of game
        """
        # the score coefficient of time
        time_coe = 1
        # the score coefficient of inventory number
        item_coe = 1
        return time_coe * self.time + item_coe * len(self.inventory)


if __name__ == "__main__":
    pass
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })
