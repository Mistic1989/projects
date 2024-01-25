"""Testing Santa's Workshop."""


import os
import re
import pytest


from santas_workshop import ReceiveData, DataWarehouse, Warehouse, Logistics, Child, Gift, Factory, PostOffice

test_nice_list_dict = {'Libby': ['United Kingdom'], 'Macky': ['United Kingdom'], 'Becky': ['United Kingdom'],
                       'Lecky': ['United Kingdom'], 'Mocky': ['United Kingdom'], 'Topy': ['United Kingdom'],
                       'Keira': ['Germany'], 'Lexie': ['Canada'], 'Amelia': ['South Africa']}
test_naughty_list_dict = {'Tanya': ['United Kingdom'], 'Jamie': ['Canada'], 'Chelsea': ['South Africa'],
                          'Taylor': ['United Kingdom']}
test_wish_list_dict = {'Libby': ['Gloomhaven board game'], 'Macky': ['Gloomhaven board game'],
                       'Becky': ['Gloomhaven board game'],
                       'Lecky': ['Gloomhaven board game'], 'Mocky': ['Gloomhaven board game'],
                       'Topy': ['Gloomhaven board game'],
                       'Keira': ['LED light up sneakers', '7200 Riot Points gift card'],
                       'Lexie': ['Mermaid barbie', 'Pink fluffy pen',
                                 'World of Warcraft: Shadowlands Collectors Edition'],
                       'Amelia': ['Wall-mount diamond pickaxe',
                                  'Magic: The Gathering Commander Legends booster box'],
                       'Tanya': ['Nintendo Switch', 'Frozen Olaf plush toy'],
                       'Jamie': ['Toy train set', 'Raspberry Pi 4', 'Trick scooter'],
                       'Chelsea': ['Raspberry Pi 4', 'World of Warcraft: Shadowlands Collectors Edition'],
                       'Taylor': ['Frozen Olaf plush toy']}
test_children_list = ["Libby", "Macky", "Becky", "Lecky", "Mocky", "Topy", "Keira",
                      "Lexie", "Amelia", "Tanya", "Jamie", "Chelsea", "Taylor"]


@pytest.fixture()
def receive_data():
    """Create instance from class ReceiveData."""
    receive_data = ReceiveData()
    return receive_data


@pytest.fixture()
def data_warehouse():
    """Create instance from class DataWarehouse."""
    receive_data = ReceiveData()
    data_warehouse = DataWarehouse(receive_data, "test_files2/ex15_nice_list.csv",
                                   "test_files2/ex15_naughty_list.csv", "test_files2/ex15_wish_list.csv")
    return data_warehouse


@pytest.fixture()
def factory():
    """Create instance from class Factory."""
    receive_data = ReceiveData()
    data_warehouse = DataWarehouse(receive_data, "test_files2/ex15_nice_list.csv",
                                   "test_files2/ex15_naughty_list.csv", "test_files2/ex15_wish_list.csv")
    factory = Factory(data_warehouse, receive_data)
    return factory


@pytest.fixture()
def logistics():
    """Create instance from class Logistics."""
    receive_data = ReceiveData()
    data_warehouse = DataWarehouse(receive_data, "test_files2/ex15_nice_list.csv",
                                   "test_files2/ex15_naughty_list.csv", "test_files2/ex15_wish_list.csv")
    factory = Factory(data_warehouse, receive_data)
    warehouse = Warehouse(factory)
    logistics = Logistics(warehouse)
    return logistics


@pytest.fixture()
def warehouse():
    """Create instance from class Warehouse."""
    receive_data = ReceiveData()
    data_warehouse = DataWarehouse(receive_data, "test_files2/ex15_nice_list.csv",
                                   "test_files2/ex15_naughty_list.csv", "test_files2/ex15_wish_list.csv")
    factory = Factory(data_warehouse, receive_data)
    warehouse = Warehouse(factory)
    return warehouse


@pytest.fixture()
def post_office():
    """Create instance from class PostOffice."""
    receive_data = ReceiveData()
    data_warehouse = DataWarehouse(receive_data, "test_files2/ex15_nice_list.csv",
                                   "test_files2/ex15_naughty_list.csv", "test_files2/ex15_wish_list.csv")
    factory = Factory(data_warehouse, receive_data)
    warehouse = Warehouse(factory)
    post_office = PostOffice(data_warehouse, receive_data, warehouse)
    return post_office


"""Test class ReceiveData."""


def test_get_data_from_nice_list_csv_file(receive_data):
    """
    Test if data received from one nice list is placed correctly to dictionary.

    Function should add child's name as dict key and country (list) as dict value.
    All the items should be added to dict in the same order as they were in csv file.
    """
    nice_list_dict = {}
    receive_data.get_data_from_file("test_files2/ex15_nice_list.csv", nice_list_dict)
    assert nice_list_dict == test_nice_list_dict


