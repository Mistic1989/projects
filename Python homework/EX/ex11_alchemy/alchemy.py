"""Alchemy."""


class AlchemicalElement:
    """
    AlchemicalElement class.

    Every element must have a name.
    """

    def __init__(self, name: str):
        """Initialize the AlchemicalElement class."""
        self.name = name

    def __repr__(self):
        """Representation of AlchemicalElement."""
        return f"<AE: {self.name}>"

    def __lt__(self, other):
        """Compare objects."""
        return self.name < other.name


class AlchemicalStorage:
    """AlchemicalStorage class."""

    def __init__(self):
        """
        Initialize the AlchemicalStorage class.

        You will likely need to add something here, maybe a list?
        """
        self.storage_list = []

    def add(self, element: AlchemicalElement):
        """
        Add element to storage.

        Check that the element is an instance of AlchemicalElement, if it is not, raise the built-in TypeError exception.

        :param element: Input object to add to storage.
        """
        if isinstance(element, AlchemicalElement):
            return self.storage_list.append(element)
        else:
            raise TypeError

    def pop(self, element_name: str) -> AlchemicalElement or None:
        """
        Remove and return previously added element from storage by its name.

        If there are multiple elements with the same name, remove only the one that was added most recently to the
        storage. If there are no elements with the given name, do not remove anything and return None.

        :param element_name: Name of the element to remove.
        :return: The removed AlchemicalElement object or None.
        """
        for item in self.storage_list[::-1]:
            if item.name == element_name:
                self.storage_list.remove(item)
                return item

        return None

    def extract(self) -> list[AlchemicalElement]:
        """
        Return a list of all of the elements from storage and empty the storage itself.

        Order of the list must be the same as the order in which the elements were added.

        Example:
            storage = AlchemicalStorage()
            storage.add(AlchemicalElement('Water'))
            storage.add(AlchemicalElement('Fire'))
            storage.extract() # -> [<AE: Water>, <AE: Fire>]
            storage.extract() # -> []

        In this example, the second time we use .extract() the output list is empty because we already extracted
         everything.

        :return: A list of all of the elements that were previously in the storage.
        """
        storage_items = self.storage_list.copy()
        self.storage_list.clear()
        return storage_items

    def get_content(self) -> str:
        """
        Return a string that gives an overview of the contents of the storage.

        Example:
            storage = AlchemicalStorage()
            storage.add(AlchemicalElement('Water'))
            storage.add(AlchemicalElement('Fire'))
            print(storage.get_content())

        Output in console:
            Content:
             * Fire x 1
             * Water x 1

        The elements must be sorted alphabetically by name.

        :return: Content as a string.
        """
        if len(self.storage_list) > 0:
            content_as_dict = {}
            for item in self.storage_list:
                content_as_dict.setdefault(item.name, []).append(item)
            result_str = "Content:\n"
            sorted_content_names = sorted(list(content_as_dict.keys()))
            for key in sorted_content_names:
                if sorted_content_names.index(key) != len(sorted_content_names) - 1:
                    result_str += f" * {key} x {len(content_as_dict[key])}\n"
                if sorted_content_names.index(key) == len(sorted_content_names) - 1:
                    result_str += f" * {key} x {len(content_as_dict[key])}"
            return result_str
        else:
            return "Content:\n Empty."


