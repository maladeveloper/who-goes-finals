def expand_combination(combination, initial_to_result_map):
    return '-'.join([initial_to_result_map[initial] for initial in combination])


def get_name_initials(name):
    return ''.join([word[0] for word in name.split()]).upper()
