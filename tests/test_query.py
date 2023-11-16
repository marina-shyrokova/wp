"""Test module query.py."""
# flake8: noqa
import sys
import os
import unittest
from unittest.mock import MagicMock

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from cli.query import (
    get_user,
    display_menu,
    get_selected_operation,
    list_items_by_warehouse,
    check_user_validation,
    order_item,
)
from cli.classes import User, Employee
from collections import Counter
from contextlib import contextmanager
import builtins


@contextmanager
def mock_input(mock):
    """Mock input."""
    original_input = builtins.input
    builtins.input = lambda _: mock
    yield
    builtins.input = original_input


@contextmanager
def mock_output(mock):
    """Mock output."""
    original_print = builtins.print
    builtins.print = lambda *value: [mock.append(val) for val in value]
    yield
    builtins.print = original_print


class TestGetUser(unittest.TestCase):
    """Test the 'get_user' function."""

    def test_get_user_not_in_employees(self):
        """Test scenarios when the user does#t hold an employee status."""
        with mock_input("Annonymous"):
            user = get_user()
        self.assertIsInstance(user, User)
        self.assertNotIsInstance(user, Employee)

        self.assertEqual(user._name, "Annonymous")

    def test_get_user_in_employees(self):
        """Test scenarios when the user holds an employee status."""
        with mock_input("Boris"):
            user = get_user()

        self.assertIsInstance(user, User)
        self.assertIsInstance(user, Employee)

        self.assertEqual(user._name, "Boris")


class TestManageWarehouse(unittest.TestCase):
    """Test functions for inventory system."""

    def test_det_select_operation(self):
        """Test the 'get_selected_operation' function."""
        menu = {
            "1": "List items by warehouse",
            "2": "Search an item and place an order",
            "3": "Browse by category",
            "4": "Quit",
        }

        output = [
            "Menu",
            "1: List items by warehouse",
            "2: Search an item and place an order",
            "3: Browse by category",
            "4: Quit",
        ]

        printed = []

        with mock_output(printed):
            display_menu(menu)

        self.assertEqual(output, printed)

        with mock_input("1"):
            selected_operation = get_selected_operation()
        self.assertEqual(selected_operation, "1")

    def test_list_item_by_warehouse(self):
        """Test the 'list_item_by_warehouse' function."""
        output = []

        with mock_output(output):
            result = list_items_by_warehouse()

        expected_lines = [
            "Total items in Warehouse 1:1346",
            "Total items in Warehouse 2:1258",
            "Total items in Warehouse 3:1173",
            "Total items in Warehouse 4:1223",
        ]

        self.assertEqual(output[-len(expected_lines) :], expected_lines)
        self.assertEqual(result, "Listed 5000 items.")

    def test_search_item(self):
        """Test the 'search_item' function."""
        mock_warehouse_1 = MagicMock()
        mock_warehouse_1.search = MagicMock(
            return_value=["Almost New Tablet", "New Tablet", "Funny Tablet"]
        )
        mock_warehouse_2 = MagicMock()
        mock_warehouse_2.search = MagicMock(return_value=["Blue Tablet", "Red Tablet"])

        count_warehouse_1_search = mock_warehouse_1.search.call_count
        count_warehouse_2_search = mock_warehouse_2.search.call_count

        mock_search_item = MagicMock()
        mock_result_of_search_item = mock_search_item.search_item.return_value(
            [
                "Almost New Tablet, Warehouse 1",
                "New Tablet, Warehouse 1",
                "Funny Tablet, Warehouse 1",
                "Blue Tablet, Warehouse 2",
                "Red Tablet, Warehouse 2",
            ]
        )
        count_of_items = Counter(item[-1] for item in mock_result_of_search_item)
        count_warehouse_1_search_item = count_of_items["1"]
        count_warehouse_2_search_item = count_of_items["2"]

        self.assertEqual(
            count_warehouse_1_search, count_warehouse_1_search_item
        )  # noqa: E501
        self.assertEqual(
            count_warehouse_2_search, count_warehouse_2_search_item
        )  # noqa: E501

    def test_print_warehouse_list(self):
        """Test printing warehouse list and the 'occupancy' method of the 'Warehouse' class."""
        mock_warehouse_1 = MagicMock()
        mock_warehouse_1.occupancy = MagicMock(return_value=3)
        mock_warehouse_2 = MagicMock()
        mock_warehouse_2.occupancy = MagicMock(return_value=2)

        amount_of_items_in_warehouse1 = mock_warehouse_1.occupancy()
        amount_of_items_in_warehouse2 = mock_warehouse_2.occupancy()

        mock_print_warehouse_list = MagicMock()
        mock_print_warehouse_list.print_warehouse_list.return_value = {
            "Warehouse 1": ["item1", "item2", "item3"],
            "Warehouse 2": ["item1", "item2"],
        }
        result = mock_print_warehouse_list.print_warehouse_list()

        self.assertEqual(amount_of_items_in_warehouse1, len(result["Warehouse 1"]))
        self.assertEqual(amount_of_items_in_warehouse2, len(result["Warehouse 2"]))


class TestNonEmployee(unittest.TestCase):
    """Test 'User' class."""

    def test_non_employee_access_order_item(self):
        """Test decorator for user validation."""
        user = User("John")
        user.is_authenticated = False

        decorated_order_item = check_user_validation(order_item)

        with mock_input("n"):
            result = decorated_order_item(user, "SomeItem", 10)

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
