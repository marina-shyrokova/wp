"""This module tests classes."""
import unittest
from cli.classes import Warehouse, Item, User, Employee


class TestClassNames(unittest.TestCase):
    """Test names of classes."""

    def test_warehouse_class_name(self):
        """Test the name of 'Warehouse' class."""
        self.assertEqual(Warehouse.__name__, "Warehouse")

    def test_item_class_name(self):
        """Test the name of 'Item' class."""
        self.assertEqual(Item.__name__, "Item")

    def test_user_class_name(self):
        """Test the name of 'User' class."""
        self.assertEqual(User.__name__, "User")

    def test_employee_class_name(self):
        """Test the name of 'Employee' class."""
        self.assertEqual(Employee.__name__, "Employee")


class TestClassInheritance(unittest.TestCase):
    """Test iheritance of classes."""

    def test_employee_inheritance(self):
        """Test the inheritance of the Employee class by the User class."""
        self.assertTrue(issubclass(Employee, User))


class TestUserClass(unittest.TestCase):
    """Test the 'User' class."""

    def test_user_annonymus(self):
        """Test the annonymous user."""
        user = User("")
        self.assertEqual(user._name, "Anonymous")
        self.assertFalse(user.is_authenticated)

    def test_user_name(self):
        """Test the user's name."""
        user_name = "Marina"
        user = User(user_name)
        self.assertEqual(user_name, user._name)
        self.assertFalse(user.is_authenticated)

    def test_user_authenticate(self):
        """Test the user's authentication."""
        user_name, password = "Marina", "12345"
        user = User(user_name)
        user.authenticate(password)
        self.assertFalse(user.is_authenticated)


class TestEmployee(unittest.TestCase):
    """Test the 'Employee' class."""

    def test_employee_with_missing_argument(self):
        """Test the 'Employee' class with the missing argument."""
        with self.assertRaises(ValueError):
            employee = Employee("", "")
            self.assertFalse(employee.is_authenticated)
            self.assertIsNone(employee.head_of)

    def test_employee_authenticated(self):
        """Test the employee's authentication."""
        employee = Employee("Marina", "123456")
        self.assertTrue(employee.authenticate("123456"))
        self.assertTrue(employee.is_authenticated)
        self.assertEqual(employee.head_of, None)

    def test_employee_head_of(self):
        """Test the 'Employee' class when it acts as the head of emoloyees."""
        employee1 = Employee("Marina", "123456")
        employee2 = Employee("Anna", "anna123")
        employee = Employee("Elis", "1111", head_of=[employee1, employee2])
        self.assertIn(employee1, employee.head_of)


class TestWarehouse(unittest.TestCase):
    """Test the 'Warehouse' class."""

    def test_warehouse_id(self):
        """Test the attribute 'warehouse_id'."""
        warehouse = Warehouse()
        self.assertIsNone(warehouse.id)
        warehouse_id = 5
        warehouse = Warehouse(warehouse_id)
        self.assertEqual(warehouse.id, warehouse_id)

    def test_warehouse_stock(self):
        """Test the method 'stock'."""
        warehouse = Warehouse()
        self.assertEqual(warehouse.stock, [])
        self.assertEqual(len(warehouse.stock), 0)
        item = Item("Almost new", "Tablet", 1, "2022-5-22")
        warehouse.add_item(item)
        self.assertEqual(len(warehouse.stock), 1)

    def test_warehouse_search(self):
        """Test the method 'search'."""
        warehouse = Warehouse()
        item1 = Item("Almost new", "Tablet", 1, "2022-5-22")
        item2 = Item("New", "Tablet", 1, "2022-5-22")
        warehouse.add_item(item1)
        warehouse.add_item(item2)
        self.assertEqual(
            warehouse.search("Tablet"), ["Almost new Tablet", "New Tablet"]
        )
        self.assertEqual(warehouse.search("ALMOST NEW"), ["Almost new Tablet"])


class TestItem(unittest.TestCase):
    """Test the 'WItem' class."""

    def test_item_properties(self):
        """Test properties of item."""
        state = "New"
        category = "Tablet"
        warehouse = 1
        date_of_stock = "2022-5-22"

        item = Item(state, category, warehouse, date_of_stock)

        self.assertEqual(item.state, "New")
        self.assertEqual(item.category, "Tablet")
        self.assertEqual(item.date_of_stock, "2022-5-22")

        self.assertTrue(isinstance(item.__str__(), str))
        self.assertEqual(item.__str__(), "New Tablet")


if __name__ == "__main__":
    unittest.main()