def test_get_data_from_naughty_list_csv_file(receive_data):
    """
    Test if data received from naughty list csv file is correct.

    Function should add child's name as dict key and country (list) as dict value.
    All the items should be added to dict in the same order as they were in csv file.
    """
    naughty_list_dict = {}
    receive_data.get_data_from_file("test_files2/ex15_naughty_list.csv", naughty_list_dict)
    assert naughty_list_dict == test_naughty_list_dict


def test_get_data_from_wish_list_csv_file(receive_data):
    """
    Test if data received from wish list csv file is correct.

    Function should add child's name as dict key and wishes (list) as dict value.
    All the items should be added to dict in the same order as they were in csv file.
    """
    wish_list_dict = {}
    receive_data.get_data_from_file("test_files2/ex15_wish_list.csv", wish_list_dict)
    assert wish_list_dict == test_wish_list_dict


def test_if_input_csv_files_all_empty(receive_data):
    """
    Test situation when nice list, naughty list or wishlist is empty.

    Using get_data_from_file, result should empty dict "{}".
    """
    wish_list_dict = {}
    nice_list_dict = {}
    naughty_list_dict = {}
    receive_data.get_data_from_file("test_files2/ex15_wish_list_empty.csv", wish_list_dict)
    receive_data.get_data_from_file("test_files2/ex15_nice_list_empty.csv", nice_list_dict)
    receive_data.get_data_from_file("test_files2/ex15_naughty_list_empty.csv", naughty_list_dict)
    assert wish_list_dict == {}
    assert nice_list_dict == {}
    assert naughty_list_dict == {}


def test_get_gift_info_from_server(receive_data):
    """
    Test getting info (from server) about certain gift.

    If gift is in database, it should receive info about gift's name, material cost,
    production time and weight in grams.
    If no gift is found from server, certain message should be received.
    If no gift info as input is given to the get_gift_info function, empty list is returned.
    """
    libby = Child("Libby", "Estonia", True, ['Zebra Jumpy'])
    keira = Child("Keira", "Peru", True, ['LED light up sneakers'])
    test_dict = {libby: 'Zebra Jumpy', keira: 'LED light up sneakers'}
    test_dict2 = {}
    test_dict3 = {libby: 'Some random item'}
    assert str(receive_data.get_gift_info(test_dict)) == "[{'gift': 'Zebra Jumpy', 'material_cost': 25," \
                                                         " 'production_time': 1, 'weight_in_grams': 1337}," \
                                                         " {'gift': 'LED light up sneakers', 'material_cost': 35," \
                                                         " 'production_time': 5.89, 'weight_in_grams': 250}]"
    assert receive_data.get_gift_info(test_dict2) == []
    assert receive_data.get_gift_info(test_dict3) == [
        {'message': 'Gift not found! Did you forget to supply the name of the gift as a query parameter?'}]


"""Test class Child."""


def test_child_object_attributes():
    """
    Test child object.

    Child object can be created in Child class.
    Child object has name, country, is_nice (if in nice list return True) and wishlist attributes.
    """
    child = Child("Eino", "Estonia", False, ["Cyberpunk 2077", "Book"])
    assert child.name == "Eino"
    assert child.is_nice is False
    assert child.country == "Estonia"
    assert child.wishlist == ["Cyberpunk 2077", "Book"]


"""Test class DataWarehouse."""


def test_data_warehouse_storage(receive_data, data_warehouse):
    """Test if nice list, naughty list, wish list and children list are accessible from DataWarehouse class."""
    data_warehouse.add_attributes_to_children()
    assert data_warehouse.nice_list == test_nice_list_dict
    assert data_warehouse.naughty_list == test_naughty_list_dict
    assert data_warehouse.wishlists == test_wish_list_dict
    for child in data_warehouse.children:
        assert str(child) in test_children_list


