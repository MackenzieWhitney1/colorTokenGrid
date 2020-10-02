from itertools import product, permutations

""" generate every partition for a number.
full credit goes to http://jeromekelleher.net/generating-integer-partitions.html"""


def accel_asc(n):
    a = [0 for i in range(n + 1)]
    k = 1
    y = n - 1
    while k != 0:
        x = a[k - 1] + 1
        k -= 1
        while 2 * x <= y:
            a[k] = x
            y -= x
            k += 1
        l = k + 1
        while x <= y:
            a[k] = x
            a[l] = y
            yield a[:k + 2]
            x += 1
            y -= 1
        a[k] = x + y
        y = x + y - 1
        yield a[:k + 1]


# if we ever have a partition for a color with a repeated number, this contradicts vertical non-duplicate rule
def duplicate_element_checker(tuple):
    for i in tuple:
        if tuple.count(i) > 1:
            return False
        else:
            if i == tuple[-1]:
                return True


# apply duplicate check to set of all partitions for a number
def partition_set_for_number(n):
    set = []
    for tuple in accel_asc(n):
        if duplicate_element_checker(tuple):
            set.append(tuple)
    return set


# for a set like (2,3,4), replace each number with the set of all its non-duplicate partitions
def permutations_list_builder(set_of_tokens):
    permutations_list = []
    for num in set_of_tokens:
        permutations_list.append(partition_set_for_number(num))
    return permutations_list


# take the cartesian product for partitions of colors to get scenarios
def scenarios_list_builder(number_of_colored_tokens):
    return product(*permutations_list_builder(number_of_colored_tokens))


# method to drop the brackets for asserting simple paths
def collapse_scenario(scenario):
    collapsed_scenario = []
    for partition in scenario:
        for element in partition:
            collapsed_scenario.append(element)
    return collapsed_scenario


# partial sum is s(n) = 1 + 2 + ... + n = n(n+1)/2. a full board has at most s(n) of any one color
def number_of_tokens_less_than_partial_sum(set_of_tokens):
    n = len(set_of_tokens)
    s = (n*(n+1))/2
    for num_tokens in set_of_tokens:
        if num_tokens > s:
            return False
    return True


# cares only about numbers, not colors of tokens. ie. can one complete 1-i chains with no holes.
def assert_simple_path(scenario):
    collapsed_scenario = collapse_scenario(scenario)
    while collapsed_scenario:
        max_num = max(collapsed_scenario)
        i = 1
        while i <= max_num:
            if i in collapsed_scenario:
                collapsed_scenario.remove(i)
            else:
                return False
            i += 1
    return True


"""transpose scenarios like ([2], [1, 2], [1, 3]) to ([G, B], [R, G], [B])
                            R      G       B           1       2      3"""


# name of definition pending.
def transpose_scenario(scenario):
    # arbitrary mapping. colors could stay as numbers but makes visualization difficult
    color_letter_map = {0: 'R',
                        1: 'G',
                        2: 'B',
                        3: 'Y',
                        4: 'O'}
    maximum_number = max(collapse_scenario(scenario))
    transposed_scenario = [[] for x in range(maximum_number)]
    """ look at the content of each set in the set of sets.
    based on the content of the set, place a character in the indexed spot.
    ex. if the set [2] is at the 0th/R position, put an R in the "2" set (whose index is 1)"""
    i = 0
    while i < len(scenario):
        # for clarity, scenario[i] is a group represented by color that contains numbers. ex. "R"
        color_character = color_letter_map.get(i)
        for color_num in scenario[i]:
            # it's color_num-1. ex. the set containing colors of exactly 1 token is at set indexed by 0.
            transposed_scenario[color_num-1].append(str(color_character))
        i += 1
    return transposed_scenario


""" take the height of the transposed scenario and fill the empty space with *
this is to allow permutes of columns where permuting empty space is needed.
example: ([G, B], [R, G], [B]) to ([G, B], [R, G], [B, *])"""


def fill_empty_space_with_asterisk(transposed_scenario):
    max_height = 0
    for column in transposed_scenario:
        if len(column) > max_height:
            max_height = len(column)
    for column in transposed_scenario:
        while len(column) < max_height:
            column.append('*')
    return transposed_scenario


def create_all_column_permutes(transposed_scenario):
    column_permutes_of_each_column = []
    for column in transposed_scenario:
        column_perms = set(permutations(column))
        column_permutes_of_each_column.append(column_perms)
    return column_permutes_of_each_column


def generate_possible_solutions(all_column_permutes):
    return product(*all_column_permutes)


def return_an_actual_solution_if_any(possible_solutions):
    for possible_solution in possible_solutions:
        if assert_if_actual_solution(possible_solution):
            return possible_solution


def assert_if_actual_solution(possible_solution):
    row_number = 0
    max_rows = len(possible_solution[0])
    # print("There are "+str(max_rows)+" rows.")
    max_columns = len(possible_solution)
    # print("There are "+str(max_columns)+" columns.")
    while row_number < max_rows:
        # print("On row "+str(row_number))
        set_of_chars_that_cant_be_repeated = []
        column_number = 0
        while column_number < max_columns:
            # print("On column "+str(column_number))
            # print(possible_solution[column_number][row_number])
            if column_number >= 1:
                if possible_solution[column_number][row_number] != '*' and possible_solution[column_number-1][row_number] == '*':
                    return False
            if possible_solution[column_number][row_number] in set_of_chars_that_cant_be_repeated:
                return False
            else:
                set_of_chars_that_cant_be_repeated.append(possible_solution[column_number][row_number])
                column_number += 1
        row_number += 1
    return True


def main(set_of_tokens):
    if len(set_of_tokens) > 5:
        print("Only number of colors <= 5 is currently supported")
        return False
    if not number_of_tokens_less_than_partial_sum(set_of_tokens):
        print("At least one color has number of tokens greater than what can fit in a complete grid")
        return False
    scenarios_created_by_list_builder = []
    for scenario in scenarios_list_builder(set_of_tokens):
        if assert_simple_path(scenario):
            scenarios_created_by_list_builder.append(scenario)
            
    for scenario in scenarios_created_by_list_builder:
        transposed_scenario = transpose_scenario(scenario)
        filled_transposed_scenario = fill_empty_space_with_asterisk(transposed_scenario)
        all_column_permutes = create_all_column_permutes(filled_transposed_scenario)
        possible_solutions = generate_possible_solutions(all_column_permutes)
        actual_solution = return_an_actual_solution_if_any(possible_solutions)
        if actual_solution is not None:
            print(actual_solution)
