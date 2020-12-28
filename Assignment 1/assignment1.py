import timeit, random

def count_sort(input_list,  column, base):
    """
    Applies Count sort to a column of digits (not the whole word).
    Sorts all the elements in input list based on that column in ascending order
    Input is a list of words, column or digit being sorted and the base to be used and outputs the numbers in
    ascending order for that column

    :Complexity: O(n + b) where n is the size of the input list and b is the base
    """
    output_list = [0]*len(input_list)
    count_list = [0]*base
    position_list = [0]*base
    # Does the count list
    for i in range(len(input_list)):
        num = int(input_list[i][column])
        count_list[num] += 1
    # Does the position list
    for i in range(1, base):
        position_list[i] = position_list[i-1] + count_list[i-1]
    # Creates the output list
    for i in range(len(input_list)):
        num = int(input_list[i][column])
        output_index = position_list[num]
        position_list[num] += 1
        output_list[output_index] = input_list[i]
    return output_list

def change_of_base(num, b):
    """
    This function changes the base of the input num.
    For example, 2 (in base 10) becomes 10 in base 2
    :complexity: O(logb(num)) where b is the base and num is the number to be changed
    """
    # Calculates the number of digits required to represent the number in the base
    if num >= b:
        dig = 0
        found_dig = False
        while not found_dig:
            if num >= b ** (dig+1):
                dig += 1
            else:
                found_dig = True

    # if num is less than base then the representation is just num
    else:
        return [num]
    # Actually calculates the new representation
    n = num
    result = []
    while n > 0:
        power = dig - len(result)
        quotient = n // b**power
        result.append(quotient)
        n = n - (quotient * b**power)

    # accounts for any extra 0s on the right so that the digits are in the right spot
    while len(result) <= dig:
        result.append(0)
    return result


def change_base_back(num_list, b):
    """
    Changes the numbers from another base (b) back to a representation in base 10
    e.g. 10 in base 2 will be returned as 2 (base 10 representation)

    :Complexity: O(n * M) where n is the length of num list and M is the biggest number of digits that was used
    to represent the numbers in the base in the input
    """
    for i in range(len(num_list)):
        num = 0
        for j in range(len(num_list[i])):
            num += num_list[i][j] * b**(len(num_list[i]) - j-1)
        num_list[i] = num
    return num_list


def numerical_radix_sort(num_list, b):
    """
    Sorts a list of numbers into increasing order using radix sort
    Input a list of numbers and returns a list where the numbers are in ascending order
    :Complexity: O((n+b) * logb(M)) where n is the length of num_list and M is the value of the greatest element in num_list
    """
    new_base_num = []
    max_len = 0
    # Gets new representation of every number with the new base
    for i in num_list:
        num = change_of_base(i, b)
        if len(num) > max_len:
            max_len = len(num)
        new_base_num.append(num)
    # adds zeros to the sort of the number so every number has the same number of digits
    for i in range(len(new_base_num)):
        if len(new_base_num[i]) < max_len:
            no_of_zeros = max_len - len(new_base_num[i])
            new_base_num[i] = [0]*no_of_zeros + new_base_num[i]
    # Count sorts every column from right to left
    for i in range(max_len-1, -1, -1):
        new_base_num = count_sort(new_base_num, i, b)
    # Returns the sorted list with the numbers back in base 10 representation
    return change_base_back(new_base_num, b)


def test_bases(num_list):
    """
    Function used to write csv files measuring the time taken to sort a list using radix sort using different bases
    Input is a list of numbers and it returns a file with the time taken to sort that list with different bases
    :Complexity: O(((n+b) * logb(M))) where n is the length of num_list and M is the value of the greatest element
    in num_list
    """
    file = open("test_base_data4.csv", "w")
    column_headings = "Time, Exponent \n"
    file.write(column_headings)
    # Does radix sort for a range of bases and saves to csv file
    for power in range(1, 16):
        base = 2**power
        start_time = timeit.default_timer()
        numerical_radix_sort(num_list, base)
        time = timeit.default_timer() - start_time
        write_str = str(time) + ", " + str(power) + "\n"
        file.write(write_str)

