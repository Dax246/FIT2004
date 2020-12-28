"""
This file contains the code to solve FIT2004 Assignment 3
Author: Damien Ambegoda (30594235)
Last modified: 8/10/2020

Classes:
Node - Creates the nodes that make the trie
Trie1 - The Trie used to do question 1. Uses the Node class
SuffixTrie - A suffix trie used for question 1 that inherits from Trie 1. Uses the node class.
PrefixTrie - A prefix trie used for question 2. Uses the node class

Functions:
letter_to_ascii_based_index - The links from one letter to another letter is based on the node.links array. The array is
                              indexed based on the 2nd character. This function returns the index that should store
                              the location of the 2nd character

build_from_substring - Given two strings, the function calculates which substrings from the 1st string can be used to
                       make the 2nd string. Function used for question 1 of the assignment

alpha_pos - Given two lists of strings, it identifies how many strings from the first list are alphabetically before
            each string in the 2nd list. Function used for question 2 of the assignment

"""


class Node:
    """ Nodes needed to build the trie. Each node represents a single letter

    self.letter is the letter that node represents
    self.links keeps track of all nodes that are below the current node.
    self.links[0] is $ and the rest are the letters of the alphabet in alphabetical order
    self.letter_index is the index of the character in the letter
    self.word_count keeps track of how many words have been inserted that have passed this node
    """

    def __init__(self, letter, letter_index=0):
        """ Initiates the node and instance variables

        Time Complexity = O(1)
        """
        self.letter = letter
        self.letter_index = letter_index
        self.word_count = 0
        self.links = [None] * 27


def letter_to_ascii_based_index(letter):
    """ Given a letter, it determines the index the letter should be stored in the node.links array

    Time complexity = O(1)
    """
    return ord(letter) - 96


class Trie1:
    """ Creates the Trie used in question 1.

    self.root is the root of the trie and is an empty node

    """

    def __init__(self):
        """ Initiates Trie1 with just an empty root node.

        Time Complexity = O(1)

        """
        self.root = Node(None, None)

    def traversal(self, target_string, index_substring=None):
        """ Given a string, the function traverses through the trie using that string. If the string is already in the
        trie then the function returns True. If the string is not completely in the trie already, it returns False,
        the current node (so that the new characters can be added to that node) and which letters have been traversed.
        This function is called by the insertion function.

        Time Complexity = O(n) where n is the length of target_string
        """
        curr_node = self.root
        # List stores the characters that have been traversed. It stores their index of the string
        traversed_letters = []
        # Traversal from build_from_substring. Instead of traversing from the start of the string, only traverse from
        # a certain index
        if index_substring is not None:
            for char_index in range(index_substring, len(target_string)):
                index = letter_to_ascii_based_index(target_string[char_index])
                if curr_node.links[index] is None:
                    # char_index is the first letter that is missing
                    return False, curr_node, traversed_letters
                else:
                    curr_node = curr_node.links[index]
                    traversed_letters.append(curr_node.letter_index)
        else:
            for char_index in range(len(target_string)):
                index = letter_to_ascii_based_index(target_string[char_index])
                if curr_node.links[index] is None:
                    # char_index is the first letter that is missing
                    return False, curr_node, traversed_letters
                else:
                    curr_node = curr_node.links[index]
                    traversed_letters.append(curr_node.letter_index)
        return True, None, traversed_letters

    def insertion(self, string, string_index):
        """ Given a string, this function inserts the string into the trie. It first traverses the trie by calling the
        traversal method, to determine how much of the string is already in the trie and then adds the rest.

        :param string_index: index of the substring from the original string. This is used so that the index of the char
        can be saved in the node under node.letter_index
        Time Complexity: O(n) where n is the length of the string
        """
        res = self.traversal(string)
        curr_node = res[1]
        if res[2] == []:
            for char_index in range(len(string)):
                index = letter_to_ascii_based_index(string[char_index])
                curr_node.links[index] = Node(string[char_index], char_index + string_index)
                curr_node = curr_node.links[index]
        else:
            for char_index in range(len(res[2]), len(string)):
                index = letter_to_ascii_based_index(string[char_index])
                curr_node.links[index] = Node(string[char_index], char_index + string_index)
                curr_node = curr_node.links[index]


class SuffixTrie(Trie1):
    """ Trie used in question 1 that builds of Trie1. Contains the insert_suffixes method which is used only in suffix
    trees

    """

    def __init__(self):
        """ Initiates SuffixTree which just creates a trie from the Trie class
        Time Complexity = O(1)
        """
        Trie1.__init__(self)

    def insert_suffixes(self, string):
        """ Given a string, this function inserts all the suffixes into a SuffixTrie's Trie.

        Time Complexity = O(n^2) where n is the length of the string)
        """
        # Adds the suffixes starting from the end
        for i in range(len(string), -1, -1):
            suffix_string = string[i:len(string)]
            SuffixTrie.insertion(self, suffix_string, i)


