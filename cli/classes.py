"""Classes for managing warehouse, items in stock, and user."""


class MissingArgument(Exception):
    def __init__(self, argument: str, message: str):
        self.argument = argument
        self.message = message

        super().__init__(f"{self.argument} is missing. {self.message}")


class Warehouse:
    """Class for managing wahrehouse."""

    def __init__(self, warehouse_id: int = None) -> None:
        """Initialize a Warehouse object.

        It takes an integer parameter 'warehouse_id'
        and sets up two attributes withn the object:
        'id' is an attribute storing the unique identifier for the warehouse,
        'stock'is an attribute initializes an empty list
        to store items within the warehouse's inventory.
        """
        self.id = warehouse_id
        self.stock = []

    def add_item(self, item) -> None:
        """Add new items in stock.

        The method takes an argument 'item',
        which has to be instance of the Item class.
        """
        if isinstance(item, Item):
            self.stock.append(item)

    def search(self, search_term: str) -> list:
        """Search for item in stock based on a provided search term.

        Args:
        - search_term(str): A string representing the state or
        category of an item.
        Returns:
        - list: A list containing string representaions
        of items thjat match the provided search term.
        """
        matching_item = []
        for item in self.stock:
            if (
                search_term.lower() == item.category.lower()
                or search_term.lower() == item.state.lower()
            ):
                matching_item.append(item.__str__())
        return matching_item

    @property
    def occupancy(self) -> int:
        """The ptoperty of the Warehouse class.

        Return the number of items currently present in the stock.
        """
        return len(self.stock)


class Item:
    """Class for managing items."""

    def __init__(
        self, state: str, category: str, warehouse: int, date_of_stock: str
    ) -> None:
        """Initialize an Item object.

        It takes the following arguments:
        - 'state': A strings indicating the state of item.
        - 'category': A strings representing the category of item.
        - 'warehouse': An integer serving as a unique indetefier
        for a warehouse.
        - 'date_of_stock': A string indicating the date
        when an item was added to the stock.

        Attrinutes:
        - 'state': Stores the state of item.
        - 'category': Stores the category of item.
        - 'warehouse': Holds unique indetefier of the associated warehouse.
        - 'date_of_stock': rECORDS the date when an item entered the stock.
        """
        self.state = state
        self.category = category
        self.warehouse = warehouse
        self.date_of_stock = date_of_stock

    def __str__(self):
        """Return a string representation of the item's state and category."""
        return f"{self.state} {self.category}"


class User:
    """Class for managing user's class."""

    def __init__(self, user_name: str) -> None:
        """Initialize an User object.

        It takes 'user name as string argument of a user's name
        and store it in private variable '_name'.
        If an empty string is provided,
        it'll be stored as the name "Anonymous".
        Attribute 'is_authenticated' stores a default value
        of authenticated by user as employee.
        """
        self._name = user_name if user_name else "Anonymous"
        self.is_authenticated = False

    def authenticate(self, password: str) -> False:
        """Take a password as argument but anyway it will return False.

        The method is used for owerriding of the Employee class.
        """
        return False

    def is_named(self, name: str) -> bool:
        """Check if the provided 'name" matches the user's stored name."""
        return name == self._name

    def greet(self) -> str:
        """Greet the user."""
        print(
            f"Hello, {self._name}!"
            f"\nWelcome to our Warehouse Database."
            f"\nIf you don't find what you are looking for,"
            f"\nplease ask one of our staff members to assist you."
        )
        return

    def bye(self) -> str:
        """Bid farewell to the user."""
        return f"Thank you for your visit, {self._name}!"


class Employee(User):
    """Class for managing employee's class."""

    def __init__(
        self, user_name=None, password=None, head_of: list = None
    ) -> None:  # no-qa
        """Initialize an Employee object and inherits from the User class.

        It takes the following arguments:
        - 'user_name': A strings indicating the user's name.
        - 'password': A strings representing the user's password.
        - 'head_of': An optional argument that may contain
        a list of Employee object.

        Attrinutes:
        - 'user_name': Stores the name by the user.
        - '__password': Holds the private attribute for the password.
        - 'head_of': Stores a list of Employee objects.

        The method requers both 'user_name' and 'password';
        if either is missing, it raises a VallueError.
        """
        super().__init__(user_name)
        if user_name is None:
            raise MissingArgument("user_name", "An employee can not be anonymous.")
        elif password is None:
            raise MissingArgument("password", "An employee requires authentication.")

        self.__password = password
        self.head_of = head_of

    def authenticate(self, password: str) -> bool:
        """Verify if the provided password matches the stored private password.

        If the input password matches the stored password,
        update the 'is_authenticated' to True and return True to indicate
        a successfull authentication. If a password doesn't match, return False
        to indicate an authentication failure.
        """
        if password == self.__password:
            self.is_authenticated = True
            return True
        return False

    def order(self, item: str, amount: int) -> None:
        """Place and order the privided item.

        Take two arguments:
        - 'item': A string indicating an item to be ordered.
        - 'amount': A integer representing the quantity of items
        to be ordered.
        """
        self.item = item
        self.amount = amount
        print(amount, item, " have been placed")

    def greet(self) -> None:
        """Greet the employee."""
        print(
            f"Hello, {self._name}!"
            f"\nIf you experience a problem with the system,"
            f"\nplease contact technical support."
        )

    def bye(self) -> None:
        """Bid farewell to the employee."""
        return f"Thank you for your visit, {self._name}!"
