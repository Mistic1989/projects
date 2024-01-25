"""Testing Adventure."""


import pytest


from adventure import Adventurer, Monster, World


def test_python_master():
    """Get Python Master's name."""
    world = World("Mati")
    assert world.get_python_master() == "Mati"


@pytest.fixture()
def world1():
    """
    Create world1 for testing.

    One monster and one adventurer.
    """
    world = World("Mati")
    adventurer = Adventurer("Kati", "Paladin", 15)
    monster = Monster("Ogre", "Big Ogre", 10)
    world.add_monster(monster)
    world.add_adventurer(adventurer)
    return world


@pytest.fixture()
def world2():
    """Create world2 for testing.

    Four different types of Adventurers. No monsters.
    """
    world = World("Alo")
    hero1 = Adventurer("Eino", "Fighter", 20)
    hero2 = Adventurer("Eino2", "Druid", 20)
    hero3 = Adventurer("Eino3", "Wizard", 20)
    hero4 = Adventurer("Eino4", "Paladin", 25)
    world.add_adventurer(hero1)
    world.add_adventurer(hero2)
    world.add_adventurer(hero3)
    world.add_adventurer(hero4)
    return world


@pytest.fixture()
def world3():
    """
    Create world3 for testing.

    Includes Animal and Ent types of monsters. Druid type in Adventurers group.
    """
    world = World("Alo2")
    hero1 = Adventurer("Eino", "Fighter", 20)
    hero2 = Adventurer("Eino2", "Druid", 20)
    hero3 = Adventurer("Eino3", "Wizard", 20)
    hero4 = Adventurer("Eino4", "Paladin", 25)
    monster1 = Monster("Ogre", "Animal", 10)
    monster2 = Monster("Ogi", "Ent", 101)
    world.add_adventurer(hero1)
    world.add_adventurer(hero2)
    world.add_adventurer(hero3)
    world.add_adventurer(hero4)
    world.add_monster(monster1)
    world.add_monster(monster2)
    return world


@pytest.fixture()
def world4():
    """
    Create world4 for testing.

    Includes two Paladin types in Adventurers group and zombie types in monsters group.
    """
    world = World("Paladin")
    hero1 = Adventurer("Eino", "Fighter", 20)
    hero2 = Adventurer("Eino2", "Dru", 20)
    hero3 = Adventurer("Eino3", "Paladin", 10)
    hero4 = Adventurer("Eino4", "Paladin", 10)
    monster1 = Monster("Ogre", "Zombie", 50)
    monster2 = Monster("Ogi", "Zombie Fighter", 20)
    world.add_adventurer(hero1)
    world.add_adventurer(hero2)
    world.add_adventurer(hero3)
    world.add_adventurer(hero4)
    world.add_monster(monster1)
    world.add_monster(monster2)
    return world


@pytest.fixture()
def monster_zombie():
    """Create monster with type Zombie."""
    return Monster("Zombi", "Zombie", 10)


@pytest.fixture()
def monster_animal():
    """Create monster with type Animal."""
    return Monster("Pig", "Animal", 10)


@pytest.fixture()
def monster_not_zombie():
    """Create monster with type not Zombie."""
    return Monster("Ogre", "Big Ogre", 10)


@pytest.fixture()
def monster_salamander():
    """Create monster with random type."""
    return Monster("Salu", "Salamander", 15)


@pytest.fixture()
def adventurer_toomas():
    """Create adventurer with Paladin type."""
    return Adventurer("Toomas", "Paladin", 10)


@pytest.fixture()
def adventurer_paladin():
    """Create another adventurer with Paladin type."""
    return Adventurer("Toomas Teine", "Paladin", 16)


@pytest.fixture()
def adventurer_mat():
    """Create one adventurer with Paladin type."""
    return Adventurer("Mat", "Paladin", 20)


@pytest.fixture()
def adventurer_aino():
    """Create adventurer with Fighter type."""
    return Adventurer("Aino", "Fighter", 85, 12)


@pytest.fixture()
def adventurer_with_different_class_type():
    """Create another adventurer with random type."""
    return Adventurer("Eino", "Mystic", 20)


def test_add_power(adventurer_toomas, monster_zombie):
    """Add power to adventurer."""
    adventurer_toomas.add_power(10)
    assert adventurer_toomas.power == 20


def test_add_experience(adventurer_toomas):
    """Add experience to adventurer."""
    adventurer_toomas.add_experience(20)
    adventurer_toomas.add_experience(100)
    assert adventurer_toomas.experience == 0