def test_add_attributes_to_children_adds_children_to_children_list(receive_data, data_warehouse):
    """
    Test if child objects are added to children list correctly.

    Child object should have name, country, whether the child is in nice list (bool) or not and wishlist.
    All the children should be added to children list that are in DataWarehouse class.
    """
    data_warehouse.add_attributes_to_children()
    children_attributes_test_list = [
        {'name': 'Libby', 'country': 'United Kingdom', 'is_nice': True, 'wishlist': ['Gloomhaven board game']},
        {'name': 'Macky', 'country': 'United Kingdom', 'is_nice': True, 'wishlist': ['Gloomhaven board game']},
        {'name': 'Becky', 'country': 'United Kingdom', 'is_nice': True, 'wishlist': ['Gloomhaven board game']},
        {'name': 'Lecky', 'country': 'United Kingdom', 'is_nice': True, 'wishlist': ['Gloomhaven board game']},
        {'name': 'Mocky', 'country': 'United Kingdom', 'is_nice': True, 'wishlist': ['Gloomhaven board game']},
        {'name': 'Topy', 'country': 'United Kingdom', 'is_nice': True, 'wishlist': ['Gloomhaven board game']},
        {'name': 'Keira', 'country': 'Germany', 'is_nice': True,
         'wishlist': ['LED light up sneakers', '7200 Riot Points gift card']},
        {'name': 'Lexie', 'country': 'Canada', 'is_nice': True,
         'wishlist': ['Mermaid barbie', 'Pink fluffy pen', 'World of Warcraft: Shadowlands Collectors Edition']},
        {'name': 'Amelia', 'country': 'South Africa', 'is_nice': True,
         'wishlist': ['Wall-mount diamond pickaxe', 'Magic: The Gathering Commander Legends booster box']},
        {'name': 'Tanya', 'country': 'United Kingdom', 'is_nice': False,
         'wishlist': ['Nintendo Switch', 'Frozen Olaf plush toy']},
        {'name': 'Jamie', 'country': 'Canada', 'is_nice': False,
         'wishlist': ['Toy train set', 'Raspberry Pi 4', 'Trick scooter']},
        {'name': 'Chelsea', 'country': 'South Africa', 'is_nice': False,
         'wishlist': ['Raspberry Pi 4', 'World of Warcraft: Shadowlands Collectors Edition']},
        {'name': 'Taylor', 'country': 'United Kingdom', 'is_nice': False, 'wishlist': ['Frozen Olaf plush toy']}]
    for child in data_warehouse.children:
        assert vars(child) in children_attributes_test_list


def test_add_attributes_to_children_only_naughty_list(receive_data):
    """
    Test if no children will be added to children list, if nice list and wish list are empty.

    Even if there are naughty children, they will not be added to children list.
    """
    data_warehouse = DataWarehouse(receive_data, "test_files2/ex15_nice_list_empty.csv",
                                   "test_files2/ex15_naughty_list.csv", "test_files2/ex15_wish_list_empty.csv")
    data_warehouse.add_attributes_to_children()
    assert data_warehouse.children == []


def test_update_csv_files(receive_data):
    """
    Test if csv files have been updated.

    Calling update_csv_files will download csv files from server
    (and overwrite files, if files already exist).
    Nice list, naughty list and wishlist will be updated.
    Os.stat is used to get status of the specified files. It gives time info about most recent content modification.
    If file is modified it will have different time than it was before.
    """
    status_nice = os.stat("ex15_nice_list.csv")
    status_naughty = os.stat("ex15_naughty_list.csv")
    status_wishlist = os.stat("ex15_wish_list.csv")
    receive_data.update_csv_files()
    status_nice2 = os.stat("ex15_nice_list.csv")
    status_naughty2 = os.stat("ex15_naughty_list.csv")
    status_wishlist2 = os.stat("ex15_wish_list.csv")
    assert status_nice != status_nice2
    assert status_naughty != status_naughty2
    assert status_wishlist != status_wishlist2


"""Test class Gift."""


def test_gift_object_attributes():
    """
    Test if gift object is created correctly.

    Gift object should have the following attributes (in this order):
    name: str, receiver: object, material_cost: int, production_time: int, weight_in_grams: int.
    """
    child = Child("Eino", "Estonia", False, ["Cyberpunk 2077"])
    gift = Gift('How to be a good kid by Rafielle E Usher', child, 2, 5, 250)
    assert gift.name == 'How to be a good kid by Rafielle E Usher'
    assert gift.weight_in_grams == 250
    assert gift.receiver == child
    assert gift.material_cost == 2
    assert gift.production_time == 5


"""Test class Factory."""


def test_produce_gifts_for_children_pick_random_gift_only_for_nice_child(receive_data, data_warehouse, factory):
    """
    Test if gifts from the wishlist are given correctly to each child.

    Only children from nice list are picked.
    Each child (if he or she is nice) will get one randomly picked gift from his/her wishlist.
    Produced gifts will be divided into two dicts (nice dict and naughty dict).
    """
    nice = {}
    naughty = {}
    factory.produce_gifts_for_children(nice, naughty)
    for key, value in nice.items():
        assert len([value]) == 1 and value in factory.wishlists[key.name]


