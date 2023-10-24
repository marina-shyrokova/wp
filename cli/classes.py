import datetime

class Warehouse:
    def __init__(self, warehouse_id: int) -> None:
        self.warehouse_id = warehouse_id
        self.stock = []

    def add_item (self, item) -> None:
        if isinstance(item, Item):
            self.stock.append(item)

    def search(self, search_term: str) -> list:
        matching_item =[]
        for item in self.stock:
            if search_term.lower() == item.category.lower():
                matching_item.append(item.__str__())
        return matching_item

    @property
    def occupancy(self) -> int:
        return len(self.stock)

class Item:
    def __init__(self, state: str, category: str, warehouse: int,  date_of_stock: datetime) -> None:
        self.state = state
        self.category = category
        self.warehouse = warehouse
        self.date_of_stock = date_of_stock

    def __str__(self):
        return f"{self.state} {self.category}"

class User:
    def __init__(self, user_name: str) -> None:
        self._name = user_name
        if not user_name:
            self.name = 'Anonymus'

        self.is_authenticated = False

    def authenticate (self, password: str) -> False:
        self.password = password
        return False
    
    def is_named(self, name : str) -> bool:
        if name == self._name:
            return True
        return False
    
    def greet (self) -> str:
        print (f"Hello, {self._name}!"
        f"\nWelcome to our Warehouse Database."
        f"\nIf you don't find what you are looking for,"
        f"\nplease ask one of our staff members to assist you.")
        return
        
    def bye (self) -> str:
        return f"Thank you for your visit, {self._name}!"

class Employee(User):
    def __init__(self, user_name: str, password: str, head_of: list = None) -> None:
        if not user_name or not password:
            raise ValueError("Both 'user_name' and 'password' are required.")
        self._name = user_name
        self.__password = password
        self.head_of = head_of

    def authenticate(self, password: str) -> bool:
        if password == self.__password:
            self.is_authenticated = True
            return True
        return False
    
    def order(self, item: str, amount: int) -> None:
        self.item = item
        self.amount = amount
        print (amount, item, " have been placed")

    def greet(self) -> None:
        print(f"Hello, {self._name}!"
            f"\nIf you experience a problem with the system,"
            f"\nplease contact technical support.")
        
    def bye(self) -> None:
        return f"Thank you for your visit, {self._name}!"



        
    















