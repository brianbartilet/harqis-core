"""
        Please don't kill me for adding these. I am tired of typing filter, iter, list, next, none, etc)
        Writing this class for my own use or anyone who thinks they might get the hang of using these methods
"""

"""
    Extracting, in case some folks want to use these methods directly instead
"""
from typing import Callable, TypeVar, Generic, MutableSequence, Iterable

T = TypeVar("T")


# TODO: Modify these values

def where(obj: list, condition: Callable[[callable], bool]):
    result = filter(condition, iter(obj))

    return qlist(result)


def first(obj: list, condition: Callable[[callable], bool] = lambda x: True) -> T:
    """
        Returns first item to meet condition
    :param obj:
    :param condition:
    :return:
    """
    return next(iter(where(obj, condition)))


def first_or_default(obj: list, condition: Callable[[callable], bool] = lambda x: True, default=None):
    """
         Returns default in case condition not met
    :param obj:
    :param condition:
    :param default:
    :return:
    """
    return next(iter(where(obj, condition)), default)


def last(obj: list, condition: Callable[[callable], bool] = lambda x: True):
    return next(iter(reversed(where(obj, condition))))


def last_or_default(obj: list, condition: Callable = lambda x: True, default=None):
    """
        Returns default in case condition not met
    :param obj:
    :param condition:
    :param default:
    :return:
    """
    return next(iter(reversed(where(obj, condition))), default)


"""
 TODO:  Create a queryable class that would contain all the methods of this qlist.
        This is needed to extend until dictionaries. 
"""


# noinspection PyPep8Naming
class qlist(list, Generic[T], MutableSequence[T], Iterable[T]):
    """
        Please don't kill me for adding these. I am tired of typing filter, iter, list, next, none, etc)
        Writing this class for my own use or anyone who thinks they might get the hang of using these methods
    """

    __counter__ = 0

    def any(self, condition: Callable[[callable], bool] = lambda x: True) -> bool:
        """
            Return if any of the items match the condition.
            If no condition - False as there's no item.
        :param condition:
        :return:
        """
        return len(self.where(condition)) > 0

    def all(self, condition: Callable[[callable], bool]) -> bool:
        """
            Return if all items match condition.
            If no items, true as there are no items to match condition
        :param condition:
        :return:
        """
        return len(self.where(condition)) == len(self)

    def where(self, condition: Callable[[callable], bool]) -> "qlist":
        result = filter(condition, iter(self))

        return qlist(result)

    def first(self, condition: Callable[[callable], bool] = lambda x: True) -> T:
        """
            Returns first item to meet condition
        :param condition:
        :return:
        """

        return next(iter(self.where(condition)))

    def first_or_default(self, condition: Callable[[callable], bool] = lambda x: True, default=None) -> T:
        """
             Returns default in case condition not met
        :param condition:
        :param default:
        :return:
        """
        return next(iter(self.where(condition)), default)

    def last(self, condition: Callable[[callable], bool] = lambda x: True) -> T:
        """
            Returns last item to meet condition
        :param condition:
        :return:
        """
        return next(iter(reversed(self.where(condition))))

    def last_or_default(self, condition: Callable[[callable], bool] = lambda x: True, default=None) -> T:
        """
            Returns default in case condition not met
        :param condition:
        :param default:
        :return:
        """
        return next(iter(reversed(self.where(condition))), default)

    def single(self, condition: Callable[[callable], bool] = lambda x: True) -> T:
        """
            Raises exception if multiple items match condition.
            Returns the first
        :param condition:
        :return: Single item matching condition
        """
        temp_list = self.where(condition)

        if len(temp_list) > 1:
            raise Exception("Multiple items found for condition.", temp_list)
        if len(temp_list) == 0:
            raise Exception("No item found for condition.", temp_list)
        # obviously there's only one item from here on
        return temp_list[0]

    def single_or_default(self, condition: Callable[[callable], bool] = lambda x: True, default=None) -> T:
        """
            Returns single item or default (in case of no matches)
        :param condition:
        :param default:
        :return:
        """
        temp_list = self.where(condition)

        if len(temp_list) > 1:
            raise Exception("Multiple items found for condition.", temp_list)

        return next(iter(temp_list), default)

    def select(self, selector: Callable[[callable], T]) ->"qlist":
        result = map(selector, iter(self))

        return qlist(result)

    def select_many(self, selector: Callable[[callable], T]) -> "qlist":
        result = map(selector, iter(self))

        return qlist([x for i in result for x in i ])

    def min(self, condition: Callable[[Callable], T] = lambda x: x) -> T:
        results = self.select(condition)

        return min(results)

    def max(self, condition: Callable[[Callable], T] = lambda x: x) -> T:
        results = self.select(condition)

        return max(results)

    def distinct(self, condition: Callable[[Callable], T] = lambda x: x) -> "qlist":

        return qlist(set(self))
    # region method overrides

    def __add__(self, rhs):
        return qlist(list.__add__(self, rhs))

    def __getitem__(self, item):
        result = list.__getitem__(self, item)
        try:
            return result
        except TypeError:
            return result

    def __copy__(self):
        result = []
        for i in range(len(self)):
            result.append(self[i])
        temp = qlist(result)
        temp.__counter__ = 0
        return temp

    def __iter__(self):
        new_copy = self.__copy__()

        # why not just return qlist again?
        return new_copy

        # generator type -> problem is type hinting gets destroyed
        """
        # check if we have any objects
        if len(self) == 0:
            return
    
        # yield our first object
        yield self[0]
        for i in range(1, len(self)):
            # yield for successive calls
            yield self[i]
    
        # no need for this line below, as we're not returning anything
        # in the case of StopIteration
        #return
        """

    def __next__(self):
        if self.__counter__ == len(self):
            raise StopIteration
        else:
            result = self[self.__counter__]
            self.__counter__ += 1
            return result


    # endregion