class AlchemicalRecipes:
    """AlchemicalRecipes class."""

    def __init__(self):
        """
        Initialize the AlchemicalRecipes class.

        Add whatever you need to make this class function.
        """
        self.recipes = {}

    def add_recipe(self, first_component_name: str, second_component_name: str, product_name: str):
        """
        Determine if recipe is valid and then add it to recipes.

        A recipe consists of three strings, two components and their product.
        If any of the parameters are the same, raise the 'DuplicateRecipeNamesException' exception.
        If there already exists a recipe for the given pair of components, raise the 'RecipeOverlapException' exception.

        :param first_component_name: The name of the first component element.
        :param second_component_name: The name of the second component element.
        :param product_name: The name of the product element.
        """
        for component_pair in self.recipes.values():
            if sorted([first_component_name, second_component_name]) == sorted(component_pair):
                raise RecipeOverlapException(Exception)
        if first_component_name != second_component_name and product_name != first_component_name and \
                product_name != second_component_name:
            self.recipes.setdefault(product_name, [first_component_name, second_component_name])
        else:
            raise DuplicateRecipeNamesException(Exception)

    def get_product_name(self, first_component_name: str, second_component_name: str) -> str or None:
        """
        Return the name of the product for the two components.

        The order of the first_component_name and second_component_name is interchangeable, so search for combinations
        of (first_component_name, second_component_name) and (second_component_name, first_component_name).

        If there are no combinations for the two components, return None

        Example:
            recipes = AlchemicalRecipes()
            recipes.add_recipe('Water', 'Wind', 'Ice')
            recipes.get_product_name('Water', 'Wind')  # ->  'Ice'
            recipes.get_product_name('Wind', 'Water')  # ->  'Ice'
            recipes.get_product_name('Fire', 'Water')  # ->  None
            recipes.add_recipe('Water', 'Fire', 'Steam')
            recipes.get_product_name('Fire', 'Water')  # ->  'Steam'

        :param first_component_name: The name of the first component element.
        :param second_component_name: The name of the second component element.
        :return: The name of the product element or None.
        """
        for product, components in self.recipes.items():
            if sorted(components) == sorted([first_component_name, second_component_name]):
                return product
            else:
                continue
        return None

    def get_component_names(self, product_name: str) -> tuple[str, str] or None:
        """Return components as tuple."""
        for product, components in self.recipes.items():
            if product_name == product:
                return tuple(components)
            else:
                continue
        return None


class DuplicateRecipeNamesException(Exception):
    """Raised when attempting to add a recipe that has same names for components and product."""


class RecipeOverlapException(Exception):
    """Raised when attempting to add a pair of components that is already used for another existing recipe."""


class Cauldron(AlchemicalStorage):
    """
    Cauldron class.

    Extends the 'AlchemicalStorage' class.
    """

    def __init__(self, recipes: AlchemicalRecipes):
        """Initialize the Cauldron class."""
        super().__init__()
        self.recipes = recipes

    def catalyst_decrease_uses(self, item, element, product_name):
        """Decrease uses count if possible.

        If there is Catalyst object, reduce uses count.
        """
        if isinstance(item, Catalyst):
            if item.uses > 0:
                item.uses -= 1
        if isinstance(element, Catalyst):
            if element.uses > 0:
                element.uses -= 1
        self.storage_list.append(element)
        return self.storage_list.append(AlchemicalElement(product_name))

    def catalyst_decrease_uses_multiple(self, item, element):
        """Decrease uses count if possible.

        It used when searching multiple combinations.
        """
        if isinstance(item, Catalyst):
            if item.uses > 0:
                item.uses -= 1
        else:
            self.storage_list.remove(item)
        if isinstance(element, Catalyst):
            if element.uses > 0:
                element.uses -= 1

    def search_component_pair(self, component_pair, element):
        """Search through components."""
        if element.name in component_pair:
            for component in component_pair:
                if component != element.name:
                    return component

    def reduce_item_uses(self, item, product_name):
        """Reduce item uses count in storage."""
        item.uses -= 1
        return self.storage_list.append(AlchemicalElement(product_name))

    def multiple_combinations(self, element):
        """Search multiple combinations."""
        for product_name, component_pair in self.recipes.recipes.items():
            for item in self.storage_list[::-1]:
                if sorted([item.name, element.name]) == sorted(component_pair):
                    self.catalyst_decrease_uses_multiple(item, element)
                    element = AlchemicalElement(product_name)
        return self.storage_list.append(element)

    def check_if_new_product_in_components(self) -> bool:
        """Check if just created product is in one of the recipe's components."""
        for key, value_list in self.recipes.recipes.items():
            for value_pair in self.recipes.recipes.values():
                if key in value_pair:
                    return True
        else:
            return False

    def remove_item_and_append_product(self, item, product_name):
        """Remove item from storage and append new product."""
        self.storage_list.remove(item)
        return self.storage_list.append(AlchemicalElement(product_name))

    def check_conditions(self, element, item, product_name):
        """Check if added element is instance of Catalyst and if it has zero uses.

        If storage item has been used and it's uses count is above zero, reduce uses count.
        """
        if isinstance(element, Catalyst) and element.uses == 0:
            return self.storage_list
        if item.uses > 0:
            return self.reduce_item_uses(item, product_name)
        else:
            return None

    def add(self, element: AlchemicalElement):
        """
        Add element to storage and check if it can combine with anything already inside.

        Use the 'recipes' object that was given in the constructor to determine the combinations.

        Example:
            recipes = AlchemicalRecipes()
            recipes.add_recipe('Water', 'Wind', 'Ice')
            cauldron = Cauldron(recipes)
            cauldron.add(AlchemicalElement('Water'))
            cauldron.add(AlchemicalElement('Wind'))
            cauldron.extract() # -> [<AE: Ice>]

        :param element: Input object to add to storage.
        """
        if isinstance(element, AlchemicalElement):
            for product_name, component_pair in self.recipes.recipes.items():
                component = self.search_component_pair(component_pair, element)
                for item in self.storage_list[::-1]:
                    if item.name == component:
                        if self.check_if_new_product_in_components() is True:
                            return self.multiple_combinations(element)
                        if isinstance(item, Catalyst):
                            if isinstance(element, Catalyst) and element.uses > 0 and item.uses > 0:
                                self.catalyst_decrease_uses(item, element, product_name)
                            if self.check_conditions(element, item, product_name) is not None:
                                return self.check_conditions(element, item, product_name)
                            if isinstance(element, Catalyst) is False:
                                continue
                            break
                        return self.remove_item_and_append_product(item, product_name)
            return self.storage_list.append(element)
        else:
            raise TypeError


