import scenario_logic

"""whole bunch of boilerplate that you can try

for scenario in scenario_logic.scenarios_list_builder((2, 3, 4)):
    if scenario_logic.assert_simple_path(scenario):
        print(scenario)

print(scenario_logic.transpose_scenario(([2], [1, 2], [1, 3])))
print(scenario_logic.fill_empty_space_with_asterisk(([['G', 'B'], ['R', 'G'], ['B']])))

for something in scenario_logic.generate_possible_solutions(scenario_logic.create_all_column_permutes(
        scenario_logic.fill_empty_space_with_asterisk(([['G', 'B'], ['R', 'G'], ['B']])))):
    print(something)
print(" ")
print(scenario_logic.assert_if_actual_solution((('G', 'B'), ('R', 'G'), ('B', '*'))))
"""

scenario_logic.main((3, 3, 5))