def test_produce_gifts_for_children_naughty_children_not_getting_any_wishlist_gifts(receive_data, data_warehouse, factory):
    """
    Children from the naughty list shouldn't receive anything from their wishlists.

    All the children who are in naughty list, will receive a book called:
    How to be a good kid by Rafielle E Usher
    """
    nice = {}
    naughty = {}
    factory.produce_gifts_for_children(nice, naughty)
    for child, gift in naughty.items():
        assert gift not in factory.wishlists[child.name]
        assert str(gift) == '[How to be a good kid by Rafielle E Usher]'


def test_add_received_gift_information_adds_gifts_to_gifts_with_attributes_dict(receive_data, data_warehouse, factory):
    """
    Every gift should have its gift name, receiver name, material cost, production time and weight in grams.

    Result should be a dictionary that contains all the children (from nice and naughty list) gift information.
    According to test, two gifts with attributes should be found from gifts_with_attributes dict.
    In test_attributes there is three gifts with attributes - it is because "Keira" can have either
    "LED light up sneakers" or "7200 Riot Points gift card" as a gift (picked randomly).
    """
    factory.add_received_gift_information()
    test_attributes = [
        """{'name': 'Gloomhaven board game', 'receiver': Libby, 'material_cost': 95, 'production_time': 25, 'weight_in_grams': 10000}""",
        """{'name': '7200 Riot Points gift card', 'receiver': Keira, 'material_cost': 50, 'production_time': 0.1, 'weight_in_grams': 10}""",
        """{'name': 'LED light up sneakers', 'receiver': Keira, 'material_cost': 35, 'production_time': 5.89, 'weight_in_grams': 250}"""]
    count = 0
    for item in test_attributes:
        if item in [str(vars(x[0])) for x in list(factory.gifts_with_attributes.values())]:
            count += 1
    assert count == 2


"""Test class Warehouse."""


def test_warehouse_storage_contains_objects(receive_data, data_warehouse, factory):
    """
    Test if warehouse stores information as objects that is sent from Factory.

    Warehouse storage is a dict, that has child (object) as a key and gift (object) as a value.
    """
    warehouse = Warehouse(factory)
    for key, value in warehouse.storage.items():
        assert isinstance(key, Child)
        assert isinstance(value[0], Gift)


def test_warehouse_storage_has_correct_items_in_storage_only_nice(receive_data, data_warehouse, factory, warehouse):
    """
    Test if warehouse storage stores correct information that is sent from Factory (only nice children).

    In warehouse storage dict, a child should have one gift from wishlist, child has to be nice and
    he/she cannot have "How to be a good kid by Rafielle E Usher" as a gift.
    Libby, Macky, Becky, Lecky, Mocky, Topy, Keira, Lexie, Amelia are all nice children.
    """
    wishlist_results = {'Libby': ['Gloomhaven board game'], 'Macky': ['Gloomhaven board game'],
                        'Becky': ['Gloomhaven board game'], 'Lecky': ['Gloomhaven board game'],
                        'Mocky': ['Gloomhaven board game'], 'Topy': ['Gloomhaven board game'],
                        'Keira': ['LED light up sneakers', '7200 Riot Points gift card'],
                        'Lexie': ['Mermaid barbie', 'Pink fluffy pen',
                                  'World of Warcraft: Shadowlands Collectors Edition'],
                        'Amelia': ['Wall-mount diamond pickaxe',
                                   'Magic: The Gathering Commander Legends booster box']}
    count = 0
    for name, gifts in wishlist_results.items():
        for child, gift in warehouse.storage.items():
            if name == child.name and gift[0].name != "How to be a good kid by Rafielle E Usher":
                assert child.is_nice is True
                assert gift[0].name in gifts
                count += 1
    assert count == 9


def test_warehouse_storage_has_correct_items_in_storage_only_naughty(receive_data, data_warehouse, factory, warehouse):
    """
    Test if warehouse storage stores correct information that is sent from Factory (only naughty children).

    Children named Tanya, Jamie, Chelsea, Taylor should have "How to be a good kid by Rafielle E Usher" as a gift.
    """
    expected_result = {"Tanya": "How to be a good kid by Rafielle E Usher",
                       "Jamie": "How to be a good kid by Rafielle E Usher",
                       "Chelsea": "How to be a good kid by Rafielle E Usher",
                       "Taylor": "How to be a good kid by Rafielle E Usher"}
    count = 0
    for child, gift in expected_result.items():
        for child_name, gift_name in warehouse.storage.items():
            if child == str(child_name):
                count += 1
                assert gift == str(gift_name[0])
    assert count == 4


