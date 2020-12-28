import unittest
from assignment1 import *


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.verificationErrors = []

    def tearDown(self):

        for item in self.verificationErrors:
            print(item)
        print("Number of Errors = " + str(len(self.verificationErrors)))

    def test_change_of_base(self):
        BASES = [10, 2, 7, 4, 13]
        NUMBERS = [2, 10, 17, 41, 374]

        base = BASES[0]
        try:
            self.assertEqual(change_of_base(NUMBERS[0], base), [2])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(change_of_base(NUMBERS[1], base), [1,0])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(change_of_base(NUMBERS[2], base), [1,7])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(change_of_base(NUMBERS[3], base), [4,1])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(change_of_base(NUMBERS[4], base), [3,7,4])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        base = BASES[1]
        try:
            self.assertEqual(change_of_base(NUMBERS[0], base), [1,0])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(change_of_base(NUMBERS[1], base), [1,0,1,0])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(change_of_base(NUMBERS[2], base), [1,0,0,0,1])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(change_of_base(NUMBERS[3], base), [1,0,1,0,0,1])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(change_of_base(NUMBERS[4], base), [1,0,1,1,1,0,1,1,0])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        # NUMBERS = [2, 10, 17, 41, 374]
        base = BASES[2]
        try:
            self.assertEqual(change_of_base(NUMBERS[0], base), [2])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(change_of_base(NUMBERS[1], base), [1,3])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(change_of_base(NUMBERS[2], base), [2,3])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(change_of_base(NUMBERS[3], base), [5,6])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(change_of_base(NUMBERS[4], base), [1,0,4,3])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        # NUMBERS = [2, 10, 17, 41, 374]
        base = BASES[3]
        try:
            self.assertEqual(change_of_base(NUMBERS[0], base), [2])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(change_of_base(NUMBERS[1], base), [2,2])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(change_of_base(NUMBERS[2], base), [1,0,1])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(change_of_base(NUMBERS[3], base), [2,2,1])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(change_of_base(NUMBERS[4], base), [1,1,3,1,2])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        # NUMBERS = [2, 10, 17, 41, 374]
        base = BASES[4]
        try:
            self.assertEqual(change_of_base(NUMBERS[0], base), [2])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(change_of_base(NUMBERS[1], base), [10])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(change_of_base(NUMBERS[2], base), [1,4])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(change_of_base(NUMBERS[3], base), [3,2])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(change_of_base(NUMBERS[4], base), [2, 2, 10])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

    def test_numerical_radix_sort(self):
        try:
            self.assertEqual(numerical_radix_sort([583, 1000, 100, 10, 3, 1], 10), [1, 3, 10, 100, 583, 1000])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(numerical_radix_sort([583, 1000, 100, 10, 3, 1], 2), [1, 3, 10, 100, 583, 1000])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(numerical_radix_sort([583, 1000, 100, 10, 3, 1], 7), [1, 3, 10, 100, 583, 1000])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(numerical_radix_sort([583, 1000, 100, 10, 3, 1], 15), [1, 3, 10, 100, 583, 1000])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(numerical_radix_sort([583, 1000, 100, 10, 3, 1], 103), [1, 3, 10, 100, 583, 1000])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(numerical_radix_sort([1, 80, 1838, 4838, 9999], 2), [1, 80, 1838, 4838, 9999])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(numerical_radix_sort([1, 80, 1838, 4838, 9999], 10), [1, 80, 1838, 4838, 9999])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(numerical_radix_sort([1, 80, 1838, 4838, 9999], 34), [1, 80, 1838, 4838, 9999])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(numerical_radix_sort([1, 80, 1838, 4838, 9999], 102), [1, 80, 1838, 4838, 9999])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

    def test_singleword_radix_sort(self):
        try:
            self.assertEqual(singleword_radix_sort('zebra'), 'aberz')
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(singleword_radix_sort('apple'), 'aelpp')
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(singleword_radix_sort('m'), 'm')
        except AssertionError as e:
            self.verificationErrors.append(str(e))

    def test_scrabbleHelper(self):
        try:
            self.assertEqual(scrabble_helper(['abc', 'cab', 'bac', 'cbc', 'abb', 'asdas'], ['abc']), [['abc', 'bac', 'cab']])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(scrabble_helper(['abc', 'cab', 'bac', 'cbc', 'abb', 'asdas'], ['abc', 'bab', 'jkre']), [['abc', 'bac', 'cab'], ['abb'], []])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(scrabble_helper(['abc', 'cab', 'bac', 'cbc', 'abb', 'asdas'], ['abc', 'bab', 'jkre', 'cab']), [['abc', 'bac', 'cab'], ['abb'], [], ['abc', 'bac', 'cab']])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(scrabble_helper(['zab', 'jhg', 'uio', 'hweu', 'xcbx', 'a', 'ab'], ['abc', 'baz', 'xbx', 'a', 'iou']), [[], ['zab'], [], ['a'], ['uio']])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(scrabble_helper(['zab', 'jhg', 'uio', 'hweu', 'xcbx', 'a', 'ab', 'asdhjkashjk', 'khjdfg', 'dfgshjk'], ['abc', 'baaz', 'xbx', 'ac', 'iohu']), [[], [], [], [], []])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(scrabble_helper(['asdas', 'sdgdsfg', 'dfgsdfg', 'sdfgsd', 'x', 'sdfgsd', 'sdfgs'], ['abc', 'baaz', 'xbx', 'ac', 'iohu']), [[], [], [], [], []])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(scrabble_helper(['pots', 'stop', 'sotp', 'otps'], ['pots', 'ostp', 'psto', 'ospt']), [['otps', 'pots', 'sotp', 'stop'], ['otps', 'pots', 'sotp', 'stop'], ['otps', 'pots', 'sotp', 'stop'], ['otps', 'pots', 'sotp', 'stop']])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(scrabble_helper(['pots', 'stop', 'sotp', 'otps', 'stomp'], ['pots', 'ostp', 'psto', 'ospt']), [['otps', 'pots', 'sotp', 'stop'], ['otps', 'pots', 'sotp', 'stop'], ['otps', 'pots', 'sotp', 'stop'], ['otps', 'pots', 'sotp', 'stop']])
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(scrabble_helper(['pots', 'stop', 'sotp', 'otps', 'stomp'], ['pots', 'ostp', 'psto', 'p', 'ospt']), [['otps', 'pots', 'sotp', 'stop'], ['otps', 'pots', 'sotp', 'stop'], ['otps', 'pots', 'sotp', 'stop'], [], ['otps', 'pots', 'sotp', 'stop']])
        except AssertionError as e:
            self.verificationErrors.append(str(e))



    def binary_search(self):
        try:
            self.assertEqual(binary_search_anagram_groups([[['abc',0,0], ['abc', 0, 0], ['abc', 0, 0]], [['askld', 0, 0]],[['asdasd',0,0]]], 'abc'), 0)
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(binary_search_anagram_groups([[['askld', 0, 0]],[['asdasd',0,0]], [['abc',0,0], ['abc', 0, 0], ['abc', 0, 0]]], 'abc'), 2)
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(binary_search_anagram_groups([[['abc',0,0], ['abc', 0, 0], ['abc', 0, 0]]], 'abc'), 0)
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(binary_search_anagram_groups([[['abc',0,0], ['abc', 0, 0], ['abc', 0, 0]], [['asfsdf', 0, 0], ['asfsdf', 0, 0]], [['zns', 0,0], ['zns',0,0]]], 'abc'), 0)
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        try:
            self.assertEqual(binary_search_anagram_groups([[['abc',0,0], ['abc', 0, 0], ['abc', 0, 0]], [['asfsdf', 0, 0], ['asfsdf', 0, 0]], [['zns', 0,0], ['zns',0,0]]], 'zns'), 1)
        except AssertionError as e:
            self.verificationErrors.append(str(e))






if __name__ == '__main__':
    unittest.main()
