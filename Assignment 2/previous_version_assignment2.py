"""
TODO: ADD FILE HEADER

"""

from math import inf
import timeit
from random import randint
import sys


def optimise_single_pickup(corridor):
    """
    This function goes through a list of items with their value and determines the optimal solution of items to be
       picked up. It returns a tuple with the total value of items in the optimal solution as well as a list showing
       which items are to be picked up to get the optimal solution. 0 indicating to not pick up and 1 indicating to pick
       up that item.

       :Time Complexity: O(N^2) where N is the length of the corridor.
       :Space Complexity: O(N^2) where N is the length of the corridor.
       """

    # if corridor has only one element
    if len(corridor) == 1:
        return 0, [0]

    # Sets up empty memo array
    memo = []
    for i in range(len(corridor)):
        memo.append([None] * (len(corridor) + 1))
    # The first element has to be skipped
    memo[0][1] = 0

    # Goes through cells in a 2d array where each row represents energy and col represents element in corridor
    for col in range(1, len(memo)):
        for energy in range(col + 2):
            # to get to current cell, looking at previous column with 1 more energy and then seeing if it can pick up \
            # the current element
            if energy + 1 < len(corridor):
                cell_value1 = memo[col-1][energy+1]
                if cell_value1 is not None:
                    cell_value1 += corridor[col]
            # Max energy so there is no cell with 1 more energy in previous column
            else:
                cell_value1 = None

            # If after dealing with the current item there is energy, it could have skipped the current item and saved
            # from the previous column
            if energy > 0:
                cell_value2 = memo[col-1][energy-1]
            # If at no energy then it must have picked up the current item
            else:
                cell_value2 = None

            # No previous solutions
            if cell_value1 is None and cell_value2 is None:
                final_cell_value = None

            # If there was no previous column with more energy, the current cell must have not picked up the current
            # item and saved energy
            elif cell_value1 is None:
                final_cell_value = cell_value2

            # If at the bottom with no energy, it must have picked up the current item
            elif cell_value2 is None:
                final_cell_value = cell_value1

            # Else if there is an option to both pick up the current item and skip the item to get to the current
            # spot in the memo array, pick the best value solution
            else:
                final_cell_value = max(cell_value1, cell_value2)
            memo[col][energy] = final_cell_value
    return optimal_solution_single_pickup(memo)


def optimal_solution_single_pickup(memo):
    """ Using an already filled in memo table of the optimal value to reach any given element and energy value, this
    function calculates both the value of the best solution as well as the combination of items to be picked up to reach
    that optimal solution.

    :Time Complexity: O(N) where N is the length of memo.
    :Space Complexity: O(N^2) where N is the length of memo.
    """
    # Calculates what the maximum value is and saves which row
    maxvalue = None
    for i in range(len(memo)+1):
        if maxvalue is None:
            if memo[len(memo)-1][i] is not None:
                maxvalue = (memo[len(memo)-1][i], i)
        else:
            if memo[len(memo)-1][i] is not None:
                if memo[len(memo)-1][i] > maxvalue[0]:
                    maxvalue = (memo[len(memo)-1][i], i)

    # Goes back and calculates how the solution was formed
    optimal_solution = [0] * len(memo)
    current_row = maxvalue[1]
    # Goes backwards through the array starting at the best value
    for j in range(len(memo)-1, 0, -1):
        if current_row > 0:
            # Checks if it did pick up. If current cell does not have the same value as the previous column with
            # 1 less energy then it must have picked up
            if memo[j][current_row] != memo[j-1][current_row-1]:
                optimal_solution[j] = 1
                current_row += 1
            else:
                current_row -= 1
        # If at 0 energy then it must have picked up
        else:
            optimal_solution[j] = 1
            current_row += 1
    return maxvalue[0], optimal_solution