def test_search_gifts_from_warehouse(receive_data, data_warehouse, factory, warehouse):
    """
    Test searching gifts from warehouse storage.

    Result should be child (object) and gift as value (object).
    """
    if str(warehouse.search_gifts_from_warehouse("LED light up sneakers")) == "{Keira: LED light up sneakers}":
        assert str(warehouse.search_gifts_from_warehouse("LED light up sneakers")) == "{Keira: LED light up sneakers}"
    if str(warehouse.search_gifts_from_warehouse(
            "7200 Riot Points gift card")) == "{Keira: 7200 Riot Points gift card}":
        assert str(warehouse.search_gifts_from_warehouse(
            "7200 Riot Points gift card")) == "{Keira: 7200 Riot Points gift card}"


"""Test class Logistics."""


def test_sort_gifts_by_country(logistics):
    """
    Test if gifts are sorted by country to the dictionary.

    Countries should be as dictionary keys and gift_lists as values.
    Gifts should be as objects in list and countries as strings.
    """
    logistics.sort_gifts_by_country()
    united_kingdom = ["Gloomhaven board game", "Gloomhaven board game", "Gloomhaven board game",
                      "Gloomhaven board game", "Gloomhaven board game", "Gloomhaven board game",
                      "How to be a good kid by Rafielle E Usher", "How to be a good kid by Rafielle E Usher"]
    germany = ["7200 Riot Points gift card", "LED light up sneakers"]
    canada = ["Mermaid barbie", "Pink fluffy pen", "World of Warcraft: Shadowlands Collectors Edition",
              "How to be a good kid by Rafielle E Usher"]
    south_africa = ["Wall-mount diamond pickaxe", "Magic: The Gathering Commander Legends booster box",
                    "How to be a good kid by Rafielle E Usher"]
    for key, gift_list in logistics.sorted_by_country.items():
        if key == "United Kingdom":
            for gift in gift_list:
                assert gift.name in united_kingdom
                united_kingdom.remove(gift.name)
        if key == "Germany":
            for gift in gift_list:
                assert gift.name in germany
                germany.remove(gift.name)
        if key == "Canada":
            for gift in gift_list:
                assert gift.name in canada
                canada.remove(gift.name)
        if key == "South Africa":
            for gift in gift_list:
                assert gift.name in south_africa
                south_africa.remove(gift.name)


def test_shipment_not_exceed_50kg(logistics):
    """Test if not more than 50kg of gifts are packed to one sledge."""
    logistics.pack_gifts_for_each_country()
    for key, value in logistics.sorted_and_packed.items():
        if key == "United Kingdom":
            assert sum([x.weight_in_grams for x in value[0]]) == 49000
            assert sum([x.weight_in_grams for x in value[1]]) == 20000


def test_pack_gifts_for_each_country_correct_results(logistics):
    """
    Test if gifts are packed correctly according to countries.

    Function pack_gifts_for_each_country() returns sorted_and_packed dict,
    where country is a key (string) and value is list of lists(shipments), where gifts are as objects.
    """
    logistics.pack_gifts_for_each_country()
    united_kingdom = [["How to be a good kid by Rafielle E Usher", "How to be a good kid by Rafielle E Usher",
                       "Gloomhaven board game", "Gloomhaven board game", "Gloomhaven board game",
                       "Gloomhaven board game"], ["Gloomhaven board game", "Gloomhaven board game"]]
    germany = ["7200 Riot Points gift card", "LED light up sneakers"]
    canada = ["Mermaid barbie", "Pink fluffy pen", "World of Warcraft: Shadowlands Collectors Edition",
              "How to be a good kid by Rafielle E Usher"]
    south_africa = ["Wall-mount diamond pickaxe", "Magic: The Gathering Commander Legends booster box",
                    "How to be a good kid by Rafielle E Usher"]
    for country, shipment_list in logistics.sorted_and_packed.items():
        if country == "United Kingdom":
            count_shipment = 0
            for shipment in shipment_list:
                for gift in shipment:
                    assert gift.name in united_kingdom[count_shipment]
                    united_kingdom[count_shipment].remove(gift.name)
                count_shipment += 1
        if country == "Germany":
            assert shipment_list[0][0].name in germany
        if country == "Canada":
            for gift in shipment_list[0]:
                assert gift.name in canada
                canada.remove(gift.name)
        if country == "South Africa":
            for gift in shipment_list[0]:
                assert gift.name in south_africa
                south_africa.remove(gift.name)


