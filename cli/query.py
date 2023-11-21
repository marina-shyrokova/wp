"""Manage a comand-line interface inventory system for a warehouse.

Functionality includes:
- Listing items by warehouse
- Searching for items and placing orders
- Browsing items by category
- User authentication and interaction.
"""
import sys
import os
from datetime import datetime as dt
from collections import Counter
import json

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(parent_dir)

from cli.loader import Loader  # noqa: E402
from cli.classes import User, Employee  # noqa: E402
from cli.data import personnel  # noqa: E402


stock = Loader(model="stock")


def display_menu(menu):
    """Display a menu of avaliable operations."""
    print("Menu")
    for k, v in menu.items():
        print(f"{k}: {v}")


def get_selected_operation():
    """Ask user for select operation and return it."""
    selected_operation = input("Make your choice: ")
    return selected_operation


def list_items_by_warehouse():
    """Print lists of items for each warehouse.

    Print amount of items in each warehouse.
    """
    count_of_items = {}

    for warehouse in stock:
        item_count = len(warehouse.stock)
        count_of_items[f"warehouse {warehouse.id}"] = item_count
        print(f"Warehouse ID: {warehouse.id}\n")
        for item in warehouse.stock:
            print(item.state, item.category)

    for warehouse in stock:
        print(f"Total items in Warehouse {warehouse.id}:{warehouse.occupancy}")

    return f"Listed {sum(count_of_items.values())} items"


def search_and_order_item():
    """Serches and places order of item.

    This function prompts the user to input
    the name of the disired item. Then it display the avalibale
    quantity of the item in stock across different location,
    along with the duration for wich it has been stored
    at each location in terms of days.
    Then, the function promts the user if they want to order the dispayed item.
    If the user confirm the order by entering 'Y'
    it procceds to the function 'order_item'
    """
    try:
        item_input = input("What is the name of the item? ")

        if item_input.isdigit():
            print("The name of the item doesn't include numbers")
        selected_item = item_input.capitalize()
        today = dt.now().date()

        info_of_item = []
        count = {}

        for warehouse in stock:
            temp = 0
            for item in warehouse.stock:
                if item.__str__().lower() == item_input.lower():
                    temp += 1
                    count[f"Warehouse {warehouse.id}"] = temp
                    date_of_stock = dt.strptime(
                        item.date_of_stock.split()[0], "%Y-%m-%d"
                    ).date()
                    days_in_stock = (today - date_of_stock).days
                    info_of_item.append(
                        {
                            f"- Warehouse {warehouse.id}": f"(in stock for {days_in_stock} days)"  # noqa: E501
                        }
                    )
        total = len(info_of_item)

        print(f"Amount available: {total}")

        print("Location:")

        if total > 0:
            for item in info_of_item:
                for k, v in item.items():
                    print(k, v)

            maximum_in_warehouse = [
                (k, v)
                for k, v in count.items()
                if v == max(v for v in count.values())  # no-qa
            ]

            max_wrh, max_item = maximum_in_warehouse[0]

            print(f"\nMaximum availability: {max_item} in {max_wrh}")

            order = input("Would you like to order this item?(y/n): ").lower()
            if order == "n":
                return f"Search a {selected_item}"
            elif order == "y":
                return order_item(user, selected_item, total)
            else:
                print("Your answer has to be y or n")
                working_continiue()

        else:
            print("Not in stock")
            return f"Search a {selected_item}"

    except ValueError:
        print("Input is not valid. Try again.")
        search_and_order_item()


def check_user_validation(func):
    """Decorate the 'order_item' function, validating user authentication.

    Verifies the user's authentication status. If user is not validated,
    it prompts for a change in the username or password and rechecks.
    If user is validated, it procceeds to call the 'order_item' function.
    """
    global user

    def wrapper(user, *args, **kwargs):
        user_validation = user.is_authenticated

        if user_validation:
            return func(user, *args, **kwargs)
        while not user_validation:
            if isinstance(user, Employee):
                password = input("Please input your password:")
                user_validation = user.authenticate(password)
                if user.is_authenticated:
                    return func(user, *args, **kwargs)
                else:
                    answer = input(
                        "User_name or password is not valid."
                        "Do you want to try again? y/n "
                    ).lower()
                    if answer == "y":
                        user = get_user()
                        globals()["user"] = user
                    elif answer == "n":
                        working_continiue()
                        break
                    else:
                        print("Yoir answer has to be y or n")
                        working_continiue()
            elif isinstance(user, User):
                answer = input(
                    "Sorry, but you are not employee."
                    "Would you like to change the name? y/n "
                ).lower()
                if answer == "y":
                    user = get_user()
                    globals()["user"] = user
                elif answer == "n":
                    break
                else:
                    print("Yoir answer has to be y or n")
            else:
                answer = input(
                    "User_name or password is not valid."
                    "Do you want to try again? y/n "
                ).lower()
                if answer == "y":
                    user = get_user()
                    globals()["user"] = user
                elif answer == "n":
                    break
                else:
                    print("Yoir answer has to be y or n")
                    working_continiue()

    return wrapper


