"""Santa's Workshop."""


import csv
import os
import random
import shutil
import urllib.parse
from aiohttp import ClientSession
import asyncio
import urllib.request
import requests
import re
import base64


class ReceiveData:
    """
    Receive important data about children and gifts.

    This is the place where nice list, naughty list and wishlist are parsed.
    Also gift information is received from the database (server).
    """

    def update_csv_files(self):
        """Receive the latest nice list, naughty list and wish list from server."""
        urllib.request.urlretrieve("https://iti0102-2020.pages.taltech.ee/info/files/ex15_nice_list.csv",
                                   "ex15_nice_list.csv")
        urllib.request.urlretrieve("https://iti0102-2020.pages.taltech.ee/info/files/ex15_naughty_list.csv",
                                   "ex15_naughty_list.csv")
        urllib.request.urlretrieve("https://iti0102-2020.pages.taltech.ee/info/files/ex15_wish_list.csv",
                                   "ex15_wish_list.csv")

    def get_data_from_file(self, filename: str, data_dict: dict) -> None:
        """
        Read information from nice list, naughty list and wishlist.

        All the information will be added to dictionary in same order as in csv file.
        Which children will receive (or not) certain gift, depends on that information.
        """
        with open(filename, "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            for rows in csv_reader:
                data_dict.setdefault(rows[0], [x.strip() for x in rows[1:]])

    def get_gift_info(self, produced_gifts: dict) -> list:
        """
        Get information for each gift.

        This information is important for Factory (gift production) and logistics.
        Result is a list of gifts (dicts) with all the attributes.
        """
        list_of_gifts = list(produced_gifts.values())
        sites = []
        for gift in list_of_gifts:
            data = {'name': gift}
            url_value = urllib.parse.urlencode(data)
            sites.append('https://cs.ttu.ee/services/xmas/gift?' + url_value)

        async def get_sites(sites):
            tasks = [asyncio.create_task(fetch_site(s)) for s in sites]
            return await asyncio.gather(*tasks)

        async def fetch_site(url):
            async with ClientSession() as session:
                async with session.get(url) as resp:
                    data = await resp.json()
            return data
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        data = asyncio.run(get_sites(sites))
        return data


class DataWarehouse:
    """All the important data received from Department of Gift Allocation is kept in DataWarehouse."""

    def __init__(self, receive_data: ReceiveData, nice_list_file: str, naughty_list_file: str, wishlist_file: str):
        """
        Initialize the DataWarehouse class.

        Here nice list, naughty list and wishlist will be automatically parsed to separate dictionaries.
        :param receive_data:
        :param nice_list_file:
        :param naughty_list_file:
        :param wishlist_file:
        """
        self.nice_list = {}
        self.naughty_list = {}
        self.wishlists = {}
        self.children = []
        receive_data.get_data_from_file(nice_list_file, self.nice_list)
        receive_data.get_data_from_file(naughty_list_file, self.naughty_list)
        receive_data.get_data_from_file(wishlist_file, self.wishlists)

    def add_attributes_to_children(self) -> None:
        """
        Add Child objects with attributes to children list.

        Child object will get name, country, wishlist and whether the child is in nice list or not.
        Nice and naughty lists will be merged.
        Function uses data from nice list, naughty list and wishlist.
        No gifts will be sent out if there isn't any nice children and no wishlists,
        so if there is only information about naughty children then they will not receive any gifts.
        All the children should be added to children list which is in the DataWarehouse.
        """
        if self.wishlists and self.nice_list:
            merge_dicts = self.nice_list.copy()
            merge_dicts.update(self.naughty_list)
            for name, country in merge_dicts.items():
                if name in self.nice_list:
                    self.children.append(Child(name, country[0], True, self.wishlists[name]))
                else:
                    self.children.append(Child(name, country[0], False, self.wishlists[name]))


class Child:
    """
    Create Child object.

    Child object has name, country, whether the child is in nice list or not and wishlist.
    """

    def __init__(self, name: str, country: str, is_nice: bool, wishlist: list):
        """Initialize the Child class.

        :param name:
        :param country:
        :param is_nice:
        :param wishlist:
        """
        self.name = name
        self.country = country
        self.is_nice = is_nice
        self.wishlist = wishlist

    def __repr__(self):
        """Child representation."""
        return self.name


class Gift:
    """
    Create Gift object.

    Every gift has name, receiver, material_cost, production_time, weight_in_grams.
    """

    def __init__(self, name: str, receiver: object, material_cost: int, production_time: int, weight_in_grams: int):
        """Initialize the Gift class.

        :param name:
        :param receiver:
        :param material_cost:
        :param production_time:
        :param weight_in_grams:
        """
        self.name = name
        self.receiver = receiver
        self.material_cost = material_cost
        self.production_time = production_time
        self.weight_in_grams = weight_in_grams

    def __repr__(self):
        """Gift representation as a string."""
        return self.name


class Factory:
    """
    Factory is the place where the gifts are produced.

    Gifts are produced according to the children wishlists.
    For each child, one gift (randomly picked) will be produced from the wishlist.
    Eventually produced gifts with all the needed attributes should be found in gifts_with_attributes dict
    """

    def __init__(self, data_warehouse: DataWarehouse, receive_data: ReceiveData):
        """Initialize the Factory class.

        :param data_warehouse:
        :param receive_data:
        """
        self.wishlists = data_warehouse.wishlists
        self.nice_list = data_warehouse.nice_list
        self.naughty_list = data_warehouse.naughty_list
        self.children = data_warehouse.children
        self.data_warehouse = data_warehouse
        self.receive_data = receive_data
        self.gifts_with_attributes = {}

    def produce_gifts_for_children(self, nice_children: dict, naughty_children: dict) -> None:
        """
        One gift for each child will be produced.

        Each child from nice list will have one randomly picked gift (from wishlist).
        Every child from naughty list will have a special book assigned as a gift.
        """
        self.data_warehouse.add_attributes_to_children()
        for child in self.children:
            if child.is_nice is True:
                gift = random.choice(self.wishlists[child.name])
                nice_children.setdefault(child, gift)
            if child.is_nice is False:
                gift_naughty = Gift('How to be a good kid by Rafielle E Usher', child, 2, 5, 4500)
                naughty_children.setdefault(child, [gift_naughty])

    def add_received_gift_information(self) -> None:
        """
        All the produced gifts will be marked with child's name.

        This is the place where important information will be added to gift for better logistics.
        Every produced gift will receive production related information and receiver.
        Every gift will have its gift name: str, receiver_name: object, material cost:int, production time: int
        and weight_in_grams: int.
        """
        result = {}
        nice = {}
        naughty = {}
        self.produce_gifts_for_children(nice, naughty)
        get_gift_attributes = self.receive_data.get_gift_info(nice)
        nice_copy = nice.copy()
        for gift in get_gift_attributes:
            for key, value in nice_copy.items():
                if gift["gift"] == value:
                    result.setdefault(key,
                                      [Gift(list(gift.values())[0], key, list(gift.values())[1], list(gift.values())[2], list(gift.values())[3])])
                nice_copy.pop(key)
                break
        result.update(naughty)
        self.gifts_with_attributes = result


class Warehouse:
    """
    All the gifts that are produced in factory, will be sent to here.

    All the gifts will be placed on the shelves with all the needed information about the child and gift.
    This is the place where all the gifts are picked.
    """

    def __init__(self, factory: Factory):
        """Initialize the Warehouse class.

        :param factory:
        """
        factory.add_received_gift_information()
        self.storage = factory.gifts_with_attributes

    def search_gifts_from_warehouse(self, gift: str) -> dict:
        """
        Search gifts by name from warehouse.

        Result will be child (receiver) and gift's name as a dictionary.
        """
        result = {}
        for key, values in self.storage.items():
            gifts = [x.name.lower() for x in values]
            if gift.lower() in gifts:
                result.setdefault(key, gift)
        return result


class Logistics:
    """
    Logistics department will take care of sending out the gifts.

    Logistics make sure that all the gifts will be picked from the warehouse storage, packed and sent to children.
    Shipments are separated by country and each shipment (to certain country) is saved as a list.
    Delivery order sheets are created for each shipment.
    """

    def __init__(self, warehouse: Warehouse):
        """Initialize the Logistics class.

        :param warehouse:
        """
        self.storage = warehouse.storage
        self.sorted_by_country = {}
        self.sorted_and_packed = {}

    def sort_gifts_by_country(self) -> dict:
        """
        Sort gifts by country.

        Countries should be as dictionary keys and gift_lists as values.
        Gifts should be as objects in list and countries as strings.
        """
        for name, gift in self.storage.items():
            for gft in gift:
                self.sorted_by_country.setdefault(gift[0].receiver.country, []).append(gft)
        return self.sorted_by_country

    def pack_gifts_for_each_country(self) -> dict:
        """
        Pack the shipments to sledge (max capacity 50kg).

        Transport costs are high at the moment, therefore sledges should be packed as full as possible, but
        it is important not to exceed 50kg limit for each shipment.
        """
        self.sort_gifts_by_country()
        total_weight = 0
        result = {}
        for country, gifts in self.sorted_by_country.items():
            gifts_sorted = sorted(gifts, key=lambda x: x.weight_in_grams)
            shipments_to_one_country = []
            for gift in gifts_sorted:
                if (total_weight + gift.weight_in_grams) <= 50000:
                    total_weight += gift.weight_in_grams
                    shipments_to_one_country.append(gift)
                if (total_weight + gift.weight_in_grams) > 50000:
                    result.setdefault(country, []).append(shipments_to_one_country)
                    total_weight = 0
                    shipments_to_one_country = []
            result.setdefault(country, []).append(shipments_to_one_country)
        self.sorted_and_packed = result
        return self.sorted_and_packed

    def create_order_sheet(self, delivery_order_number: int, country: str, max_len_name: int, max_len_gift_name: int) -> str:
        """
        Create delivery order sheet for adding gifts information later.

        Order sheets are separated by countries.
        One country can have multiple order sheets.
        """
        order_sheet = f"                        DELIVERY ORDER {delivery_order_number}"
        order_sheet += r"""
                                                          _v
                                                     __* (__)
             ff     ff     ff     ff                {\/ (_(__).-.
      ff    <_\__, <_\__, <_\__, <_\__,      __,~~.(`>|-(___)/ ,_)
    o<_\__,  (_ ff ~(_ ff ~(_ ff ~(_ ff~~~~~@ )\/_;-"``     |
      (___)~~//<_\__, <_\__, <_\__, <_\__,    | \__________/|
      // >>     (___)~~(___)~~(___)~~(___)~~~~\\_/_______\_//
                // >>  // >>  // >>  // >>     `'---------'`"""

        order_sheet += "\n\nFROM: NORTH POLE CHRISTMAS CHEER INCORPORATED"
        order_sheet += f"\nTO: {country}\n"
        order_sheet += "\n//".ljust(max_len_name + 5, "=") + "[]".ljust(max_len_gift_name + 4, "=") + "[]".ljust(20, "=") + r"\\""\n"
        order_sheet += "||" + "Name".center(max_len_name + 2) + "||" + "Gifts".center(max_len_gift_name + 2) + "||" + "Total Weight(kg)".center(18) + "||\n"
        order_sheet += "|]".ljust(max_len_name + 4, "=") + "[]".ljust(max_len_gift_name + 4, "=") + "[]".ljust(20, "=") + "[|\n"
        return order_sheet

    def max_gifts_len_multi(self, gift_list_input: list) -> int:
        """Return gifts names (strings) length for creating table."""
        result = []
        for a in gift_list_input:
            name = a.receiver.name
            result.append(sum([len(x.name) for x in gift_list_input if x.receiver.name == name]))
        if result:
            return max(result)
        else:
            return 0

    def add_deliveries(self) -> None:
        """
        Add deliveries by country to delivery order sheets.

        Every delivery order consists maximum 50kg of gifts.
        Order sheet contains child's name, gifts and total weight.
        That sheet will be attached to the sledge.
        Gift's weight_in_grams is divided by 1000 (weight unit is kg).
        """
        if os.path.exists("delivery_orders"):
            shutil.rmtree("delivery_orders")
        if not os.path.exists("delivery_orders"):
            os.makedirs("delivery_orders")
        self.pack_gifts_for_each_country()
        delivery_order_number = 1
        names_count = []
        for country, gifts in self.sorted_and_packed.items():
            for gift_list in gifts:
                total_weight = 0
                if len(gift_list) > 0:
                    max_len_name = max([len(x.receiver.name) for x in list(gift_list)])
                    max_len_gift_name = max([len(x.name) for x in list(gift_list)])
                    max_len_name_multi = self.max_gifts_len_multi(gift_list)
                    if max_len_gift_name < max_len_name_multi:
                        max_len_gift_name = (max_len_name_multi + 2)
                    blank_sheet = self.create_order_sheet(delivery_order_number, country, max_len_name,
                                                          max_len_gift_name)
                    for gift in gift_list:
                        if gift.receiver.name in names_count:
                            continue
                        names_count.append(gift.receiver.name)
                        name = gift.receiver.name
                        gifts_per_child = [x.name for x in gift_list if x.receiver.name == name]
                        total_weight += (gift.weight_in_grams / 1000)
                        blank_sheet += "||" + gift.receiver.name.center(max_len_name + 2) + "||" + ", ".join(gifts_per_child).center(max_len_gift_name + 2) + "|| " + str(gift.weight_in_grams / 1000).rjust(16) + " ||\n"
                    blank_sheet += r"\\".ljust(max_len_name + 4, "=") + "[]".ljust(max_len_gift_name + 4, "=") + \
                                   "[]".ljust(20, "=") + "//" + "\n"
                    blank_sheet += r" \\".ljust(max_len_name + 4, "=") + "[]".ljust(max_len_gift_name + 4, "=") + \
                                   "[]" + f"Total: {round(total_weight, 1)}kg".rjust(17, ">") + "//"
                    f = open(f"delivery_orders/delivery_order{delivery_order_number}.txt", "w")
                    f.write(blank_sheet)
                    delivery_order_number += 1


class PostOffice:
    """
    Parse sent letters and find out if there are gift wishes written by children.

    Letters will be divided to letters_with_wishes (dictionary) and letters_without_wishes (list).
    All the letters that are encoded (Caesar cipher or Base64), will be decoded.
    If child is nice, one extra wish from
    """

    def __init__(self, data: DataWarehouse, receive_data: ReceiveData, warehouse: Warehouse):
        """
        Initialize class PostOffice.

        Letters will be divided by:
        letters_with_wishes (dictionary) and letters_without_wishes (list)
        """
        self.data = data
        self.receive_data = receive_data
        self.warehouse = warehouse
        self.letters_with_wishes = {}
        self.letters_without_wishes = []

    def decrypt_caesar_cipher(self, shift, message) -> str:
        """Decrypt letter in Caesar cipher."""
        message = message.upper()
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        result = ""

        for letter in message:
            if letter in alphabet:
                letter_index = (alphabet.find(letter) - shift) % len(alphabet)
                result = result + alphabet[letter_index]
            else:
                result = result + letter
        return result

    def parse_wishes_from_letters(self, wishes_amount: int) -> None:
        """
        Collect letters with wishes and add these to the "letters_with_wishes" dict.

        Function takes how many letters with wishes should be parsed as a parameter.
        Only letters with wishes will be picked and added to the "letters_with_wishes".
        If no wishes are found, letter will be moved to "letters_without_wishes" list.
        Letters with caesar cipher will be moved to "letters_without_wishes" list as well,
        if there isn't any wishes in these letters.
        All the letters that are encrypted in caesar cipher,
        should be decrypted before adding these to the "letters_without_wishes" list or
        "letters_with_wishes" dict.
        Parameter wishes_amount can be in range 1-300.
        """
        if 0 < wishes_amount <= 300:
            s = requests.Session()
            while True:
                r = s.get("https://cs.ttu.ee/services/xmas/letter")
                pattern = r'(?<=I wish for )[^\.]+|(?<=I want )[^\.]+|(?<=wishlist: )[^\.]+|(?<=WISHLIST: )[^\.]+|(?<=I WANT )[^\.]+|(?<=I WISH FOR )[^\.]+'
                wishes_match = re.findall(pattern, r.json()["letter"])
                decrypted_letter = self.decrypt_caesar_cipher(4, r.json()["letter"])
                decrypted_wishes = re.findall(pattern, decrypted_letter)
                if wishes_match or decrypted_wishes:
                    name = r.json()["letter"].split(",")[-2][1:]
                    if name not in self.letters_with_wishes:
                        if wishes_match:
                            self.letters_with_wishes.setdefault(r.json()["letter"].split(",")[-2][1:], [x.strip() for x in wishes_match[0].split(",")])
                            wishes_amount -= 1
                        if decrypted_wishes and not wishes_match:
                            self.letters_with_wishes.setdefault((decrypted_letter.split(",")[-2][1:]).capitalize(),
                                                                [x.strip().capitalize() for x in decrypted_wishes[0].split(",")])
                            wishes_amount -= 1
                        if wishes_amount == 0:
                            break
                else:
                    if "SANTA" in decrypted_letter or "GREETINGS" in decrypted_letter:
                        self.letters_without_wishes.append(decrypted_letter)
                    else:
                        self.letters_without_wishes.append(r.json()["letter"])
        else:
            return None

    def parse_base64_encoded_letters(self) -> None:
        """
        Decode letters with Base64 encoding.

        Letters with Base64 encoding will be moved to "letters_without_wishes" list,
        if there isn't any wishes in these letters.
        If there are wishes in letter, it will be moved to letters_with_wishes.
        """
        pattern = r'(?<=I wish for )[^\.]+|(?<=I want )[^\.]+|(?<=wishlist: )[^\.]+|(?<=WISHLIST: )[^\.]+|(?<=I WANT )[^\.]+|(?<=I WISH FOR )[^\.]+'
        pattern2 = r'santa|greetings'
        letters_without_wishes_copy = self.letters_without_wishes.copy()
        for letter in letters_without_wishes_copy:
            find_santa_greetings = re.findall(pattern2, letter.lower())
            if not find_santa_greetings:
                base64_decoded = str(base64.b64decode(letter), 'UTF-8')
                match_wishes = re.findall(pattern, base64_decoded)
                if match_wishes:
                    self.letters_with_wishes.setdefault(base64_decoded.split(",")[-2][1:],
                                                        [x.strip() for x in match_wishes[0].split(",")])
                    self.letters_without_wishes.remove(letter)
                else:
                    self.letters_without_wishes.remove(letter)
                    self.letters_without_wishes.append(base64_decoded)

    def pick_wishes_from_letters(self) -> None:
        """
        Pick wishes from letters and add these as extra gifts for children.

        Only nice children will get extra gift (one gift).
        Extra gifts receive only children (nice),
        who already have one randomly picked gift in warehouse storage.
        Extra gifts are not produced in factory and these can be picked directly from secret place in warehouse.
        A child cannot have two same gifts.
        """
        result = {}
        for key, value in self.letters_with_wishes.items():
            for child, wish in self.warehouse.storage.items():
                extra_gift = [x for x in value if x.lower() != wish[0].name.lower()]
                if key == child.name and len(extra_gift) > 0 and child.is_nice:
                    gift_info = self.receive_data.get_gift_info({child: extra_gift[0]})
                    result.setdefault(child,
                                      Gift(list(gift_info)[0]["gift"], child, list(gift_info)[0]["material_cost"],
                                           list(gift_info)[0]["production_time"], list(gift_info)[0]["weight_in_grams"]))
        for key, value in result.items():
            for child, gift in self.warehouse.storage.items():
                if key.name == child.name:
                    gift.append(value)

    def process_letters(self, letters_amount):
        """
        Process received letters, decode them and add extra gift for the children, if they are nice.

        This function calls all the other functions under PostOffice class and modifies warehouse storage dict.
        """
        self.parse_wishes_from_letters(letters_amount)
        self.parse_base64_encoded_letters()
        self.pick_wishes_from_letters()


# if __name__ == '__main__':
#     receive_data = ReceiveData()
#     # receive_data.update_csv_files()
#     data_warehouse = DataWarehouse(receive_data, "ex15_nice_list.csv", "ex15_naughty_list.csv",
#                                    "ex15_wish_list.csv")
#     factory = Factory(data_warehouse, receive_data)
#     warehouse = Warehouse(factory)
#     post_office = PostOffice(data_warehouse, receive_data, warehouse)
#     # post_office.pick_wishes_from_letters(150)
#     post_office.process_letters(150)
#     logistics = Logistics(warehouse)
#     warehouse.search_gifts_from_warehouse("7200 Riot Points gift card")
#     logistics.add_deliveries()