def test_create_order_sheet(logistics):
    """
    Test creating order sheet for filling it later.

    All the letters and symbols have to match with the string in "result" variable.
    """
    logistics.pack_gifts_for_each_country()
    result = r"""                        DELIVERY ORDER 1
                                                          _v
                                                     __* (__)
             ff     ff     ff     ff                {\/ (_(__).-.
      ff    <_\__, <_\__, <_\__, <_\__,      __,~~.(`>|-(___)/ ,_)
    o<_\__,  (_ ff ~(_ ff ~(_ ff ~(_ ff~~~~~@ )\/_;-"``     |
      (___)~~//<_\__, <_\__, <_\__, <_\__,    | \__________/|
      // >>     (___)~~(___)~~(___)~~(___)~~~~\\_/_______\_//
                // >>  // >>  // >>  // >>     `'---------'`

FROM: NORTH POLE CHRISTMAS CHEER INCORPORATED
TO: United Kingdom

//========[]==========================================[]==================\\
||  Name  ||                  Gifts                   || Total Weight(kg) ||
|]========[]==========================================[]==================[|"""
    order_sheet = logistics.create_order_sheet(1, "United Kingdom", 6, 40)
    assert order_sheet == result + "\n"


def test_add_deliveries_create_files_and_folder(logistics):
    """Test if delivery_orders folder and delivery_order files are created calling add_deliveries function."""
    logistics.add_deliveries()
    assert os.path.exists("delivery_orders") is True
    assert os.path.isfile("./delivery_orders/delivery_order1.txt")
    assert os.path.isfile("./delivery_orders/delivery_order2.txt")
    assert os.path.isfile("./delivery_orders/delivery_order3.txt")
    assert os.path.isfile("./delivery_orders/delivery_order4.txt")
    assert os.path.isfile("./delivery_orders/delivery_order5.txt")


def test_add_deliveries(logistics):
    """
    Test if name, gifts and weight are placed correctly to the delivery note.

    All the letters and symbols have to match with the string in "result" variable.
    """
    logistics.add_deliveries()
    result = r"""                        DELIVERY ORDER 1
                                                          _v
                                                     __* (__)
             ff     ff     ff     ff                {\/ (_(__).-.
      ff    <_\__, <_\__, <_\__, <_\__,      __,~~.(`>|-(___)/ ,_)
    o<_\__,  (_ ff ~(_ ff ~(_ ff ~(_ ff~~~~~@ )\/_;-"``     |
      (___)~~//<_\__, <_\__, <_\__, <_\__,    | \__________/|
      // >>     (___)~~(___)~~(___)~~(___)~~~~\\_/_______\_//
                // >>  // >>  // >>  // >>     `'---------'`

FROM: NORTH POLE CHRISTMAS CHEER INCORPORATED
TO: United Kingdom

//========[]==========================================[]==================\\
||  Name  ||                  Gifts                   || Total Weight(kg) ||
|]========[]==========================================[]==================[|
|| Tanya  || How to be a good kid by Rafielle E Usher ||              4.5 ||
|| Taylor || How to be a good kid by Rafielle E Usher ||              4.5 ||
|| Libby  ||          Gloomhaven board game           ||             10.0 ||
|| Macky  ||          Gloomhaven board game           ||             10.0 ||
|| Becky  ||          Gloomhaven board game           ||             10.0 ||
|| Lecky  ||          Gloomhaven board game           ||             10.0 ||
\\========[]==========================================[]==================//
 \\=======[]==========================================[]>>>>Total: 49.0kg//"""
    with open("delivery_orders/delivery_order1.txt", "r") as file:
        assert file.read() == result


"""Test class PostOffice."""


def test_decrypt_caesar_cipher(post_office):
    """Test if caesar cipher is decrypted correctly from received letters."""
    letter = 'kviixmrkw xs xli rsvxl tspi!\n\nm eq zivc xlerojyp jsv xli rmgi tviwirxw csy fvsyklx qi pewx ciev, m wxmpp tpec amxl xliq izivc hec!\n\nxlmw ciev, m aerx fvyrixxi fevfmi hspp.\n\nxlero csy,\nlevvc, yrmxih wxexiw sj eqivmge'
    assert post_office.decrypt_caesar_cipher(4,
                                             letter) == 'GREETINGS TO THE NORTH POLE!\n\nI AM VERY THANKFUL FOR THE NICE PRESENTS YOU BROUGHT ME LAST YEAR, I STILL PLAY WITH THEM EVERY DAY!\n\nTHIS YEAR, I WANT BRUNETTE BARBIE DOLL.\n\nTHANK YOU,\nHARRY, UNITED STATES OF AMERICA'


def test_parse_wishes_from_letters_placed_correctly(receive_data, data_warehouse, factory, warehouse, post_office):
    """
    Test parsing letters are placed correctly.

    Letters with wishes should be added to "letters_with_wishes" dict.
    If no wishes are found, letter will be moved to "letters_without_wishes" list.
    """
    post_office.parse_wishes_from_letters(5)
    pattern = r'(?<=I wish for )[^\.]+|(?<=I want )[^\.]+|(?<=wishlist: )[^\.]+|(?<=WISHLIST: )[^\.]+|(?<=I WANT )[^\.]+|(?<=I WISH FOR )[^\.]+'
    for wishes in post_office.letters_with_wishes.values():
        for wish in wishes:
            assert (receive_data.get_gift_info({'gift': wish})[0]["gift"]).lower() == wish.lower()
    for letter in post_office.letters_without_wishes:
        assert re.findall(pattern, letter) == []