#random.seed(0)
#data1 = [random.randint(0, 2**8-1) for _ in range(10**4)]
#data2 = [random.randint(0, 2**8-1) for _ in range(10**5)]
#data3 = [random.randint(0, 2**(2**10)-1) for _ in range(10)]
#data4 = [random.randint(0, 2**(2**10)-1) for _ in range(20)]


def scrabble_helper(word_list, char_set_list):
    """
    Given a list of tilesets in char_set_list, the function returns all words from word_list that can be made with
    all the tiles in a tileset for each tileset as a list of lists
    :Complexity: O(nM + qMlog(n)) where n is the length of word list, M is the longest word in word_list and q is the
    length of char_set_list
    """
    alpha_word_list = []
    max_word_len = 0
    # sorts words into tuple: (word with letters in alphabetical order, original word, original position)
    # e.g. apple becomes aelpp
    for i in range(len(word_list)):
        if len(word_list[i]) > max_word_len:
            max_word_len = len(word_list[i])
        alpha_word_list.append((singleword_radix_sort(word_list[i]), word_list[i], i))

    # Sorts char set list into tuples: (chars in alphabetical order, original char_set_list tileset, original position)
    # Does not include tilesets that are longer than the longest word in word_list
    alpha_char_set_list = []
    for i in range(len(char_set_list)):
        if len(char_set_list[i]) <= max_word_len:
            alpha_char_set_list.append((singleword_radix_sort(char_set_list[i]), char_set_list[i], i))

    # Sorts all words into alphabetical order (Each word is currently all the letters in alphabetical order)
    sorted_alpha_word_list = multiword_radix_sort(alpha_word_list, max_word_len)

    # The output from multiword_radix_sort is a list of numbers (ascii values of each letter) so this part turns
    # the numbers back into letters
    for i in range(len(sorted_alpha_word_list)):
        word = []
        for j in range(max_word_len):
            if sorted_alpha_word_list[i][0][j] != 0:
                word.append(chr(sorted_alpha_word_list[i][0][j]+96))
        sorted_alpha_word_list[i][0] = ''.join(word)

    # Combine all of the same anagrams into one list. E.g. 'apple' and 'aeppl' would combine into one list as they are
    # anagrams of each other
    grouped_anagrams = [[sorted_alpha_word_list[0]]]
    group_counter = 0
    for i in range(1, len(sorted_alpha_word_list)):
        if sorted_alpha_word_list[i][0] == sorted_alpha_word_list[i-1][0]:
            grouped_anagrams[group_counter].append(sorted_alpha_word_list[i])
        else:
            grouped_anagrams.append([sorted_alpha_word_list[i]])
            group_counter += 1

    # Prepares lists in a format for output. Just the word without the alphabetical order letters or original position
    output_grouped_anagrams = []
    for i in range(len(grouped_anagrams)):
        group = []
        for j in range(len(grouped_anagrams[i])):
            group.append(grouped_anagrams[i][j][1])
        output_grouped_anagrams.append(group)

    # This chunk sorts each list of anagrams into alphabetical order so the final output is in alphabetical order
    for i in range(len(output_grouped_anagrams)):
        if len(output_grouped_anagrams[i]) > 1:
            max_len = len(output_grouped_anagrams[i][0])
            output_grouped_anagrams[i] = multiword_radix_sort2(output_grouped_anagrams[i], max_len)

            # This turns the words back into their string representation rather than list of ascii values
            for k in range(len(output_grouped_anagrams[i])):
                word = []
                for j in range(max_len):
                    if output_grouped_anagrams[i][k][0][j] != 0:
                        word.append(chr(output_grouped_anagrams[i][k][0][j] + 96))
                output_grouped_anagrams[i][k] = ''.join(word)

    # Finds the words that can be made using each tileset in char_set_list using binary search
    # Only compares to the groups of anagrams rather than the whole list
    final_output_list = []
    for i in range(len(char_set_list)):
        final_output_list.append([])
    for i in range(len(alpha_char_set_list)):
        index = binary_search_anagram_groups(grouped_anagrams, alpha_char_set_list[i][0])
        if index is not None:
            final_output_list[alpha_char_set_list[i][2]] = output_grouped_anagrams[index]
    return final_output_list