@check_user_validation
def order_item(user, selected_item, total):
    """Places an order for items.

    Prompts the user to input the quantity of items they want to order.
    Virifies if the quantity isn't greater
    than avaliable amount of items in the stock.
    If the quantity is acceptable,
    calls the 'order' method from the 'User' class.
    """
    while True:
        try:
            amount = int(input("How many would you like? "))
            if amount == 0:
                print(f"The amount has to be grater than 0")
                working_continiue()
            if amount >= total:
                print(f"There are not avalibale {amount}, only {total}")
                working_continiue()
            elif amount < total:
                stock_dict = stock.to_dict()
                index_to_remove = []
                i = 0
                for item in stock_dict:
                    i += 1
                    if (
                        selected_item.lower()
                        == (f"{item['state']} {item['category']}").lower()
                    ):
                        index_to_remove.append(i - 1)
                        if len(index_to_remove) == amount:
                            break

                for i in index_to_remove:
                    del stock_dict[i]

                json_file_path = os.path.join(current_dir, "data", "stock.json")

                with open(json_file_path, "w") as file:
                    json.dump(stock_dict, file, indent=1)

                user.order(selected_item, amount)
                break
        except ValueError:
            print("Input valid")
    return f"Search and ordered the {selected_item}"


def browse_by_category():
    """Browse items by category.

    This function displays all available categories along with
    the quantity of items in each category.
    It prompts the user to input the number corresponding to
    the desired category for browsing,
    after that it pocceeds the 'search_item'function.
    """
    categories = []

    for warehouse in stock:
        for item in warehouse.stock:
            categories.append(item.category)

    count = Counter(categories)

    summary_of_categories = []

    i = 1
    for k, v in count.items():
        summary_of_categories.append((i, k, v))
        i += 1

    for i in summary_of_categories:
        print(f"{i[0]}. {i[1]} ({i[2]})")

    try:
        number_of_category = int(
            input("Type the number of the category to browse: ")
        )  # no-qa

        if number_of_category > len(summary_of_categories):
            print(f"There are only {len(summary_of_categories)} categories")

        else:
            selected_category = None

            for category_info in summary_of_categories:
                if number_of_category == category_info[0]:
                    selected_category = category_info[1]
                    break

            return search_item(selected_category)

    except ValueError:
        print("Invalid input. Try again.")
    except TypeError:
        print("It has to be a number of category")


def search_item(selected_category):
    """Search for items based on the selected category.

    This function displays a list of items that belong to the choosen category
    obtained from  the 'browse_by_category' function.
    """
    print(f"\nList of {selected_category} available:")

    for warehouse in stock:
        for item in warehouse.search(selected_category):
            print(f"{item}, Warehouse {warehouse.id}")

    return f"Browsed the category {selected_category}"


def session_operation():
    """Manage user operations.

    Displays a menu of avaliable operations and prompts the user for input.
    Based on the selected operation, it triggers specific funcrions.
    """
    menu = {
        "1": "List items by warehouse",
        "2": "Search an item and place an order",
        "3": "Browse by category",
        "4": "Quit",
    }
    display_menu(menu)

    operation = get_selected_operation()

    if operation == "4":
        user.bye()
        return
    elif operation == "1":
        action = list_items_by_warehouse()
        session_actions.append(
            {
                user.__class__.__name__: f"{user._name}. {action}. {dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')}."
            }
        )
        working_continiue()
    elif operation == "2":
        action = search_and_order_item()
        session_actions.append(
            {
                user.__class__.__name__: f"{user._name}. {action}. {dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')}."
            }
        )
        working_continiue()
    elif operation == "3":
        action = browse_by_category()
        session_actions.append(
            {
                user.__class__.__name__: f"{user._name}. {action}. {dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')}."
            }
        )
        working_continiue()
    else:
        print("*" * 50)
        print(operation, "is not a valid operation.")
        print("*" * 50)
        working_continiue()


def working_continiue():
    """Prompts the user to continue to work with programm.

    Ask the user weher they would like to continue working with the program.
    If they confirm by entering 'Y', the programm procceds
    to the 'session_operation.
    If 'N', the program stops execution.'
    """
    try:
        working_continue = input(
            "Would you like to continue to work with program?(y/n) "
        ).lower()
        if working_continue == "y":
            session_operation()
        elif working_continue == "n":
            return
        else:
            print("Invalid input. Try again")
    except ValueError:
        print("Invalid input. Try again")
    except TypeError:
        print("Invalid input. Try again")


def get_user():
    """Get the user's name and verifies if the name corresponds to an employee.

    Prompts the user for input their name and checks if the name is presentin
    the personnel database.
    If the name is found, it is stored as an instance of the 'Employee' class.
    If name is not found,it is stored it as an instance of the 'User' class.
    """
    user = None
    user_name = input("Please provide your name: ")
    for i in personnel:
        if user_name == i["user_name"]:
            user = Employee(i["user_name"], i["password"])
            return user
        for j in i.get("head_of", []):
            if user_name == j["user_name"]:
                user = Employee(j["user_name"], j["password"])
                return user
    user = User(user_name)
    return user


if __name__ == "__main__":
    session_actions = []
    user = get_user()
    print(user.greet())
    session_operation()
    print(user.bye())
    if session_actions:
        users_logs = []
        emploeeys_logs = []
        for data in session_actions:
            if "User" in data:
                users_logs.append(f"{data['User']}\n")

            elif "Employee" in data:
                emploeeys_logs.append(f"{data['Employee']}\n")

        path_file_users_log = os.path.join(current_dir, "log", "users.log")
        with open(path_file_users_log, "a") as file:
            file.writelines(users_logs)

        path_file_employees_log = os.path.join(current_dir, "log", "employees.log")
        with open(path_file_employees_log, "a") as file:
            file.writelines(emploeeys_logs)