def test_create_different_type_of_adventurer(adventurer_with_different_class_type):
    """Return type Fighter, if adventurer is not Fighter, Druid, Wizard or Paladin."""
    assert adventurer_with_different_class_type.class_type == "Fighter"


def test_fighter_druid_wizard_paladin_types(world2):
    """Test if Fighter, Druid, Wizard or Paladin types of adventurers are created correctly to the adventurers list."""
    class_types = ["Fighter", "Druid", "Wizard", "Paladin"]
    four_types_of_adventurers = [x.class_type for x in world2.get_adventurer_list()]
    assert str(four_types_of_adventurers) == str(class_types)


def test_get_active_adventurers(world1):
    """
    Get active adventurers.

    Adventurers may not be in adventurers list if they are active.
    """
    world1.add_all_adventurers()
    assert str(world1.get_adventurer_list()) == "[]"
    assert str(world1.get_active_adventurers()) == "[Kati, the Paladin, Power: 15, Experience: 0.]"


def test_representation_of_adventurer_object(adventurer_toomas):
    """Adventurer object should be represented as described."""
    assert str(adventurer_toomas) == 'Toomas, the Paladin, Power: 10, Experience: 0.'


def test_only_adventurers_can_be_added_to_adventurers_list(world1, monster_not_zombie):
    """Monsters cannot be added to adventurers list."""
    world1.add_adventurer(monster_not_zombie)
    assert str(world1.get_adventurer_list()) == "[Kati, the Paladin, Power: 15, Experience: 0.]"


def test_get_persons_from_graveyard_after_removed_from_adventurers_list(world2):
    """When adventurers removed from adventurers list, they should appear in graveyard."""
    world2.remove_character("Eino")
    world2.remove_character("Eino2")
    world2.remove_character("Eino3")
    world2.remove_character("Eino4")
    assert str(world2.get_adventurer_list()) == "[]"
    assert str(world2.get_graveyard()) == "[Eino, the Fighter, Power: 20, Experience: 0.," \
                                          " Eino2, the Druid, Power: 20, Experience: 0.," \
                                          " Eino3, the Wizard, Power: 20, Experience: 0.," \
                                          " Eino4, the Paladin, Power: 25, Experience: 0.]"


def test_append_persons_from_adventurers_and_monsters_list_to_graveyard(world2, monster_not_zombie):
    """Add monster or adventurer directly to graveyard."""
    world2.get_graveyard().append(monster_not_zombie)
    hero1 = Adventurer("Eino", "Fighter", 20)
    world2.get_graveyard().append(hero1)
    assert str(world2.get_graveyard()) ==\
           "[Ogre of type Big Ogre, Power: 10., Eino, the Fighter, Power: 20, Experience: 0.]"


def test_persons_in_graveyard_not_in_other_lists(world2, monster_not_zombie):
    """When monster or adventurer sent to graveyard, they are not in any other lists."""
    world2.remove_character("Eino3")
    world2.remove_character("Eino4")
    world2.add_monster(monster_not_zombie)
    world2.remove_character("Ogre")
    world2.remove_character("Ogre")
    assert str(world2.get_graveyard()) == "[Eino3, the Wizard, Power: 20, Experience: 0., Eino4, the Paladin, Power: 25, Experience: 0.]"
    assert str(world2.get_monster_list()) == "[]"
    assert str(world2.get_adventurer_list()) == "[Eino, the Fighter, Power: 20, Experience: 0., Eino2, the Druid, Power: 20, Experience: 0.]"


def test_revive_graveyard_necromancers_active_and_not_active(world2):
    """
    Test revive graveyard when necromancers are active and if they are not.

    If necromancers status if True, the monsters will be removed to monsters list.
    If necromancers status is False, persons will stay in graveyard.
    """
    hero1 = Adventurer("Eino", "Fighter", 20)
    hero2 = Adventurer("Eino2", "Druid", 20)
    world2.necromancers_active(True)
    world2.get_graveyard().append(hero1)
    world2.get_graveyard().append(hero2)
    world2.revive_graveyard()
    assert str(world2.get_monster_list()) ==\
           "[Undead Eino of type Zombie Fighter, Power: 20., Undead Eino2 of type Zombie Druid, Power: 20.]"
    world2.necromancers_active(False)
    world2.get_graveyard().append(hero1)
    world2.get_graveyard().append(hero2)
    world2.revive_graveyard()
    assert str(world2.get_graveyard()) == \
           "[Eino, the Fighter, Power: 20, Experience: 0., Eino2, the Druid, Power: 20, Experience: 0.]"
    assert str(world2.get_monster_list()) == \
           "[Undead Eino of type Zombie Fighter, Power: 20., Undead Eino2 of type Zombie Druid, Power: 20.]"
    assert world2.necromancers_status is False


