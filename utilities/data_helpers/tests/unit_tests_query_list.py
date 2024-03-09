import unittest
from utilities.data_helpers.query_list import QList

class UnitTestsQList(unittest.TestCase):
    """
    Unit tests for the QList class.
    """

    def setUp(self):
        """Set up a QList instance for testing."""
        self.list = QList([1, 2, 3, 4, 5])

    def test_any(self):
        """Test the any method."""
        self.assertTrue(self.list.any(lambda x: x > 3))
        self.assertFalse(self.list.any(lambda x: x > 5))

    def test_all(self):
        """Test the all method."""
        self.assertTrue(self.list.all(lambda x: x < 6))
        self.assertFalse(self.list.all(lambda x: x < 5))

    def test_where(self):
        """Test the where method."""
        self.assertEqual(self.list.where(lambda x: x % 2 == 0), QList([2, 4]))

    def test_first(self):
        """Test the first method."""
        self.assertEqual(self.list.first(lambda x: x > 3), 4)
        with self.assertRaises(StopIteration):
            self.list.first(lambda x: x > 5)

    def test_first_or_default(self):
        """Test the first_or_default method."""
        self.assertEqual(self.list.first_or_default(lambda x: x > 3), 4)
        self.assertEqual(self.list.first_or_default(lambda x: x > 5, default=0), 0)

    def test_last(self):
        """Test the last method."""
        self.assertEqual(self.list.last(lambda x: x < 4), 3)
        with self.assertRaises(StopIteration):
            self.list.last(lambda x: x < 1)

    def test_last_or_default(self):
        """Test the last_or_default method."""
        self.assertEqual(self.list.last_or_default(lambda x: x < 4), 3)
        self.assertEqual(self.list.last_or_default(lambda x: x < 1, default=0), 0)

    def test_single(self):
        """Test the single method."""
        self.assertEqual(self.list.single(lambda x: x == 3), 3)
        with self.assertRaises(ValueError):
            self.list.single(lambda x: x < 3)

    def test_single_or_default(self):
        """Test the single_or_default method."""
        self.assertEqual(self.list.single_or_default(lambda x: x == 3), 3)
        self.assertEqual(self.list.single_or_default(lambda x: x > 5, default=0), 0)
        with self.assertRaises(ValueError):
            self.list.single_or_default(lambda x: x < 3)

    def test_select(self):
        """Test the select method."""
        self.assertEqual(self.list.select(lambda x: x * 2), QList([2, 4, 6, 8, 10]))

    def test_select_many(self):
        """Test the select_many method."""
        nested_list = QList([[1, 2], [3, 4], [5]])
        self.assertEqual(nested_list.select_many(lambda x: x), QList([1, 2, 3, 4, 5]))

    def test_distinct(self):
        """Test the distinct method."""
        duplicate_list = QList([1, 2, 2, 3, 4, 4, 5])
        self.assertEqual(duplicate_list.distinct(), QList([1, 2, 3, 4, 5]))

    def test_min(self):
        """Test the min method."""
        self.assertEqual(self.list.min(), 1)
        self.assertEqual(self.list.min(lambda x: -x), 5)

    def test_max(self):
        """Test the max method."""
        self.assertEqual(self.list.max(), 5)
        self.assertEqual(self.list.max(lambda x: -x), 1)
