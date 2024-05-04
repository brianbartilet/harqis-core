from typing import Callable, TypeVar, Generic, MutableSequence, Iterable, Union, Dict, Any

T = TypeVar("T", bound=Union[Dict, Iterable])


class QList(list, Generic[T], MutableSequence[T], Iterable[T]):
    """
    A class that mimics LINQ in C# providing a fluent way for list comprehension.
    This class extends the built-in list class and adds methods for querying and
    manipulating lists in a more expressive and readable way. It has been enhanced
    to handle dictionary-type data effectively.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __contains__(self, item):
        # This method is inherited from list, but redefining here for clarity
        return super().__contains__(item)

    def __iter__(self):
        # This method is inherited from list, but redefining here for clarity
        return super().__iter__()

    def __getitem__(self, item):
        # Utilize the built-in __getitem__ for normal index and slicing operations.
        try:
            return super(QList, self).__getitem__(item)
        except TypeError:
            return self

    def __len__(self):
        # Utilize the length method provided by the parent list class
        return super().__len__()

    def any(self, condition: Callable[[T], bool] = lambda x: True) -> bool:
        """
        Checks if any element of the list satisfies the condition.

        Args:
            condition: A function that evaluates to True or False for each element.

        Returns:
            True if any element satisfies the condition, False otherwise.
        """
        return any(condition(item) for item in self)

    def all(self, condition: Callable[[T], bool]) -> bool:
        """
        Checks if all elements of the list satisfy the condition.

        Args:
            condition: A function that evaluates to True or False for each element.

        Returns:
            True if all elements satisfy the condition, False otherwise.
        """
        return all(condition(item) for item in self)

    def where(self, condition: Callable[[T], bool]) -> "QList":
        """
        Filters the list based on a condition.

        Args:
            condition: A function that evaluates to True or False for each element.

        Returns:
            A new QList containing elements that satisfy the condition.
        """
        return QList(filter(condition, self))

    def first(self, condition: Callable[[T], bool] = lambda x: True) -> T:
        """
        Returns the first element that satisfies the condition.

        Args:
            condition: A function that evaluates to True or False for each element.

        Returns:
            The first element that satisfies the condition.

        Raises:
            StopIteration if no element satisfies the condition.
        """
        return next(filter(condition, self))

    def first_or_default(self, condition: Callable[[T], bool] = lambda x: True, default=None) -> T:
        """
        Returns the first element that satisfies the condition or a default value.

        Args:
            condition: A function that evaluates to True or False for each element.
            default: The default value to return if no element satisfies the condition.

        Returns:
            The first element that satisfies the condition or the default value.
        """
        return next(filter(condition, self), default)

    def last(self, condition: Callable[[T], bool] = lambda x: True) -> T:
        """
        Returns the last element that satisfies the condition.

        Args:
            condition: A function that evaluates to True or False for each element.

        Returns:
            The last element that satisfies the condition.

        Raises:
            StopIteration if no element satisfies the condition.
        """
        return next(filter(condition, reversed(self)))

    def last_or_default(self, condition: Callable[[T], bool] = lambda x: True, default=None) -> T:
        """
        Returns the last element that satisfies the condition or a default value.

        Args:
            condition: A function that evaluates to True or False for each element.
            default: The default value to return if no element satisfies the condition.

        Returns:
            The last element that satisfies the condition or the default value.
        """
        return next(filter(condition, reversed(self)), default)

    def single(self, condition: Callable[[T], bool] = lambda x: True) -> T:
        """
        Returns the single element that satisfies the condition.

        Args:
            condition: A function that evaluates to True or False for each element.

        Returns:
            The single element that satisfies the condition.

        Raises:
            ValueError if no element or more than one element satisfies the condition.
        """
        filtered = self.where(condition)
        if len(filtered) == 1:
            return filtered[0]
        elif len(filtered) > 1:
            raise ValueError("Multiple items found for condition.")
        else:
            raise ValueError("No item found for condition.")

    def single_or_default(self, condition: Callable[[T], bool] = lambda x: True, default=None) -> T:
        """
        Returns the single element that satisfies the condition or a default value.

        Args:
            condition: A function that evaluates to True or False for each element.
            default: The default value to return if no element satisfies the condition.

        Returns:
            The single element that satisfies the condition or the default value.

        Raises:
            ValueError if more than one element satisfies the condition.
        """
        filtered = self.where(condition)
        if len(filtered) > 1:
            raise ValueError("Multiple items found for condition.")
        return filtered[0] if filtered else default

    def select(self, selector: Callable[[T], T]) -> "QList":
        """
        Projects each element of the list into a new form.

        Args:
            selector: A function that transforms each element.

        Returns:
            A new QList containing the transformed elements.
        """
        return QList(map(selector, self))

    def select_many(self, selector: Callable[[T], Iterable[T]]) -> "QList":
        """
        Projects each element of the list into a new iterable and flattens the result.

        Args:
            selector: A function that transforms each element into an iterable.

        Returns:
            A new QList containing the flattened result of the transformations.
        """
        return QList(item for sublist in map(selector, self) for item in sublist)

    def distinct(self, key: Callable[[T], Any] = lambda x: x) -> "QList":
        """
        Returns a new QList containing distinct elements from the original list, uniquely identified by a key function.

        Args:
            key (Callable): A function that extracts a comparison key from each element. This key is used to determine
                            uniqueness among the elements. If not provided, the element itself is used as the key.

        Returns:
            A new QList with distinct elements based on the provided key.
        """
        seen = set()
        distinct_items = []
        for item in self:
            comparator = key(item)  # Extract the unique key from the item
            if comparator not in seen:
                seen.add(comparator)  # Mark this key as seen
                distinct_items.append(item)  # Add the original item to the result list
        return QList(distinct_items)

    def min(self, key: Callable[[T], T] = lambda x: x) -> T:
        """
        Returns the minimum element of the list based on a key function.

        Args:
            key: A function that returns a value used for comparison.

        Returns:
            The minimum element of the list.
        """
        return min(self, key=key)

    def max(self, key: Callable[[T], T] = lambda x: x) -> T:
        """
        Returns the maximum element of the list based on a key function.

        Args:
            key: A function that returns a value used for comparison.

        Returns:
            The maximum element of the list.
        """
        return max(self, key=key)