def test_after_revive_graveyard_graveyard_is_empty(world2):
    """Graveyard is empty after revive graveyard (if necromancers status is True)."""
    hero1 = Adventurer("Eino", "Fighter", 20)
    hero2 = Adventurer("Eino2", "Druid", 20)
    world2.necromancers_active(True)
    world2.get_graveyard().append(hero1)
    world2.get_graveyard().append(hero2)
    world2.revive_graveyard()
    assert str(world2.get_graveyard()) == "[]"


def test_revive_graveyard_monsters_type_changed_to_zombie(world2, monster_not_zombie, monster_salamander):
    """After revive graveyard monsters type will be changed to Zombie and added to monsters list."""
    world2.get_graveyard().append(monster_salamander)
    world2.get_graveyard().append(monster_not_zombie)
    world2.necromancers_active(True)
    world2.revive_graveyard()
    zombie_types = [x.type for x in world2.get_monster_list()]
    assert str(zombie_types) == "['Zombie', 'Zombie']"


def test_revive_graveyard_adventurers_type_changed_to_monster(world2, adventurer_toomas, adventurer_mat):
    """
    After revive graveyard adventurers will be changed to monsters.

    Adventurers will be moved to monsters list and will have Undead in front of the name.
    Adventurers will be Monsters.
    When added to monsters list, Zombie will be added in front of the type name.
    """
    world2.get_graveyard().append(adventurer_toomas)
    world2.get_graveyard().append(adventurer_mat)
    world2.necromancers_active(True)
    world2.revive_graveyard()
    assert str(world2.get_monster_list()[0].name) == "Undead Toomas"
    assert str(world2.get_monster_list()[0].type) == "Zombie Paladin"
    assert isinstance(world2.get_monster_list()[0], Monster) is True


def test_add_strongest_adventurer(world2):
    """Add adventurer with most power to active adventurers list."""
    new_hero = Adventurer("Tere", "Wizard", 3)
    world2.add_adventurer(new_hero)
    world2.add_strongest_adventurer("Wizard")
    assert str(world2.get_active_adventurers()) == "[Eino3, the Wizard, Power: 20, Experience: 0.]"


def test_add_weakest_adventurer(world2):
    """Add adventurer with least power to active adventurers list."""
    new_hero = Adventurer("Tere", "Wizard", 3)
    world2.add_adventurer(new_hero)
    world2.add_weakest_adventurer("Wizard")
    assert str(world2.get_active_adventurers()) == "[Tere, the Wizard, Power: 3, Experience: 0.]"


def test_add_most_experienced_adventurer(world2):
    """Add adventurer with most experience to active adventurers list."""
    new_hero = Adventurer("Tere", "Wizard", 3, 2)
    world2.add_adventurer(new_hero)
    world2.add_most_experienced_adventurer("Wizard")
    assert str(world2.get_active_adventurers()) == "[Tere, the Wizard, Power: 3, Experience: 2.]"


def test_add_least_experienced_adventurer(world2):
    """Add adventurer with the least experience to active adventurers list."""
    new_hero = Adventurer("Tere", "Wizard", 3, 2)
    world2.add_adventurer(new_hero)
    world2.add_least_experienced_adventurer("Wizard")
    assert str(world2.get_active_adventurers()) == "[Eino3, the Wizard, Power: 20, Experience: 0.]"


def test_add_adventurer_by_name(world2):
    """Add adventurer by name to active adventurers list."""
    new_hero = Adventurer("Tere", "Wizard", 3, 2)
    world2.add_adventurer(new_hero)
    world2.add_adventurer_by_name("Tere")
    assert str(world2.get_active_adventurers()) == "[Tere, the Wizard, Power: 3, Experience: 2.]"


def test_add_all_adventurers_of_class_type(world2):
    """Add all adventurers by class type to active adventurers list."""
    new_hero = Adventurer("Tere", "Wizard", 3, 2)
    world2.add_adventurer(new_hero)
    world2.add_all_adventurers_of_class_type("Wizard")
    assert str(world2.get_active_adventurers()) == "[Tere, the Wizard, Power: 3, Experience: 2., Eino3, the Wizard, Power: 20, Experience: 0.]"