def test_parse_wishes_from_letters_parameter_wishes_amount(post_office):
    """
    Test parse_wishes_from_letters function's parameter wishes_amount.

    Parameter wishes_amount describes how many letters with wishes should be added to "letters_with_wishes" dict.
    If parameter is 5, then 5 letters with wishes should be parsed (even if letter is encoded).
    """
    post_office.parse_wishes_from_letters(5)
    assert len(post_office.letters_with_wishes) == 5
    post_office.parse_wishes_from_letters(5)
    assert len(post_office.letters_with_wishes) == 10


def test_parse_wishes_from_letters_parameter_wishes_amount_edges(post_office):
    """
    Test if parse_wishes_from_letters parameter wishes_amount is in range 1-300.

    If wishes_amount is out of range 1-300, return None.
    """
    assert post_office.parse_wishes_from_letters(0) is None
    assert post_office.parse_wishes_from_letters(301) is None
    assert post_office.parse_wishes_from_letters(-1) is None


def test_parse_base64_encoded_letter_without_wishes(post_office):
    """
    Test if base64 encoded letter that has no wishes, is decoded in letters_without_wishes.

    Letter should not be in letters_with_wishes.
    """
    post_office.parse_wishes_from_letters(3)
    post_office.letters_without_wishes = [
        'R3JlZXRpbmdzIHRvIHRoZSBOb3J0aCBQb2xlIQoKSSBzYXcgYW4gZWxmIHRoZSBvdGhlciBkYXksIGhlIHdhcyBqdXN0IG1ha2luZyBpdCBvdXQgdGhyb3VnaCB0aGUgd2luZG93IHdoZW4gSSBzcG90dGVkIGhpbQoKVGhhbmsgeW91LApKdXN0aW4sIFBlcnU=']
    post_office.letters_with_wishes = {}
    post_office.parse_base64_encoded_letters()
    assert post_office.letters_with_wishes == {}
    assert str(
        post_office.letters_without_wishes) == r"['Greetings to the North Pole!\n\nI saw an elf the other day, he was just making it out through the window when I spotted him\n\nThank you,\nJustin, Peru']"


def test_parse_base64_encoded_letter_with_wishes(post_office):
    """
    Test if base64 encoded letter that has wishes and is decoded in letters_with_wishes.

    Letter should not be in letters_without_wishes.
    """
    post_office.parse_wishes_from_letters(3)
    post_office.letters_without_wishes = [
        'RGVhciBtciBhbmQgbXJzIFNhbnRhIQoKSSBzYXcgYW4gZWxmIHRoZSBvdGhlciBkYXksIGhlIHdhcyBqdXN0IG1ha2luZyBpdCBvdXQgdGhyb3VnaCB0aGUgd2luZG93IHdoZW4gSSBzcG90dGVkIGhpbQoKVGhlIGZvbGxvd2luZyBpcyBteSB3aXNobGlzdDogTmVyZiByaWZsZS4KClRoYW5rIHlvdSwKRG9taW5paywgVW5pdGVkIEtpbmdkb20=']
    post_office.letters_with_wishes = {}
    post_office.parse_base64_encoded_letters()
    assert str(post_office.letters_with_wishes) == "{'Dominik': ['Nerf rifle']}"
    assert post_office.letters_without_wishes == []


def test_pick_wishes_from_letters_pick_extra_gift(receive_data, factory, data_warehouse):
    """
    Test if pick_wishes_from_letters function adds extra gift to child.

    As a result, child named "Addison" should get "Mechanical keyboard" as an extra gift.
    Addison will get both "Tablet computer" and "Mechanical keyboard" as gifts.
    """
    warehouse = Warehouse(factory)
    post_office = PostOffice(data_warehouse, receive_data, warehouse)
    addison = Child("Addison", "Estonia", True, ['Tablet computer'])
    gift = Gift('Tablet computer', addison, 2, 5, 250)
    warehouse.storage = {addison: [gift]}
    post_office.letters_with_wishes = {'Addison': ['Tablet computer', 'Mechanical keyboard']}
    post_office.pick_wishes_from_letters()
    assert str(warehouse.storage) == "{Addison: [Tablet computer, Mechanical keyboard]}"


