"""Adventure."""


import math


class Adventurer:
    """Class Adventurer."""

    def __init__(self, name: str, class_type: str, power: int, experience: int = 0):
        """Initialize the Adventurer class."""
        self.name = name
        self.class_type = class_type if class_type in ["Fighter", "Druid", "Wizard", "Paladin"] else "Fighter"
        self.power = power if power < 100 else 10
        self.experience = experience

    def __repr__(self):
        """Representation of Adventurer object."""
        return f"{self.name}, the {self.class_type}, Power: {self.power}, Experience: {self.experience}."

    def add_power(self, power: int):
        """Add power to Adventurer."""
        self.power += power

    def add_experience(self, exp: int):
        """Add experience to Adventurer."""
        if (self.experience + exp) > 0:
            if exp > 99:
                self.power += math.floor((self.experience + exp) / 10)
                self.experience = 0
                return self.experience
            self.experience += exp


class Monster:
    """Class Monster."""

    def __init__(self, name: str, type: str, power: int):
        """Initialize the Monster class."""
        self._name = name
        self.type = type
        self.power = power

    @property
    def name(self):
        """Get Monster name."""
        return self._name

    def __repr__(self):
        """Representation of Monster object."""
        if self.type == "Zombie":
            return f"Undead {self.name} of type {self.type}, Power: {self.power}."
        else:
            return f"{self.name} of type {self.type}, Power: {self.power}."