def test_add_all_adventurers_to_adventures_list(world2):
    """Add all adventurers by to active adventurers list."""
    new_hero = Adventurer("Tere", "Wizard", 3, 2)
    world2.add_adventurer(new_hero)
    world2.add_all_adventurers()
    assert str(world2.get_active_adventurers()) == "[Tere, the Wizard, Power: 3, Experience: 2., Eino, the Fighter, Power: 20, Experience: 0., Eino2, the Druid, Power: 20, Experience: 0., Eino3, the Wizard, Power: 20, Experience: 0., Eino4, the Paladin, Power: 25, Experience: 0.]"


def test_representation_of_monster_object_if_zombie(monster_zombie):
    """Monster object representation if type is Zombie."""
    assert str(monster_zombie) == 'Undead Zombi of type Zombie, Power: 10.'


def test_representation_of_monster_object_if_not_zombie(monster_not_zombie):
    """Monster object representation if type is not Zombie."""
    assert str(monster_not_zombie) == 'Ogre of type Big Ogre, Power: 10.'


def test_only_monsters_can_be_added_to_monsters_list(world1, adventurer_toomas):
    """Only monsters can be added to monsters list."""
    world1.add_monster(adventurer_toomas)
    assert str(world1.get_monster_list()) == "[Ogre of type Big Ogre, Power: 10.]"


def test_get_active_monsters(world1):
    """Get active monsters list."""
    world1.add_all_monsters()
    assert str(world1.get_monster_list()) == "[]"
    assert str(world1.get_active_monsters()) == "[Ogre of type Big Ogre, Power: 10.]"


def test_add_monster_by_name(world1):
    """Add monster by name to active monsters list."""
    new_monster = Monster("Sabbath", "Worm", 300000000)
    world1.add_monster(new_monster)
    world1.add_monster_by_name("Sabbath")
    assert str(world1.get_active_monsters()) == "[Sabbath of type Worm, Power: 300000000.]"


def test_add_strongest_monster(world1):
    """Add the strongest monster to active monsters list."""
    new_monster = Monster("Sabbath", "Worm", 300000000)
    world1.add_monster(new_monster)
    world1.add_strongest_monster()
    assert str(world1.get_active_monsters()) == "[Sabbath of type Worm, Power: 300000000.]"


def test_add_weakest_monster(world1):
    """Add the weakest monster to active monsters list."""
    new_monster = Monster("Sabbath", "Worm", 300000000)
    new_monster2 = Monster("Uss", "Worm", 1)
    world1.add_monster(new_monster)
    world1.add_monster(new_monster2)
    world1.add_weakest_monster()
    assert str(world1.get_active_monsters()) == "[Uss of type Worm, Power: 1.]"


def test_add_all_monsters_of_type(world1):
    """Add all monsters by type to active monsters list."""
    new_monster = Monster("Sabbath", "Worm", 300000000)
    new_monster2 = Monster("Uss", "Worm", 300)
    world1.add_monster(new_monster)
    world1.add_monster(new_monster2)
    world1.add_all_monsters_of_type("Worm")
    assert str(world1.get_active_monsters()) == "[Sabbath of type Worm, Power: 300000000., Uss of type Worm, Power: 300.]"


def test_add_all_monsters_to_active_list(world1):
    """Add all monsters to active monsters list."""
    new_monster = Monster("Sabbath", "Worm", 300000000)
    new_monster2 = Monster("Uss", "Worm", 300)
    world1.add_monster(new_monster)
    world1.add_monster(new_monster2)
    world1.add_all_monsters()
    assert str(world1.get_active_monsters()) == "[Sabbath of type Worm, Power: 300000000., Uss of type Worm, Power: 300., Ogre of type Big Ogre, Power: 10.]"


def test_add_monster_to_monsters_list(world1):
    """Add monster to monsters list."""
    new_monster2 = Monster("Uss", "Worm", 300)
    world1.add_monster(new_monster2)
    assert str(world1.get_monster_list()) == "[Ogre of type Big Ogre, Power: 10., Uss of type Worm, Power: 300.]"


def test_remove_character_all(world1):
    """Remove character from monsters or adventurers list and move to graveyard."""
    new_monster = Monster("Sabbath", "Worm", 300000000)
    new_monster2 = Monster("Uss", "Worm", 300)
    world1.add_monster(new_monster)
    world1.get_graveyard().append(new_monster2)
    world1.remove_character("Uus")
    world1.remove_character("Sabbath")
    assert str(world1.get_monster_list()) == "[Ogre of type Big Ogre, Power: 10.]"
    assert str(world1.get_adventurer_list()) == "[Kati, the Paladin, Power: 15, Experience: 0.]"
    assert str(world1.get_graveyard()) == "[Uss of type Worm, Power: 300., Sabbath of type Worm, Power: 300000000.]"