def optimise_multiple_pickup(corridor):
    """
    TODO: FINISH THIS
    :Time Complexity: O(N^2) where N is the length of the corridor.
    :Space Complexity: O(N^2) where N is the length of the corridor.
    """

    # if corridor has only one element
    if len(corridor) == 1:
        return 0, [0]

    # Sets up empty memo array
    memo = []
    for i in range(len(corridor)):
        x = []
        for j in range(len(corridor)+2):
            x.append([None, None])
        memo.append(x)
#        memo.append([None] * (len(corridor) + 1))
    # The first element has to be skipped
    memo[0][1][0] = 0
    memo[0][1][1] = 0

    # Goes through cells in a 2d array where each row represents energy and col represents element in corridor
    for col in range(1, len(memo)):
        for energy in range(col + 2):
            # to get to current cell, looking at previous column with 1 more energy and then seeing if it can pick up \
            # the current element. It builds off the best value in the previous column, 1 more energy
            if energy + 1 < len(corridor):
                if memo[col-1][energy+1][0] is None:
                    cell_value1 = memo[col-1][energy+1][1]
                elif memo[col-1][energy+1][1] is None:
                    cell_value1 = memo[col - 1][energy + 1][0]
                else:
                    cell_value1 = max(memo[col-1][energy+1][0], memo[col-1][energy+1][1])
                if cell_value1 is not None:
                    cell_value1 += corridor[col]
            # Max energy so there is no cell with 1 more energy in previous column
            else:
                cell_value1 = None

            # If after dealing with the current item there is energy, it could have skipped the current item and saved
            # from the previous column
            if energy > 0:
                cell_value2 = memo[col-1][energy-1][1]
            # If at no energy then it must have picked up the current item
            else:

                cell_value2 = cell_value1

            # Cell value 1 is it picked up, cell_value 2 is it did not pick up
            final_cell_value = [cell_value1, cell_value2]

            memo[col][energy] = final_cell_value
    return optimal_solution_multiple_pickup(memo)

def optimal_solution_multiple_pickup(memo):
    """ #TODO THIS

    :Time Complexity: O(N) where N is the length of memo.
    :Space Complexity: O(N^2) where N is the length of memo.
    """
    # Calculates what the maximum value is and saves which row and [col][energy] index
    maxvalue = None

    for i in range(len(memo)+1):
        # Sets up initial value
        if maxvalue is None:
            # Sets initial value to first non empty cell[1]
            if memo[len(memo)-1][i][1] is not None:
                maxvalue = (memo[len(memo)-1][i][1], i, 1)
            # Compares first non empty cell[1] with first non empty cell[0]
            if memo[len(memo)-1][i][0] is not None:
                if maxvalue is not None:
                    if memo[len(memo) - 1][i][0] > maxvalue[0]:
                        maxvalue = (memo[len(memo) - 1][i][0], i, 0)
                # In case first non empty cell[1] was None
                else:
                    maxvalue = (memo[len(memo) - 1][i][0], i, 0)
        # After initial value is set
        else:
            if memo[len(memo)-1][i][1] is not None:
                if memo[len(memo)-1][i][1] > maxvalue[0]:
                    maxvalue = (memo[len(memo)-1][i][1], i, 1)
            if memo[len(memo)-1][i][0] is not None:
                if memo[len(memo)-1][i][0] > maxvalue[0]:
                    maxvalue = (memo[len(memo)-1][i][0], i, 0)

    # Goes back and calculates how the solution was formed
    optimal_solution = [0] * len(memo)
    current_row = maxvalue[1]
    current_index = maxvalue[2]
    # Goes backwards through the array starting at the best value
    for col in range(len(memo)-1, 0, -1):
        # For energy > 0 where it has the choice to pick up or not
        if current_row > 0:
            # Checks if it did pick up. If current cell does not have the same value as the previous column with
            # 1 less energy[current_index] then it must have picked up
            if memo[col][current_row][current_index] != memo[col-1][current_row-1][1]:
                optimal_solution[col] = 1


                # Picks the maximum number from previous column and 1 more energy
                if memo[col-1][current_row+1][0] is None:
                    current_index = 1
                elif memo[col-1][current_row+1][1] is None:
                    current_index = 0
                else:
                    if memo[col-1][current_row+1][0] > memo[col-1][current_row+1][1]:
                        current_index = 0
                    else:
                        current_index = 1
                current_row += 1
            # it did not pick up
            else:
                current_row -= 1
                current_index = 1
        # If at 0 energy then it must have picked up
        else:
            optimal_solution[col] = 1
            current_row += 1
            if memo[col - 1][1][0] is None:
                current_index = 1
            elif memo[col - 1][1][1] is None:
                current_index = 0
            else:
                if memo[col - 1][1][0] > memo[col - 1][1][1]:
                    current_index = 0
                else:
                    current_index = 1
    return maxvalue[0], optimal_solution