def singleword_radix_sort(word):
    """
    Sorts a word so that the letters are in alphabetical order
    Input is a string and output is a string in alphabetical order
    e.g. 'apple' becomes 'aelpp'
    :Complexity: O(len(word))
    """
    # Turns every string into its ascii value
    radix_sort_list = []
    for char in word:
        radix_sort_list.append(ord(char) - 97)
    # complexity is O(M)
    # radix sorts the list using the ascii values of the strings
    radix_sort_list = numerical_radix_sort(radix_sort_list, 26)
    # Turns the strings back to string form and returns it
    for i in range(len(radix_sort_list)):
        radix_sort_list[i] = chr(radix_sort_list[i]+97)
    return ''.join(radix_sort_list)

def multiword_radix_sort(word_list, max_word_len):
    """
    Sorts a list of words into alphabetical ascending order. This function is used to sort all the words in word_list
    that already have their letters in alphabetical order
    :Complexity: O(n*M) where N is the length of the word_list and M is the max_word_len
    """
    new_words_list = []
    # turns each letter into it ascii value - 1 and makes a new list with each element =
    # [[letters in ascii values], original word, original position of word]
    for i in range(len(word_list)):
        letter_list = []
        for char in word_list[i][0]:
            letter_list.append(ord(char)-96)
        new_words_list.append([letter_list, word_list[i][1], i])

    # Adds zeros onto words where the number of letters is less than the maximum number of letters of any word
    for i in range(len(new_words_list)):
        if len(new_words_list[i][0]) < max_word_len:
            no_of_zeros = max_word_len - len(new_words_list[i][0])
            new_words_list[i][0] = new_words_list[i][0] + [0]*no_of_zeros

    # Count sorts each word from right to left. Each word is represented as a list of the ascii values of each letter
    for i in range(max_word_len-1, -1, -1):
        new_words_list = count_sort_scrabble(new_words_list, i, 27)
    return new_words_list

def multiword_radix_sort2(word_list, max_word_len):
    """
    Sorts a list of words into alphabetical ascending order. This function is used to sort the grouped anagrams
    :Complexity: O(n*M) where N is the length of the word_list and M is the max_word_len
    """
    new_words_list = []
    # turns each letter into its ascii value - 1 and makes a new list with each element =
    # [[letters in ascii values], original word, original position of word]
    for i in range(len(word_list)):
        letter_list = []
        for char in word_list[i]:
            letter_list.append(ord(char)-96)
        new_words_list.append([letter_list, word_list[i], i])
    # Complexity is O(n*M)
    # Count sorts each word from right to left. Each word is represented as a list of the ascii values of each letter
    for i in range(max_word_len-1, -1, -1):
        new_words_list = count_sort_scrabble(new_words_list, i, 27)
    return new_words_list



def count_sort_scrabble(input_list, column, base):
    """
    Applies Count sort to a list of words for only one column/digit
    Input a list of words but each word is a list of letters in their ascii value and output is a list of the
    number representation of each word but in alphabetical order
    :Complexity: O(nM) where n is the length of the input_list and M is the number of characters in the longest word in
    input_list
    """
    output_list = [0]*len(input_list)
    count_list = [0]*base
    position_list = [0]*base
    # Creates the count array
    for i in range(len(input_list)):
        num = input_list[i][0][column]
        count_list[num] += 1
    # Creates the position array
    for i in range(1, base):
        position_list[i] = position_list[i-1] + count_list[i-1]
    # Creates the output list
    for i in range(len(input_list)):
        num = input_list[i][0][column]
        output_index = position_list[num]
        position_list[num] += 1
        output_list[output_index] = input_list[i]
    return output_list

def binary_search_anagram_groups(input_list, target):
    """
    Applies binary search to find which sublist matches the target
    Input is a list of anagrams that are grouped together if they are anagrams of each other and returns the index
    of the group of anagrams if it matches target else it returns None
    Based of the psuedocode given on page 2 of the FIT2004 course notes by Daniel Anderson
    :Complexity = O(M*logn) where n is the length of input_list and M is the length of target
    """
    hi = len(input_list)
    lo = 0
    # changes lo/hi depending on which side of mid the target should be
    while lo < hi -1:
        mid = (lo+hi)//2
        if target >= input_list[mid][0][0]:
            lo = mid
        else:
            hi = mid
    if input_list[lo][0][0] == target:
        return lo
    else:
        return None