class Catalyst(AlchemicalElement):
    """Catalyst class."""

    def __init__(self, name: str, uses: int):
        """
        Initialize the Catalyst class.

        :param name: The name of the Catalyst.
        :param uses: The number of uses the Catalyst has.
        """
        super().__init__(name)
        self.name = name
        self.uses = uses

    def __repr__(self) -> str:
        """
        Representation of the Catalyst class.

        Example:
            catalyst = Catalyst("Philosophers' stone", 3)
            print(catalyst) # -> <C: Philosophers' stone (3)>

        :return: String representation of the Catalyst.
        """
        return f"<C: {self.name} ({self.uses})>"


class Purifier(AlchemicalStorage):
    """
    Purifier class.

    Extends the 'AlchemicalStorage' class.
    """

    def __init__(self, recipes: AlchemicalRecipes):
        """Initialize the Purifier class."""
        super().__init__()
        self.recipes = recipes

    def add(self, element: AlchemicalElement):
        """
        Add element to storage and check if it can be split into anything.

        Use the 'recipes' object that was given in the constructor to determine the combinations.

        Example:
            recipes = AlchemicalRecipes()
            recipes.add_recipe('Water', 'Wind', 'Ice')
            purifier = Purifier(recipes)
            purifier.add(AlchemicalElement('Ice'))
            purifier.extract() # -> [<AE: Water>, <AE: Wind>]   or  [<AE: Wind>, <AE: Water>]

        :param element: Input object to add to storage.
        """
        if isinstance(element, AlchemicalElement):
            for product_name, component_pair in self.recipes.recipes.items():
                has_multiple_combinations = []
                if product_name == element.name:
                    for item in component_pair:
                        if item in self.recipes.recipes.keys():
                            component_copy = component_pair
                            component_copy.remove(item)
                            has_multiple_combinations.append(component_copy[0])
                            self.add(AlchemicalElement(item))
                    if len(has_multiple_combinations) > 0:
                        for component_name in has_multiple_combinations:
                            self.storage_list.append(AlchemicalElement(component_name))
                        return self.storage_list
                    else:
                        for component in self.recipes.get_component_names(product_name):
                            self.storage_list.append(AlchemicalElement(component))
                    return self.storage_list
                else:
                    continue
            return self.storage_list.append(element)
        else:
            raise TypeError


if __name__ == '__main__':
    recipes = AlchemicalRecipes()
    purifier = Purifier(recipes)
    recipes.add_recipe('Earth', 'Fire', 'Iron')
    recipes.add_recipe("Philosophers' stone", 'Iron', 'Silver')
    recipes.add_recipe("Philosophers' stone", 'Silver', 'Gold')
    recipes.add_recipe('Iron', 'Crystal', 'Talisman')
    # ((Earth + Fire) + Philosophers' stone) + Philosophers' stone) = Gold

    cauldron = Cauldron(recipes)
    cauldron.add(Catalyst("Philosophers' stone", 2))
    cauldron.add(AlchemicalElement('Fire'))
    cauldron.get_content()
    # Content:
    #  * Fire x 1
    #  * Philosophers' stone x 1

    cauldron.add(AlchemicalElement('Earth'))
    print(cauldron.extract())  # -> [<C: Philosophers' stone (0)>, <AE: Gold>]

    purifier.add(AlchemicalElement('Talisman'))
    purifier.add(AlchemicalElement('Gold'))
    print(purifier.extract())  # -> [<AE: Earth>, <AE: Fire>, <AE: Crystal>]  (in any order)