def build_from_substrings(S, T):
    """ Given two strings, the function determines which substrings in S can be used to make T. If it is not possible,
    the function returns false

    Time Complexity: O(N^2 + M) where N is the number of characters in S and M is the number of characters in T
    """
    trie = SuffixTrie()
    # O(n^2)
    # Creates a trie with all substrings of S
    trie.insert_suffixes(S)
    res = []
    # Traversing only the unsolved part of the T. The index is kept of track of and passed to the traversal method
    current_target_index = 0
    # O(M)
    while current_target_index < len(T):
        # Traverses down the Suffix Trie of S as far as possible to determine the substring of S that can make the
        # first characters of current_target
        traversal_res = trie.traversal(T, current_target_index)
        # If the trie has not been traversed at all, that means that it is not possible to make T using substrings
        # of S so should return False
        # traversal_res[2] keeps track of the indexes of the traversed characters from S
        if traversal_res[2] == []:
            return False
        else:
            # One issue with the node.letter_index is that it only keeps track of the index of the character that makes
            # a node when the node was created. Sometimes multiple characters with different indexes will point to the
            # same node.
            # e.g. AAB. There will be an A node from the root node that will be given index 1. However the index 0 A
            # will also use that node but the function will think its index is 1.
            # This for loop fixes this issue by ensuring that the indexes increase by 1 from left to right
            for i in range(len(traversal_res[2]) - 1, 0, -1):
                if len(traversal_res[2]) > 1:
                    if traversal_res[2][i - 1] != traversal_res[2][i] - 1:
                        traversal_res[2][i - 1] = traversal_res[2][i] - 1
            first_last_of_traversed_strings = (traversal_res[2][0], traversal_res[2][-1])
        res.append(first_last_of_traversed_strings)
        # Removes adds indexes to the "solved" part of T
        current_target_index = current_target_index + len(traversal_res[2])
    return res


class PrefixTrie:
    """ Creates a prefix trie to be used for question 2. Uses the node class.
    """

    def __init__(self):
        """ Initialises PrefixTrie
        PrefixTrie.root is the root of the trie. The root is an empty Node
        PrefixTrie.root.links[0] adds '$' as a word in the Trie.

        Time Complexity = O(1)
        """
        self.root = Node(None)
        self.root.links[0] = Node('$')

    def insert_traversal(self, target_string):
        """ Traversal used when trying to insert a string. Returns false, the current node and the indexes of characters
        in the trie already for strings that are not already in the trie. Returns True if the string and appropriate
        $ is in the trie already.

        Time Complexity = O(n) where n is the length of target_string
        """
        curr_node = self.root
        # Word count keeps track of how many inserted strings in the Trie pass through the current node
        curr_node.word_count += 1
        for char_index in range(len(target_string)):
            index = letter_to_ascii_based_index(target_string[char_index])
            # If the next letter is not linked to the current_node, then the string is not in the trie
            if curr_node.links[index] is None:
                # char_index is the first letter that is missing
                return False, curr_node, char_index
            else:
                # If the next letter is linked to the current node, make the next letter node the current node
                curr_node = curr_node.links[index]
                curr_node.word_count += 1
        # Checking if the completed string also has a $ and that the target_string is not just a prefix of another word
        if curr_node.links[0] is None:
            return False, curr_node, len(target_string)
        return True, curr_node, None

    def insertion(self, string):
        """ Inserts a string into the Trie. First traverses the Trie to see how many letters are already in then
        adds in the new characters starting from the final traversed node.

        Time Complexity = O(n) where n is the length of string
        """
        insert_traversal_res = self.insert_traversal(string)
        # If the string and $ is connected to the last character, then the string is in the Trie and nothing needs to be
        # inserted. (insert_traversal would return True)
        if insert_traversal_res[0]:
            curr_node = insert_traversal_res[1]
            curr_node.links[0].word_count += 1
            return
        else:
            curr_node = insert_traversal_res[1]
            # For all characters not in the Trie already, inserts them in
            for char_index in range(insert_traversal_res[2], len(string)):
                index = letter_to_ascii_based_index(string[char_index])
                curr_node.links[index] = Node(string[char_index])
                curr_node = curr_node.links[index]
                # Word count will be 1 as this current string being added would be the only string that builds off
                # the new nodes at the moment
                curr_node.word_count += 1
            # Adds '$' node as a link to the last character of string to indicate the end of the string
            curr_node.links[0] = Node('$')
            curr_node.links[0].word_count += 1

    def nonedit_traversal(self, string):
        """ Given a string, this function traverses through the trie. This function is not called by the insertion'
        method so the word_count should not be updated during the traversal and does not need to return
        arguments needed for insertion. Instead called by alpha_pos. Returns the word_count which is how many words
        that are lexicographically before string.

        Time Complexity = O(n) where n is the length of the string
        """
        word_count_res = 0
        curr_node = self.root
        for char in string:
            index = letter_to_ascii_based_index(char)
            # Gets the word_count for all characters that are lexicographically before the current letter in string and
            # is connected to the same previous character
            for i in range(index):
                if curr_node.links[i] is not None:
                    word_count_res += curr_node.links[i].word_count
            # Traverses to the next node
            if curr_node.links[index] is not None:
                curr_node = curr_node.links[index]
            # If the next character is not on the Trie then ends the function
            else:
                return word_count_res
        return word_count_res


def alpha_pos(text, query_list):
    """ Given two lists of strings, the function returns how many strings in text are lexicographically before each
    string in query list

    Time Complexity = O(C + Q) where C is the total number of characters in text and Q is the total number of characters
    in query_list
    """
    trie = PrefixTrie()
    # inserts all the strings in text into the PrefixTrie
    # O(C)
    for word in text:
        trie.insertion(word)
    res = []
    # Traverses through the PrefixTrie for each word in query_list and determines how many strings in text are
    # lexicographically before the word in query_list
    for word in query_list:
        res_for_each_word = trie.nonedit_traversal(word)
        res.append(res_for_each_word)
    return res


print(alpha_pos(["a","a"],["ab"]))