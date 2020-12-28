"""
This file contains the functions required for the FIT2004 Assignment 2 - Dynamic Programming.
The file has 6 functions.

Question 1:
-Optimise_single_pickup calculates the optimal combination of items to be picked up when the robot is not broken.
-Optimal_solution_single_pickup is an auxiliary function that calculates the best solution and what combination of items
gets the optimal solution

Question 2:
- Optimise_multiple_pickup calculates the optimal combination of items when the robot is broken.
- Optimal_solution_multiple_pickup is an auxiliary function that calculates the best solution and what combination of
items get the optimal solution

Question 3:
- Optimal_shade_selector calculates the value of the best tree given a list of shades and their probabilities of being
chosen
- Optimal_subtree is an auxiliary function that calculates the optimal subtree given a list of elements

Author: Damien Ambegoda (30594235)
Last modified: 17/9/2020

"""

from math import inf

def optimise_single_pickup(corridor):
    """ This function goes through a list of items with their value and determines the optimal solution of items to be
    picked up. It returns a tuple with the total value of items in the optimal solution as well as a list showing
    which items are to be picked up to get the optimal solution. 0 indicating to not pick up and 1 indicating to pick
    up that item.

    The overlapping subproblems is the best value of items that can be picked up for each set of items from the start
    and final energy level.

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
            # to get to current cell, looking at previous column with 1 more energy and then seeing if it can pick up
            # the current element
            if energy + 1 < len(corridor):
                cell_value1 = memo[col-1][energy+1]
                if cell_value1 is not None:
                    cell_value1 += corridor[col]
            # Max energy so there is no cell with 1 more energy in previous column
            else:
                cell_value1 = None

            # If after dealing with the current item there is energy, it could have skipped the current item and saved
            # from the previous column with 1 less energy
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
    """ Given a list of numbers, the function returns the maximum value that can be picked up and the combination
    of items to be picked up. This function is different to single pickup as once an item is picked up, items will keep
    being picked up until energy=0.

    The overlapping subproblems is the best value of items that can be picked up for each set of items from the start
    and final energy level.

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
    """ Input is the memo array which has saved the max value that can be gathered by that element and with a specific
    amount of energy. It saves both the value if the robot skipped the current item and if it picked up that item.
    The function returns which objects have been picked up in a list like [0, 1, 0, 1, 0] where 0 means the item has
    been picked up and 1 means the item has been picked up. The function also returns the value of the optimal
    combination of items picked up.

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
        # After initial value is set. Compares it the other value in that cell to get maximum
        else:
            if memo[len(memo)-1][i][1] is not None:
                if memo[len(memo)-1][i][1] > maxvalue[0]:
                    maxvalue = (memo[len(memo)-1][i][1], i, 1)
            if memo[len(memo)-1][i][0] is not None:
                if memo[len(memo)-1][i][0] > maxvalue[0]:
                    maxvalue = (memo[len(memo)-1][i][0], i, 0)

    # Goes back and calculates how the optimal solution was formed
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
            # otherwise it did not pick up
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
    """ Given a list of shades and their probability of being chosen, this function returns the value of the optimal
    tree such that higher probability shades are higher up on the tree.
    The value calculation involves summing for each level, the probability of each level * the level number

    Overlapping subproblems are the optimal tree that can be created given a set of shades as well as the price of said
    tree.

    Time Complexity: O(N^3) where N is the length of shades

    """
    # Each list in subtree_solutions is a list of solutions involving that shade. 3rd index means combinations made with
    # the third shade
    # First element in each nested list is the elements used to make that subtree
    # Every other element in the nested list value of each level of the subtree without being adjusted for the
    # multiplier for each level

    # Subtree_solutions_values is a list of the values of that subtree. Each element corresponds with the combination
    # in subtree_solutions

    if len(shades) == 0:
        return 0
    subtree_solutions = [[]]
    subtree_solutions_values = [[]]
    # O(n)
    for colour_index in range(len(shades)):
        len_of_previous_solutions = len(subtree_solutions[-1])
        # adds the subtree made with just the new shade
        if len(subtree_solutions[0]) == 0:
            subtree_solutions[0] = [[[shades[colour_index]], probs[colour_index]]]
            subtree_solutions_values = [[probs[colour_index]]]
        else:
            subtree_solutions.append([[[shades[colour_index]], probs[colour_index]]])
            subtree_solutions_values.append([probs[colour_index]])

        # Calculates the new combinations that are created when the new shade is added to all combinations made when
        # the previous shade combinations were calculated
        # If the 4th shade is being calculated, it will be appended to all the combinations made when the 3rd shade was
        # calculated
        # O(n)
        for previous_combinations_index in range(len_of_previous_solutions):
            # Creates the sublist of shades that the tree has to be calculated for
            colours_sublist = subtree_solutions[colour_index-1][previous_combinations_index][0] + [shades[colour_index]]
            # O(n)
            # Finds what index the first shade of the colours sublist has in the shades/probs list
            for i in range(len(shades)):
                if colours_sublist[0] == shades[i]:
                    index_in_shades = i
            # O(n) function
            # Calls the aux function that calculates the optimal subtree and its value
            optimal_solution, optimal_value = optimal_subtree(probs, subtree_solutions, subtree_solutions_values, colours_sublist, index_in_shades)
            subtree_solutions[colour_index].append(optimal_solution)
            subtree_solutions_values[colour_index].append(optimal_value)

    # The value of the subtree that has every shade is the final answer
    return subtree_solutions_values[-1][-1]

def optimal_subtree(probs, subtree_solutions, subtree_solution_values, colours_sublist, index_in_shades):
    """ Given a list of shades in colour_sublist, given the previous solutions in subtree_solutions and given the
    values of each subtree in subtree_solutions_values, the function will return the most optimal way to arrange
    the colour_sublist.
    Time Complexity: O(K) where K is the length of colours_sublist. At its worst, len(colours_sublist) will be equal
    to the length of probs/shades
    """
    list_of_all_roots = []

    # Tries out the subtrees made from every element being the root
    # O(n)
    for i in range(len(colours_sublist)):
        root = colours_sublist[i]
        # The left subtree is every colour lighter than the root
        # following block notes down the first and if the subtree is longer than 1, the last element in the left subtree
        if i == 0:
            left_subtree = []
        elif i == 1:
            left_subtree = [colours_sublist[0]]
        else:
            left_subtree = [colours_sublist[0]] + [colours_sublist[i - 1]]
        # Important as left_subtree does not save the entire left subtree but only the first and last elements
        actual_length_of_left_subtree = i

        # The right subtree is every colour darker than the root
        # following block notes down the first and if the subtree is longer than 1, the last element in the right subtree
        if i == len(colours_sublist) - 2:
            right_subtree = [colours_sublist[len(colours_sublist)-1]]
        elif i == len(colours_sublist) - 1:
            right_subtree = []
        else:
            right_subtree = [colours_sublist[i + 1]] + [colours_sublist[len(colours_sublist) - 1]]
        # Important as right_subtree does not save the entire right subtree but only the first and last elements
        actual_length_of_right_subtree = len(colours_sublist) - i - 1

        # Index_in_shades identifies the index of the first element in the left subtree. This line calculates the index
        # of the first element in the right subtree
        right_shades_index = index_in_shades + len(colours_sublist) - 1

        # Saves every tree made from each element being the root in the list
        list_of_all_roots.append([root, left_subtree, right_subtree, (actual_length_of_left_subtree, index_in_shades + i - 1), (actual_length_of_right_subtree, right_shades_index)])

    # O(n)
    # Calculates the value of each child made when each element acts as the root
    # This is done so that each tree can be compared to identify what the best root is
    # This function pulls from subtree_solutions_values which had the value of each subtree
    subtree_tree_values = []
    for i in range(len(list_of_all_roots)):
        if len(list_of_all_roots[i][1]) != 0:
            left_subtree_value = subtree_solution_values[list_of_all_roots[i][3][1]][list_of_all_roots[i][3][0] - 1]
        else:
            left_subtree_value = 0

        if len(list_of_all_roots[i][2]) != 0:
            right_subtree_value = subtree_solution_values[list_of_all_roots[i][4][1]][list_of_all_roots[i][4][0] - 1]
        else:
            right_subtree_value = 0

        subtree_tree_values.append(left_subtree_value + right_subtree_value)
    #O(n)
    # This goes through every tree and identifies the tree that has the minimum value children
    min_tree_value = inf
    index = 0
    for i in range(len(subtree_tree_values)):
        if subtree_tree_values[i] < min_tree_value:
            min_tree_value = subtree_tree_values[i]
            index = i

    # Pulls from subtree_solutions to get the value of each level of the optimal tree. Cannot use
    # subtree_solution_values as that does not contain the value of each level but the value of the entire tree
    # so the value calculation cannot be done which involves the value of each level
    if len(list_of_all_roots[index][1]) != 0:
        left_values = subtree_solutions[list_of_all_roots[index][3][1]][list_of_all_roots[index][3][0] - 1]
    else:
        left_values = []
    if len(list_of_all_roots[index][2]) != 0:
        right_values = subtree_solutions[list_of_all_roots[index][4][1]][list_of_all_roots[index][4][0] - 1]
    else:
        right_values = []

    #O(n)
    # Makes one list that combines each level into one element in temp_solution_list
    temp_solution_list = [colours_sublist, probs[index_in_shades + index]]
    # If right subtree is longer than left
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

    # O(n)
    # Does the value calculation stated in the function comments for optimal_shade_selector
    value = probs[list_of_all_roots[index][3][1]+1]
    level = 2
    for k in range(2, len(temp_solution_list)):
        value += level * temp_solution_list[k]
        level += 1
    optimal_subtree_value = value
    solution_list = temp_solution_list

    # Solution list = [[shades used to make tree], value of level 1, value of level 2...]
    # Optimal_subtree_value is the value of the entire tree
    return solution_list, optimal_subtree_value