def test_pick_wishes_from_letters_only_nice_children(receive_data, factory, data_warehouse):
    """
    Test if only nice children can get extra gift.

    As a test result, naughty child who has a gift ready in warehouse storage,
    should not get any extra gift.
    """
    warehouse = Warehouse(factory)
    post_office = PostOffice(data_warehouse, receive_data, warehouse)
    tanya_naughty = Child("Tanya", "Estonia", False, ["Nintendo Switch"])
    addison_nice = Child("Addison", "Estonia", True, ['Tablet computer'])
    gift_addison = Gift('Tablet computer', addison_nice, 2, 5, 250)
    gift_tanya = Gift('How to be a good kid by Rafielle E Usher', tanya_naughty, 2, 5, 4500)
    warehouse.storage = {addison_nice: [gift_addison], tanya_naughty: [gift_tanya]}
    post_office.letters_with_wishes = {'Addison': ['Tablet computer', 'Mechanical keyboard'],
                                       'Tanya': ["Nintendo Switch", "Frozen Olaf plush toy"]}
    post_office.pick_wishes_from_letters()
    assert str(
        warehouse.storage) == '{Addison: [Tablet computer, Mechanical keyboard], Tanya: [How to be a good kid by Rafielle E Usher]}'


def test_process_letters(receive_data, data_warehouse, factory):
    """
    Test executes process_letters function, triggering all the other functions under PostOffice class and modifies warehouse storage dict.

    process_letters function will call these functions from PostOffice class:
    decrypt_caesar_cipher()
    parse_wishes_from_letters(letters_amount)
    parse_base64_encoded_letters()
    pick_wishes_from_letters()

    As a result, warehouse storage dict should be modified.
    It should have "[Tablet computer, Mechanical keyboard]" list in its values.
    """
    warehouse = Warehouse(factory)
    post_office = PostOffice(data_warehouse, receive_data, warehouse)
    addison = Child("Addison", "Estonia", True, ['Tablet computer'])
    gift_addison = Gift('Tablet computer', addison, 2, 5, 250)
    warehouse.storage.setdefault(addison, [gift_addison])
    post_office.process_letters(300)
    assert "[Tablet computer, Mechanical keyboard]" in str(list(warehouse.storage.values()))


def test_letters_without_wishes_dict(post_office):
    """
    Test if correct letters are in letters_without_wishes list after processing letters.

    After processing letters, letters_without_wishes list shouldn't have any letters with wishes.
    All the letters should be decoded too.
    """
    post_office.process_letters(50)
    pattern1 = r'I wish for |I want |wishlist: |WISHLIST: |I WANT |I WISH FOR '
    pattern2 = r'santa|SANTA|Santa|greetings|Greetings|GREETINGS'
    for letter in post_office.letters_without_wishes:
        find_wishes = re.findall(pattern1, letter)
        find_match = re.findall(pattern2, letter)
        assert find_match
        assert find_wishes == []


def test_add_deliveries_if_extra_gift(receive_data, data_warehouse, factory):
    """
    Test if all the deliveries are placed correctly to the delivery note if extra gift is added to child.

    As a result "Keira" should have two gifts in delivery note.
    """
    warehouse = Warehouse(factory)
    post_office = PostOffice(data_warehouse, receive_data, warehouse)
    logistics = Logistics(warehouse)
    addison = Child("Addison", "Estonia", True, ['Tablet computer'])
    gift_addison = Gift('Tablet computer', addison, 2, 5, 250)
    warehouse.storage.setdefault(addison, [gift_addison])
    post_office.process_letters(300)
    logistics.add_deliveries()
    result = r"""                        DELIVERY ORDER 3
                                                          _v
                                                     __* (__)
             ff     ff     ff     ff                {\/ (_(__).-.
      ff    <_\__, <_\__, <_\__, <_\__,      __,~~.(`>|-(___)/ ,_)
    o<_\__,  (_ ff ~(_ ff ~(_ ff ~(_ ff~~~~~@ )\/_;-"``     |
      (___)~~//<_\__, <_\__, <_\__, <_\__,    | \__________/|
      // >>     (___)~~(___)~~(___)~~(___)~~~~\\_/_______\_//
                // >>  // >>  // >>  // >>     `'---------'`

FROM: NORTH POLE CHRISTMAS CHEER INCORPORATED
TO: Germany

//=======[]===================================================[]==================\\
||  Name ||                       Gifts                       || Total Weight(kg) ||
|]=======[]===================================================[]==================[|
|| Keira || 7200 Riot Points gift card, LED light up sneakers ||             0.01 ||
\\=======[]===================================================[]==================//
 \\======[]===================================================[]>>>>>Total: 0.0kg//"""
    with open("delivery_orders/delivery_order3.txt", "r") as file:
        assert file.read() == result