def optimal_shade_selector(shades, probs):
    """

    Time Complexity: O(N^3) where N is the length of shades or length of probs
    :param shades:
    :param probs:
    :return:
    """
    # Each list in subtree_solutions is a list of solutions involving the ith element in shades
    # First element  is the elements used to make that subtree
    # Every other element is value of each level of the subtree without being adjusted for the multiplier for each level

    if len(shades) == 0:
        return 0
    subtree_solutions = [[]]
    # O(n)
    for colour_index in range(len(shades)):
        len_of_previous_solutions = len(subtree_solutions[-1])
        # adds the subtree made with just the new shade
        if len(subtree_solutions[0]) == 0:
            subtree_solutions[0] = [[[shades[colour_index]], probs[colour_index]]]
        else:
            subtree_solutions.append([[[shades[colour_index]], probs[colour_index]]])
        # Adds the new shade to the combinations made when the previous shade was added
        # O(n)
        for previous_combinations_index in range(len_of_previous_solutions):
            colours_sublist = subtree_solutions[colour_index-1][previous_combinations_index][0] + [shades[colour_index]]
            #O(n^2) function
            for i in range(len(shades)):
                if colours_sublist[0] == shades[i]:
                    index_in_shades = i
            optimal_solution = optimal_subtree(shades, probs, subtree_solutions, colours_sublist, index_in_shades)
            subtree_solutions[colour_index].append(optimal_solution)

    full_solution = subtree_solutions[-1][-1]
    output_value = 0
    level = 1
    for j in range(1, len(full_solution)):
        output_value += full_solution[j] * level
        level += 1
    return subtree_solutions, output_value