def test_compare_adventurers_and_monsters_powers(world1):
    """
    Compare monsters and adventurers powers.

    Testing both adventurers and monsters power sums separately.
    The one with higher power will win.
    """
    new_monster = Monster("Sabbath", "Worm", 30)
    new_monster2 = Monster("Uss", "Worm", 98)
    new_monster3 = Monster("Uss2", "Worm", 77)
    new_hero = Adventurer("Tere", "Wizard", 3, 100)
    new_hero2 = Adventurer("Tere2", "Fighter", 99)
    new_hero3 = Adventurer("Tere3", "Mingi", 98)
    world1.add_adventurer(new_hero)
    world1.add_monster(new_monster)
    world1.add_monster(new_monster2)
    world1.add_all_adventurers()
    world1.add_all_monsters()
    assert world1.calculate_adventurers_all_power() == 18
    assert world1.calculate_monsters_all_power() == 138
    assert world1.compare_powers() == "Monsters win"
    world1.add_adventurer(new_hero2)
    world1.add_adventurer(new_hero3)
    world1.add_all_adventurers()
    assert world1.compare_powers() == "Adventurers win"
    world1.add_monster(new_monster3)
    world1.add_all_monsters()
    assert world1.compare_powers() == "Equal"


def test_check_monster_type_animal_or_ent(world3):
    """
    Animal and Ent type of monsters cannot go to battle if Druid type in active adventurers list.

    Test confirms that Animal and Ent types remain in monsters list.
    """
    world3.add_all_adventurers()
    world3.add_all_monsters()
    world3.go_adventure(True)
    assert str(world3.get_monster_list()) == "[Ogre of type Animal, Power: 10., Ogi of type Ent, Power: 101.]"


def test_power_doubled_when_paladin_in_adventures_list(world4):
    """Paladin type of adventurers power will be doubled for one battle."""
    world4.add_all_adventurers()
    world4.add_all_monsters()
    world4.go_adventure(True)
    world4.add_all_adventurers()
    assert world4.calculate_adventurers_all_power() == 55


def test_defeated_adventurers_to_graveyard(world1):
    """Defeated adventurers will go to graveyard."""
    new_monster = Monster("Sabbath", "Worm", 30)
    new_monster2 = Monster("Uss", "Worm", 98)
    new_hero = Adventurer("Tere", "Wizard", 3, 100)
    world1.add_adventurer(new_hero)
    world1.add_monster(new_monster)
    world1.add_monster(new_monster2)
    world1.add_all_adventurers()
    world1.add_all_monsters()
    world1.go_adventure(True)
    assert str(world1.get_graveyard()) == "[Kati, the Paladin, Power: 15, Experience: 0., Tere, the Wizard, Power: 3, Experience: 100.]"


def test_defeated_monsters_to_graveyard(world1):
    """Defeated monsters will go to graveyard."""
    new_monster = Monster("Sabbath", "Worm", 1)
    world1.add_monster(new_monster)
    world1.add_all_adventurers()
    world1.add_all_monsters()
    world1.go_adventure(True)
    assert str(world1.get_graveyard()) == "[Ogre of type Big Ogre, Power: 10., Sabbath of type Worm, Power: 1.]"


def test_adventurers_receive_experience_from_monsters(world1, monster_animal, adventurer_paladin):
    """Adventurers receive experience points if they win monsters."""
    world1.add_monster(monster_animal)
    world1.add_adventurer(adventurer_paladin)
    world1.add_all_adventurers()
    world1.add_all_monsters()
    world1.go_adventure()
    assert str(world1.get_adventurer_list()[0]) == "Kati, the Paladin, Power: 15, Experience: 10."
    assert str(world1.get_adventurer_list()[1]) == "Toomas Teine, the Paladin, Power: 16, Experience: 10."