# for typing purposes

class QList(Generic[T], qlist):
    def __getitem__(self, item):
        result = list.__getitem__(self, item)
        try:
            return result
        except TypeError:
            return result


"""
# Some tests

list = qlist
a = list([1,2,3,4])

assert a.any(lambda x: x == 5) == False
assert a.any(lambda x: x == 1) == True
assert a.all(lambda x: x == 4) == False
assert a.all(lambda x: x == 1) == False
assert a.all(lambda x: x > 1) == False
assert a.all(lambda x: x < 5) == True
assert a.all(lambda x: x < -1) == False
assert a.any(lambda x: x == 'a') == False

b = qlist(["hello", "w0rld", "ball"])

assert b.first_or_default(lambda x: "l" in x) == 'hello'
assert b.first(lambda x: "0" in x) == 'w0rld'
try:
    assert b.first(lambda x: "x" in x)
    assert False
except:
    pass

assert b.last_or_default(lambda x: "l" in x) == 'ball'
assert b.last(lambda x: "0" in x) == 'w0rld'

try:
    assert b.last(lambda x: "x" in x)
    assert False
except:
    pass

assert b.where(lambda x: "ll" in x) == ['hello', 'ball']

# default clauses
assert b.any() == True
try:
    assert b.single()
    assert False
except:
    pass

try:
    b.single_or_default()
    assert False
except:
    pass

assert b.first() == 'hello'
assert b.first_or_default() == 'hello'
assert b.last() == 'ball'
assert b.last_or_default() == 'ball'

# empty list
c = qlist()

assert c.any() == False
assert c.all(lambda x: x==0) ==True
try:
    assert c.single()
    assert False
except:
    pass
assert c.single_or_default() == None
try:
    assert c.first()
    assert False
except:
    pass

assert c.first_or_default() == None
try:
    c.last()
    assert False
except:
    pass
assert c.last_or_default(default='Awesome') == 'Awesome'

# single list
d = qlist([1])
assert d.any() == True
assert d.all(lambda x: x==0) ==False
assert d.all(lambda x: x==1) ==True
assert d.single() == 1
assert d.single_or_default() == 1
assert d.first() == 1
assert d.first_or_default(lambda x: x==2) == None
assert d.last() == 1
assert d.last_or_default(lambda x: x==2, default='Awesome') == 'Awesome'

# type hinting
def some_method(some_values) -> QList[T]:
    return qlist(some_values)

xyz = some_method([1,2,2,4])

assert some_method([1,2,3,4]).where(lambda x: x > 1).first() == 2


for item, expected in zip(xyz, [1,2,2,4]):
    # iterator test
    assert item == expected

xyz.reverse()
assert xyz.count(2) == 2
assert xyz == [4,2,2,1]

xyz.append("sh")
assert xyz.pop(0) == 4
assert xyz.last() == "sh"

xyz.extend([55])
xyz.insert(3, 999)
assert [i for i in xyz] == [2, 2, 1, 999, 'sh', 55]


xyz.clear()
assert xyz.last_or_default() == None
print(xyz.all(lambda x: x is not None))
print(xyz.all(lambda x: x is None))
print(xyz.any(lambda x: x is None))
print(xyz)

"""

