import sys

def expand_combination(combination, initial_to_result_map):
    return '-'.join([initial_to_result_map[initial] for initial in combination])


def get_name_initials(name):
    return ''.join([word[0] for word in name.split()]).upper()


def print_to_file_and_console(text, file_path):
    with open(file_path, 'a') as file:
        original_stdout = sys.stdout
        sys.stdout = file
        print(text)
        sys.stdout = original_stdout
        print(text)