def test_paladins_against_necromancers_experience(world1, monster_animal, adventurer_paladin, monster_salamander, monster_not_zombie, adventurer_mat, adventurer_aino):
    """
    Paladin type of adventurers against necromancers.

    Paladin type of adventurers power will be doubled,
    therefore it should affect the amount of power and experience points adventurers receive when they win the battle.
    """
    world1.add_monster(monster_animal)
    world1.add_adventurer(adventurer_paladin)
    world1.add_adventurer(adventurer_aino)
    world1.get_graveyard().append(monster_salamander)
    world1.get_graveyard().append(monster_not_zombie)
    world1.necromancers_active(True)
    world1.revive_graveyard()
    world1.add_all_adventurers()
    world1.add_all_monsters()
    world1.go_adventure(True)
    assert world1.get_adventurer_list()[0].experience == 30
    assert world1.get_adventurer_list()[1].experience == 30
    assert world1.get_adventurer_list()[2].experience == 42
    assert world1.get_adventurer_list()[0].power == 15
    assert world1.get_adventurer_list()[1].power == 8
    assert world1.get_adventurer_list()[2].power == 85


def test_go_adventure_if_deadly_get_lists_correct(world1):
    """Test adventure when status is deadly.

    When deadly, defeated group will move to graveyard and will be removed from other lists.
    Winners can receive power and experience points from monsters and can return to their main list.
    Experience points will be doubled.
    If tie occurs, adventurers receive experience points that will be divided by 2.
    """
    world1.add_monster(Monster("Suur", "Ogre", 98))
    world1.add_monster(Monster("Suur2", "Ogre", 80))
    world1.add_monster(Monster("Suur3", "Zombie", 5000))
    world1.add_all_adventurers()
    world1.add_all_monsters()
    world1.go_adventure(True)
    assert str(world1.get_adventurer_list()) == "[]"
    assert str(world1.get_monster_list()) == "[Ogre of type Big Ogre, Power: 10., Suur of type Ogre, Power: 98., Suur2 of type Ogre, Power: 80., Undead Suur3 of type Zombie, Power: 5000.]"


def test_go_adventure_if_not_deadly_get_lists_correct(world1, adventurer_toomas, adventurer_paladin):
    """Test adventure when status is not deadly.

    When not deadly, no one moves to graveyard and everyone can go back to their main lists.
    Winners (Adventurers) can receive power and experience points from monsters.
    Adventurers can receive experience points but points will not be doubled.
    If tie occurs, adventurers receive experience points that will be divided by 2.
    Test will test 3 different possibilities: Adventurers win, Monsters win and tie
    """
    world1.add_monster(Monster("Suur", "Ogre", 98))
    world1.add_monster(Monster("Suur2", "Ogre", 80))
    world1.add_monster(Monster("Suur3", "Zombie", 5000))
    world1.add_adventurer(adventurer_toomas)
    world1.add_all_adventurers()
    world1.add_all_monsters()
    world1.go_adventure(False)
    assert str(world1.get_adventurer_list()) == "[Kati, the Paladin, Power: 15, Experience: 0., Toomas, the Paladin, Power: 5, Experience: 0.]"
    assert str(world1.get_monster_list()) == "[Ogre of type Big Ogre, Power: 10., Suur of type Ogre, Power: 98., Suur2 of type Ogre, Power: 80., Undead Suur3 of type Zombie, Power: 5000.]"
    world1.remove_character("Suur3")
    world1.remove_character("Suur2")
    world1.remove_character("Suur")
    world1.add_monster(Monster("Suur3", "Zombie", 5))
    world1.add_adventurer(adventurer_paladin)
    world1.add_adventurer(adventurer_toomas)
    world1.add_all_adventurers()
    world1.add_all_monsters()
    world1.go_adventure(False)
    assert str(world1.get_adventurer_list()) == "[Toomas, the Paladin, Power: 2, Experience: 5., Kati, the Paladin, Power: 15, Experience: 5., Toomas, the Paladin, Power: 2, Experience: 5., Toomas Teine, the Paladin, Power: 8, Experience: 5.]"
    assert str(world1.get_monster_list()) == "[Ogre of type Big Ogre, Power: 10., Undead Suur3 of type Zombie, Power: 5.]"
    world1.add_monster(Monster("Suur4", "Lambi", 12))
    world1.add_all_adventurers()
    world1.add_all_monsters()
    world1.go_adventure(False)
    assert str(world1.get_adventurer_list()) == "[Toomas, the Paladin, Power: 2, Experience: 9., Toomas, the Paladin, Power: 2, Experience: 9., Kati, the Paladin, Power: 7, Experience: 9., Toomas Teine, the Paladin, Power: 4, Experience: 9.]"
    assert str(world1.get_monster_list()) == "[Ogre of type Big Ogre, Power: 10., Undead Suur3 of type Zombie, Power: 5., Suur4 of type Lambi, Power: 12.]"
