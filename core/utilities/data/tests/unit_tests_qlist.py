import unittest
from core.utilities.data.qlist import QList


class UnitTestsList(unittest.TestCase):
    def setUp(self):
        """Set up a QList instance for testing."""
        self.list = QList([1, 2, 3, 4, 5])

    def test_any(self):
        """Test the .any method."""
        self.assertTrue(self.list.any(lambda x: x > 3))
        self.assertFalse(self.list.any(lambda x: x > 5))

    def test_all(self):
        """Test the .all method."""
        self.assertTrue(self.list.all(lambda x: x < 6))
        self.assertFalse(self.list.all(lambda x: x < 5))

    def test_where(self):
        """Test the .where method."""
        self.assertEqual(self.list.where(lambda x: x % 2 == 0), QList([2, 4]))

    def test_first(self):
        """Test the .first method."""
        self.assertEqual(self.list.first(lambda x: x > 3), 4)
        with self.assertRaises(StopIteration):
            self.list.first(lambda x: x > 5)

    def test_first_or_default(self):
        """Test the .first_or_default method."""
        self.assertEqual(self.list.first_or_default(lambda x: x > 3), 4)
        self.assertEqual(self.list.first_or_default(lambda x: x > 5, default=0), 0)

    def test_last(self):
        """Test the .last method."""
        self.assertEqual(self.list.last(lambda x: x < 4), 3)
        with self.assertRaises(StopIteration):
            self.list.last(lambda x: x < 1)

    def test_last_or_default(self):
        """Test the .last_or_default method."""
        self.assertEqual(self.list.last_or_default(lambda x: x < 4), 3)
        self.assertEqual(self.list.last_or_default(lambda x: x < 1, default=0), 0)

    def test_single(self):
        """Test the .single method."""
        self.assertEqual(self.list.single(lambda x: x == 3), 3)
        with self.assertRaises(ValueError):
            self.list.single(lambda x: x < 3)

    def test_single_or_default(self):
        """Test the .single_or_default method."""
        self.assertEqual(self.list.single_or_default(lambda x: x == 3), 3)
        self.assertEqual(self.list.single_or_default(lambda x: x > 5, default=0), 0)
        with self.assertRaises(ValueError):
            self.list.single_or_default(lambda x: x < 3)

    def test_select(self):
        """Test the .select method."""
        self.assertEqual(self.list.select(lambda x: x * 2), QList([2, 4, 6, 8, 10]))

    def test_select_many(self):
        """Test the .select_many method."""
        nested_list = QList([[1, 2], [3, 4], [5]])
        self.assertEqual(nested_list.select_many(lambda x: x), QList([1, 2, 3, 4, 5]))

    def test_distinct(self):
        """Test the .distinct method."""
        duplicate_list = QList([1, 2, 2, 3, 4, 4, 5])
        self.assertEqual(duplicate_list.distinct(), QList([1, 2, 3, 4, 5]))

    def test_min(self):
        """Test the .min method."""
        self.assertEqual(self.list.min(), 1)
        self.assertEqual(self.list.min(lambda x: -x), 5)

    def test_max(self):
        """Test the .max method."""
        self.assertEqual(self.list.max(), 5)
        self.assertEqual(self.list.max(lambda x: -x), 1)


class TestQListDictionaries(unittest.TestCase):
    def setUp(self):
        """Set up a QList instance with dictionary entries for testing."""
        self.data = QList([
            {'id': 1, 'name': 'Alice', 'age': 28},
            {'id': 2, 'name': 'Bob', 'age': 23},
            {'id': 3, 'name': 'Charlie', 'age': 30},
            {'id': 4, 'name': 'David', 'age': 28},
            {'id': 2, 'name': 'Eve', 'age': 35}  # Duplicate ID with different info
        ])

    def test_any(self):
        """Test if any dictionary matches a certain condition."""
        self.assertTrue(self.data.any(lambda x: x['age'] > 30))
        self.assertFalse(self.data.any(lambda x: x['name'] == 'Zoe'))

    def test_all(self):
        """Test if all dictionaries match a certain condition."""
        self.assertTrue(self.data.all(lambda x: 'id' in x))
        self.assertFalse(self.data.all(lambda x: x['age'] < 35))

    def test_where(self):
        """Test filtering dictionaries based on a condition."""
        filtered = self.data.where(lambda x: x['age'] == 28)
        self.assertEqual(len(filtered), 2)
        self.assertTrue(all(item['age'] == 28 for item in filtered))

    def test_first(self):
        """Test getting the first dictionary matching a condition."""
        self.assertEqual(self.data.first(lambda x: x['name'] == 'Alice')['id'], 1)
        with self.assertRaises(StopIteration):
            self.data.first(lambda x: x['name'] == 'Zoe')

    def test_first_or_default(self):
        """Test getting the first dictionary or a default if no match found."""
        self.assertIsNone(self.data.first_or_default(lambda x: x['name'] == 'Zoe', default=None))

    def test_last(self):
        """Test getting the last dictionary matching a condition."""
        self.assertEqual(self.data.last(lambda x: x['age'] == 28)['name'], 'David')

    def test_last_or_default(self):
        """Test getting the last dictionary or a default if no match found."""
        default_dict = {'id': 0, 'name': 'None', 'age': 0}
        self.assertEqual(self.data.last_or_default(lambda x: x['age'] == 25, default=default_dict), default_dict)

    def test_single(self):
        """Test getting a single dictionary that uniquely satisfies a condition."""
        self.assertEqual(self.data.single(lambda x: x['id'] == 3)['name'], 'Charlie')
        with self.assertRaises(ValueError):
            self.data.single(lambda x: x['age'] == 28)

    def test_single_or_default(self):
        """Test getting a single dictionary or a default if condition is not uniquely satisfied."""
        self.assertEqual(self.data.single_or_default(lambda x: x['id'] == 3)['name'], 'Charlie')
        self.assertIsNone(self.data.single_or_default(lambda x: x['id'] == 5, default=None))
        with self.assertRaises(ValueError):
            self.data.single_or_default(lambda x: x['age'] == 28)

    def test_select(self):
        """Test transforming each dictionary based on a selector function."""
        names = self.data.select(lambda x: x['name'].upper())
        self.assertIn('ALICE', names)

    def test_select_many(self):
        """Test projecting each element into an iterable and flattening the result."""
        details = self.data.select_many(lambda x: [x['name'], str(x['age'])])
        self.assertIn('Alice', details)
        self.assertIn('28', details)  # Age from multiple entries as strings

    def test_distinct(self):
        """Test getting distinct dictionaries based on IDs to avoid duplicate entries."""
        distinct = self.data.distinct(lambda x: x['id'])
        self.assertEqual(len(distinct), 4)  # Expected 4 unique IDs

    def test_min_and_max(self):
        """Test finding minimum and maximum based on a key function."""
        youngest = self.data.min(key=lambda x: x['age'])
        oldest = self.data.max(key=lambda x: x['age'])
        self.assertEqual(youngest['age'], 23)