def optimal_subtree(shades, probs, subtree_solutions, colours_sublist, index_in_shades):
    """ Given a list of shades in colour_sublist and given the previous solutions in subtree_solutions, the function
    will return the most optimal way to arrange the colour_sublist
    O(n^2)
    """
    optimal_subtree_value = inf
    solution_tuple = ()
    # Tries out the subtrees made from every element being the root
    # O(n)
    for i in range(len(colours_sublist)):
        root = colours_sublist[i]
        if i == 0:
            left_subtree = []
        elif i == 1:
            left_subtree = [colours_sublist[0]]
        else:
            left_subtree = [colours_sublist[0]] + [colours_sublist[i - 1]]

        if i == len(colours_sublist) - 2:
            right_subtree = [colours_sublist[len(colours_sublist)-1]]
        elif i == len(colours_sublist) - 1:
            right_subtree = []
        else:
            right_subtree = [colours_sublist[i + 1]] + [colours_sublist[len(colours_sublist) - 1]]


        # for all solutions made when the i-1 shade was added. Doing left subtree
        if len(left_subtree) == 0:
            left_values = [[]]
        else:
            # O(n)
            for j in range(len(subtree_solutions[index_in_shades + i- 1])):
                # finding previous saved solution for this specific subtree
                if len(subtree_solutions[index_in_shades + i - 1][j][0]) == 1:
                    if left_subtree == subtree_solutions[index_in_shades + i - 1][j][0]:
                        left_values = subtree_solutions[index_in_shades + i - 1][j]
                elif left_subtree[0] == subtree_solutions[index_in_shades + i - 1][j][0][0] and left_subtree[-1] == subtree_solutions[index_in_shades + i - 1][j][0][-1]:
                    left_values = subtree_solutions[index_in_shades + i - 1][j]

        if len(right_subtree) == 0:
            right_values = [[]]
        else:
            # finds index of last element of right subtree in shades
            #(O(n)
            for n in range(len(shades)):
                if right_subtree[-1] == shades[n]:
                    right_shades_index = n
            # O(n)
            for j in range(len(subtree_solutions[right_shades_index])):
                if len(subtree_solutions[right_shades_index][j][0]) == 1:
                    if right_subtree == subtree_solutions[right_shades_index][j][0]:
                        right_values = subtree_solutions[right_shades_index][j]
                elif right_subtree[0] == subtree_solutions[right_shades_index][j][0][0] and right_subtree[-1] == subtree_solutions[right_shades_index][j][0][-1]:
                    right_values = subtree_solutions[right_shades_index][j]

        # First element is what combination of elements. Everything after is the value of that level when combining both
        # left and right subtrees
        #O(N)
        temp_solution_list = []
        temp_solution_list.append(colours_sublist)
        temp_solution_list.append(probs[index_in_shades + i])
        # If the right subtree is longer than left
        # O(n)
        if len(right_values) > len(left_values):
            k = 1
            while k < len(left_values):
                temp_solution_list.append(left_values[k] + right_values[k])
                k += 1
            while k < len(right_values):
                temp_solution_list.append(right_values[k])
                k += 1

        # if the left subtree is longer than right subtree
        elif len(left_values) > len(right_values):
            k = 1
            while k < len(right_values):
                temp_solution_list.append(left_values[k] + right_values[k])
                k += 1
            while k < len(left_values):
                temp_solution_list.append(left_values[k])
                k += 1
        # If both subtrees are the same length
        else:
            for k in range(1, len(right_values)):
                temp_solution_list.append(left_values[k] + right_values[k])

        #O(n)
        value = probs[index_in_shades + i - 1]
        level = 2
        for k in range(2, len(temp_solution_list)):
            value += level * temp_solution_list[k]
            level += 1

        # O(1)
        if value < optimal_subtree_value:
            optimal_subtree_value = value
            solution_tuple = temp_solution_list

    return solution_tuple

test_shades = [0.1, 0.2, 0.3]
test_probs = [0.3, 0.5, 0.35]
test_subtree_solutions = [[[[0.1], 0.3]],
                          [[[0.2], 0.5], [[0.1, 0.2], 0.5, 0.3]],
                          [[[0.3], 0.35], [[0.2, 0.3], 0.5, 0.35]]
                        ]
test_colours_sublist = [0.1, 0.2, 0.3]

#print(optimal_subtree(test_shades, test_probs, test_subtree_solutions, test_colours_sublist))
print(optimal_shade_selector([0.1, 0.2, 0.3, 0.4, 0.5], [0.15, 0.05, 0.2, 0.25, 0.35]))
#print(optimal_shade_selector([0.1, 0.2], [0.2, 0.8]))
#print(optimal_shade_selector([0.01, 0.02, 0.03, 0.04, 0.05, 0.06], [0.11, 0.2, 0.21, 0.18, 0.15, 0.15]))
#print(optimal_shade_selector([0.04, 0.05, 0.06], [0.18, 0.15, 0.15]))


def sum_to_1(length): # Randomly generate a list of numbers that sums to 1
    res = [1] * length
    while sum(res) < 100:
        res[randint(0, length - 1)] += 1
    for i in range(length):
        res[i] /= 100
    return res

#if __name__ == "__main__":
#    in1 = [(i+1)/10 for i in range(10)]
#    in2 = sum_to_1(10)
#    in3 = [(i+1)/20 for i in range(20)]
#    in4 = sum_to_1(20)
#    sys.setrecursionlimit(10000)
#    timebefore = timeit.default_timer()
#    optimal_shade_selector(in1, in2)
#    print(timeit.default_timer() - timebefore)
#    timebefore = timeit.default_timer()
#    optimal_shade_selector(in3, in4)
#    print(timeit.default_timer() - timebefore)