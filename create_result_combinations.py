from constants import RESULT_TO_POINTS_MAP, MAX_ROUNDS_CALCULATION
from itertools import combinations_with_replacement
import json


def main():
    results_initials = ''.join(
        [result[0] for result in RESULT_TO_POINTS_MAP.keys()]
    )
    initials_to_points_map = {
        result[0]: points for result, points in RESULT_TO_POINTS_MAP.items()
    }

    rounds_to_results = {}
    for rounds in range(MAX_ROUNDS_CALCULATION+1):
        result_combinations_generator = combinations_with_replacement(results_initials, rounds)
        result_combinations_w_points = create_combination_w_points(
            result_combinations_generator, initials_to_points_map
        )
        rounds_to_results[rounds] = result_combinations_w_points

    with open('resources/precomputed_result_combinations.json', "w") as json_file:
        json.dump(rounds_to_results, json_file, indent=4)


def create_combination_w_points(result_combination_generator, initials_to_points_map):
    result_combinations_w_points = []
    for result_combination in result_combination_generator:
        result_combinations_w_points.append(
            [result_combination, find_result_points(result_combination, initials_to_points_map)]
        )
    return result_combinations_w_points


def find_result_points(result_combination, initials_to_points_map):
    points = 0
    for result in result_combination:
        points += initials_to_points_map[result]
    return points


if __name__ == "__main__":
    main()
