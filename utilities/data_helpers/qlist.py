from typing import Callable, TypeVar, Generic, MutableSequence, Iterable

T = TypeVar("T")

class QList(list, Generic[T], MutableSequence[T], Iterable[T]):
    def __getitem__(self, item):
        result = list.__getitem__(self, item)
        try:
            return result
        except TypeError:
            return result
    """
    A class that mimics LINQ in C# providing a fluent way for list comprehension.

    This class extends the built-in list class and adds methods for querying and
    manipulating lists in a more expressive and readable way.
    """

    def any(self, condition: Callable[[T], bool] = lambda x: True) -> bool:
        """
        Checks if any element of the list satisfies the condition.

        :param condition: A function that evaluates to True or False for each element.
        :return: True if any element satisfies the condition, False otherwise.
        """
        return any(condition(item) for item in self)

    def all(self, condition: Callable[[T], bool]) -> bool:
        """
        Checks if all elements of the list satisfy the condition.

        :param condition: A function that evaluates to True or False for each element.
        :return: True if all elements satisfy the condition, False otherwise.
        """
        return all(condition(item) for item in self)

    def where(self, condition: Callable[[T], bool]) -> "QList":
        """
        Filters the list based on a condition.

        :param condition: A function that evaluates to True or False for each element.
        :return: A new qlist containing elements that satisfy the condition.
        """
        return QList(filter(condition, self))

    def first(self, condition: Callable[[T], bool] = lambda x: True) -> T:
        """
        Returns the first element that satisfies the condition.

        :param condition: A function that evaluates to True or False for each element.
        :return: The first element that satisfies the condition.
        :raises: StopIteration if no element satisfies the condition.
        """
        return next(filter(condition, self))

    def first_or_default(self, condition: Callable[[T], bool] = lambda x: True, default=None) -> T:
        """
        Returns the first element that satisfies the condition or a default value.

        :param condition: A function that evaluates to True or False for each element.
        :param default: The default value to return if no element satisfies the condition.
        :return: The first element that satisfies the condition or the default value.
        """
        return next(filter(condition, self), default)

    def last(self, condition: Callable[[T], bool] = lambda x: True) -> T:
        """
        Returns the last element that satisfies the condition.

        :param condition: A function that evaluates to True or False for each element.
        :return: The last element that satisfies the condition.
        :raises: StopIteration if no element satisfies the condition.
        """
        return next(filter(condition, reversed(self)))

    def last_or_default(self, condition: Callable[[T], bool] = lambda x: True, default=None) -> T:
        """
        Returns the last element that satisfies the condition or a default value.

        :param condition: A function that evaluates to True or False for each element.
        :param default: The default value to return if no element satisfies the condition.
        :return: The last element that satisfies the condition or the default value.
        """
        return next(filter(condition, reversed(self)), default)

    def single(self, condition: Callable[[T], bool] = lambda x: True) -> T:
        """
        Returns the single element that satisfies the condition.

        :param condition: A function that evaluates to True or False for each element.
        :return: The single element that satisfies the condition.
        :raises: ValueError if no element or more than one element satisfies the condition.
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

        :param condition: A function that evaluates to True or False for each element.
        :param default: The default value to return if no element satisfies the condition.
        :return: The single element that satisfies the condition or the default value.
        :raises: ValueError if more than one element satisfies the condition.
        """
        filtered = self.where(condition)
        if len(filtered) > 1:
            raise ValueError("Multiple items found for condition.")
        return filtered[0] if filtered else default

    def select(self, selector: Callable[[T], T]) -> "QList":
        """
        Projects each element of the list into a new form.

        :param selector: A function that transforms each element.
        :return: A new qlist containing the transformed elements.
        """
        return QList(map(selector, self))

    def select_many(self, selector: Callable[[T], Iterable[T]]) -> "QList":
        """
        Projects each element of the list into a new iterable and flattens the result.

        :param selector: A function that transforms each element into an iterable.
        :return: A new qlist containing the flattened result of the transformations.
        """
        return QList(item for sublist in map(selector, self) for item in sublist)

    def distinct(self) -> "QList":
        """
        Returns a new qlist containing distinct elements from the original list.

        :return: A new qlist with distinct elements.
        """
        return QList(set(self))

    def min(self, key: Callable[[T], T] = lambda x: x) -> T:
        """
        Returns the minimum element of the list based on a key function.

        :param key: A function that returns a value used for comparison.
        :return: The minimum element of the list.
        """
        return min(self, key=key)

    def max(self, key: Callable[[T], T] = lambda x: x) -> T:
        """
        Returns the maximum element of the list based on a key function.

        :param key: A function that returns a value used for comparison.
        :return: The maximum element of the list.
        """
        return max(self, key=key)
