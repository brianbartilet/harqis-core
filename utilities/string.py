from random import randint
import random
import string


class StringHelper(object):

    def random_string_generator(self, size=2, chars=string.ascii_uppercase):
        return ''.join(random.choice(chars) for x in range(size))

    def generate_passport_no(self):
        return "{}{}".format(self.random_string_generator(size=2), self.random_with_n_digits(6))

    @staticmethod
    def random_with_n_digits(n):
        range_start = 10 ** (n - 1)
        range_end = (10 ** n) - 1
        return randint(range_start, range_end)

    @staticmethod
    def concatenate_string(string_to_concatenate, concatenate_with, separator=" ", ):
        array = str(string_to_concatenate).split(separator)
        ret = array[0]
        for i in range(1, len(array)):
            ret = ret + concatenate_with + array[i]

        return ret