class World:
    """
    World class.

    World is the class where all Adventurers and Monsters are kept and where the game logic is located.
    """

    def __init__(self, python_master: str):
        """Initialize the World class."""
        self._python_master = python_master
        self.adventurer_list = []
        self.monster_list = []
        self.graveyard = []
        self.is_active_adventurers = []
        self.is_active_monsters = []
        self.dict_of_functions = {}
        self.necromancers_status = False

    def get_python_master(self):
        """Get Python master's name."""
        return self._python_master

    def get_monster_list(self):
        """Get monsters from monsters list."""
        return self.monster_list

    def get_adventurer_list(self):
        """Get adventurers from adventurers list."""
        return self.adventurer_list

    def get_graveyard(self):
        """Get persons in graveyard list."""
        return self.graveyard

    def add_adventurer(self, adventurer: Adventurer):
        """Add adventurer to adventurers list."""
        if isinstance(adventurer, Adventurer) and adventurer not in self.is_active_adventurers\
                and adventurer not in self.graveyard:
            self.adventurer_list.append(adventurer)

    def get_active_adventurers(self):
        """Get all the adventurer's from active adventurers list."""
        return sorted(self.is_active_adventurers, key=lambda adventurer: adventurer.experience, reverse=True)

    def search_adventurers_by_class_type(self, class_type):
        """Filter out adventurers who are not in active adventurers list."""
        return list(filter(lambda adventurer: adventurer.class_type == class_type
                    and adventurer not in self.is_active_adventurers, self.adventurer_list))

    def add_adventurer_by_class_type(self, class_type: str, adventurer: Adventurer):
        """
        Add adventurer with certain class_type to active adventurer's list that aren't already in that list.

        Adventurer will be removed from the adventurers list.
        """
        if self.adventurer_list:
            if len(self.search_adventurers_by_class_type(class_type)) > 0:
                self.adventurer_list.remove(adventurer)
                self.is_active_adventurers.append(adventurer)

    def add_strongest_adventurer(self, class_type: str):
        """Add the strongest adventurer to active adventurers list."""
        if len(self.search_adventurers_by_class_type(class_type)) > 0:
            adventurer_most_power = sorted(self.search_adventurers_by_class_type(class_type), key=lambda x: x.power)[-1]
            self.add_adventurer_by_class_type(class_type, adventurer_most_power)

    def add_weakest_adventurer(self, class_type: str):
        """Add the weakest adventurer to active adventurers list."""
        if len(self.search_adventurers_by_class_type(class_type)) > 0:
            adventurer_least_power = sorted(self.search_adventurers_by_class_type(class_type), key=lambda x: -x.power)[-1]
            self.add_adventurer_by_class_type(class_type, adventurer_least_power)

    def add_most_experienced_adventurer(self, class_type: str):
        """Add the most experienced adventurer to active adventurers list."""
        if len(self.search_adventurers_by_class_type(class_type)) > 0:
            most_experienced = sorted(self.search_adventurers_by_class_type(class_type), key=lambda x: x.experience)[-1]
            self.add_adventurer_by_class_type(class_type, most_experienced)

    def add_least_experienced_adventurer(self, class_type: str):
        """Add the lest experienced adventurer to active adventurers list."""
        if len(self.search_adventurers_by_class_type(class_type)) > 0:
            least_experienced = sorted(self.search_adventurers_by_class_type(class_type), key=lambda x: -x.experience)[-1]
            self.add_adventurer_by_class_type(class_type, least_experienced)

    def add_adventurer_by_name(self, name: str):
        """Add adventurer by name to active adventurers list."""
        for adventurer in self.adventurer_list.copy():
            if adventurer.name == name and adventurer not in self.is_active_adventurers:
                self.adventurer_list.remove(adventurer)
                return self.is_active_adventurers.append(adventurer)

    def add_all_adventurers_of_class_type(self, class_type: str):
        """Add the adventurer's by class type from adventurers list to active adventurers list."""
        for adventurer in self.adventurer_list:
            if adventurer.class_type == class_type and adventurer not in self.is_active_adventurers:
                self.is_active_adventurers.append(adventurer)

    def add_all_adventurers(self):
        """Add the adventurers to active adventurers list."""
        for adventurer in self.adventurer_list.copy():
            if adventurer not in self.is_active_adventurers:
                self.adventurer_list.remove(adventurer)
                self.is_active_adventurers.append(adventurer)

    def get_active_monsters(self):
        """Get all the monsters from active monsters list."""
        return sorted(self.is_active_monsters, key=lambda x: -x.power)

    def add_monster_by_name(self, name: str):
        """Add monster by name to active monsters list."""
        for monster in self.monster_list.copy():
            if monster.name == name and monster not in self.is_active_monsters:
                self.monster_list.remove(monster)
                return self.is_active_monsters.append(monster)

    def add_strongest_monster(self):
        """Add the strongest monster to active monsters list."""
        if len(self.monster_list) > 0:
            non_active_monsters = list(filter(lambda x: x not in self.is_active_monsters, self.monster_list))
            if len(non_active_monsters) > 0:
                most_power = sorted(non_active_monsters, key=lambda x: x.power)[-1]
                self.monster_list.remove(most_power)
                self.is_active_monsters.append(most_power)

    def add_weakest_monster(self):
        """Add the weakest monster to active monsters list."""
        if len(self.monster_list) > 0:
            non_active_monsters = list(filter(lambda x: x not in self.is_active_monsters, self.monster_list))
            if len(non_active_monsters) > 0:
                least_power = sorted(non_active_monsters, key=lambda x: -x.power)[-1]
                self.monster_list.remove(least_power)
                self.is_active_monsters.append(least_power)

    def add_all_monsters_of_type(self, type: str):
        """Add all the monsters from monsters list by type to active monsters list."""
        for monster in self.monster_list:
            if monster.type == type and monster not in self.is_active_monsters:
                self.is_active_monsters.append(monster)

    def add_all_monsters(self):
        """Add all the monsters from monsters list to active monsters list."""
        for monster in self.monster_list.copy():
            if monster not in self.is_active_monsters:
                self.monster_list.remove(monster)
                self.is_active_monsters.append(monster)

    def add_monster(self, monster: Monster):
        """Add monster to monsters list."""
        if isinstance(monster, Monster) and monster not in self.graveyard:
            self.monster_list.append(monster)

    def remove_character(self, name: str):
        """Remove character from graveyard, monsters list or adventurers list and move it to graveyard."""
        for person in self.adventurer_list:
            if person.name == name:
                self.adventurer_list.remove(person)
                return self.graveyard.append(person)
        for monster in self.monster_list:
            if monster.name == name:
                self.monster_list.remove(monster)
                return self.graveyard.append(monster)
        for being in self.graveyard:
            if being.name == name:
                return self.graveyard.remove(being)

    def necromancers_active(self, active: bool):
        """
        Set necromancers status to True or False.

        If necromancers status is set to True revive_graveyard() function (when called)
        moves everyone from graveyard to monsters list.
        """
        if active is True:
            self.necromancers_status = True
        if active is False:
            self.necromancers_status = False

    def revive_graveyard(self):
        """
        Move everyone from graveyard to monsters list (when necromancers status is True).

        Monsters will be changed to Zombie type and adventurers to monsters (type Zombie [adventurer's class type])
        """
        if self.necromancers_status:
            graveyard_list_copy = self.graveyard.copy()
            for being in graveyard_list_copy:
                if isinstance(being, Monster):
                    self.graveyard.remove(being)
                    being.type = "Zombie"
                    self.monster_list.append(being)
                if isinstance(being, Adventurer):
                    new_monster = Monster(f"Undead {being.name}", f"Zombie {being.class_type}", being.power)
                    self.monster_list.append(new_monster)
                    self.graveyard.remove(being)
            self.necromancers_status = False

    def calculate_adventurers_all_power(self):
        """Calculate the power of all active adventurers."""
        return sum([x.power for x in self.is_active_adventurers])

    def calculate_monsters_all_power(self):
        """Calculate the power of all active monsters."""
        return sum([x.power for x in self.is_active_monsters])

    def compare_powers(self):
        """Compare the powers of adventurers and monsters and decide who win or if it's a draw."""
        adventurers_power_sum = self.calculate_adventurers_all_power()
        monsters_power_sum = self.calculate_monsters_all_power()
        if adventurers_power_sum > monsters_power_sum:
            return "Adventurers win"
        if adventurers_power_sum == monsters_power_sum:
            return "Equal"
        if adventurers_power_sum < monsters_power_sum:
            return "Monsters win"

    def check_if_druid_in_active_adventurers(self):
        """Check if Druid type is in active adventurers list."""
        for adventurer in self.is_active_adventurers:
            if adventurer.class_type == "Druid":
                return True
        return False

    def check_monster_type_animal_or_ent(self):
        """
        When monster's type is Animal or Ent, the monster will be removed from active monsters list.

        Method also checks if Druid type is in active adventurers list.
        """
        for monster in self.is_active_monsters.copy():
            if (monster.type == "Animal" or monster.type == "Ent") and self.check_if_druid_in_active_adventurers():
                self.is_active_monsters.remove(monster)
                self.monster_list.append(monster)

    def paladin_power_will_be_doubled(self):
        """
        Double the amount of power of adventurers with type Paladin.

        When monster's type is "Zombie", "Zombie Fighter", "Zombie Druid", "Zombie Paladin", "Zombie Wizard"
        and one of the adventurer's type is Paladin, double the power of that adventurer.
        """
        monster_types = ["Zombie", "Zombie Fighter", "Zombie Druid", "Zombie Paladin", "Zombie Wizard"]
        monster_type_in_list = False
        for monster in self.is_active_monsters:
            if monster.type in monster_types:
                monster_type_in_list = True
                break
        if monster_type_in_list:
            for adventurer in self.is_active_adventurers:
                if adventurer.class_type == "Paladin":
                    adventurer.power = adventurer.power * 2
                    return True
        return False

    def restore_previous_paladin_power_state(self):
        """After fight adventurers powers (only with type Paladin) will be reduced as they were before the fight."""
        for adventurer in self.is_active_adventurers:
            if adventurer.class_type == "Paladin":
                adventurer.power = adventurer.power // 2

    def return_all_adventurers_from_active(self):
        """Move all the adventurers from active to adventurers list."""
        for adventurer in self.is_active_adventurers.copy():
            self.is_active_adventurers.remove(adventurer)
            self.adventurer_list.append(adventurer)

    def return_all_monsters_from_active(self):
        """Move all the monsters from active to monsters list."""
        for monster in self.is_active_monsters.copy():
            self.is_active_monsters.remove(monster)
            self.monster_list.append(monster)

    def defeated_adventurers_to_graveyard(self):
        """Remove all the adventurers from active adventurers list and send them to graveyard."""
        for adventurer in self.is_active_adventurers.copy():
            self.is_active_adventurers.remove(adventurer)
            self.graveyard.append(adventurer)

    def defeated_monsters_to_graveyard(self):
        """Remove all the monsters from active monsters list and send them to graveyard."""
        for monster in self.is_active_monsters.copy():
            self.is_active_monsters.remove(monster)
            self.graveyard.append(monster)

    def adventurers_receive_experience_from_monsters(self, multiply=1, divide_by=1):
        """Calculate the amount of experience adventurers should receive after winning the fight."""
        experience_to_add = self.calculate_monsters_all_power() / len(self.is_active_adventurers)
        for adventurer in self.is_active_adventurers:
            adventurer.add_experience(math.floor((experience_to_add / divide_by) * multiply))

    def go_adventure_if_deadly(self, calculate_powers, paladin_power):
        """Call all the functions needed if adventure is deadly."""
        if calculate_powers == "Equal":
            if paladin_power is True:
                self.restore_previous_paladin_power_state()
            self.adventurers_receive_experience_from_monsters(divide_by=2)
            self.return_all_adventurers_from_active()
            self.return_all_monsters_from_active()
        if calculate_powers == "Adventurers win":
            if paladin_power is True:
                self.restore_previous_paladin_power_state()
            self.adventurers_receive_experience_from_monsters(multiply=2)
            self.return_all_adventurers_from_active()
            self.defeated_monsters_to_graveyard()
        if calculate_powers == "Monsters win":
            if paladin_power is True:
                self.restore_previous_paladin_power_state()
            self.return_all_monsters_from_active()
            self.defeated_adventurers_to_graveyard()

    def go_adventure_if_not_deadly(self, calculate_powers, paladin_power):
        """Call all the functions needed if adventure is not deadly."""
        if calculate_powers == "Equal":
            if paladin_power is True:
                self.restore_previous_paladin_power_state()
            self.adventurers_receive_experience_from_monsters(divide_by=2)
            self.return_all_adventurers_from_active()
            self.return_all_monsters_from_active()
        if calculate_powers == "Adventurers win":
            if paladin_power is True:
                self.restore_previous_paladin_power_state()
            self.adventurers_receive_experience_from_monsters()
            self.return_all_adventurers_from_active()
            self.return_all_monsters_from_active()
        if calculate_powers == "Monsters win":
            if paladin_power is True:
                self.restore_previous_paladin_power_state()
            self.return_all_adventurers_from_active()
            self.return_all_monsters_from_active()

    def go_adventure(self, deadly: bool = False):
        """
        Implement all game logic.

        This is where monsters and adventurers will fight with each other.
        """
        self.check_monster_type_animal_or_ent()
        paladin_power = self.paladin_power_will_be_doubled()
        calculate_powers = self.compare_powers()
        if deadly:
            self.go_adventure_if_deadly(calculate_powers, paladin_power)
        if deadly is False:
            self.go_adventure_if_not_deadly(calculate_powers, paladin_power)
