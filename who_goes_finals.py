import argparse
import json
from constants import TOTAL_ROUNDS, RESULT_TO_POINTS_MAP
from input import current_round, opponent_team, affiliated_team


def main(result_combinations):
    affiliated_team_initials = get_name_initials(affiliated_team["name"])
    opponent_team_initials = get_name_initials(opponent_team["name"])
    rounds_remaining = TOTAL_ROUNDS - current_round + 1
    round_combinations = result_combinations[str(rounds_remaining)]

    initial_to_result_map = {}

    def expand_result_initial(initial):
        try:
            return initial_to_result_map[initial]
        except KeyError:
            for result in RESULT_TO_POINTS_MAP.keys():
                if initial == result[0]:
                    initial_to_result_map[initial] = result
            return initial_to_result_map[initial]

    def expand_combination(combination):
        return '-'.join([expand_result_initial(initial) for initial in combination])

    affiliated_team_wins = 0
    affiliated_team_draws = 0
    for opponent_team_result in round_combinations:
        for affiliated_team_result in round_combinations:
            opponent_combination, opponent_points = opponent_team_result
            chosen_combination, chosen_points = affiliated_team_result
            opponent_total = opponent_team['current_points'] + opponent_points
            chosen_total = affiliated_team['current_points'] + chosen_points

            if chosen_total > opponent_total:
                final_result_str = f"{affiliated_team_initials} WINS."
                affiliated_team_wins += 1
            elif chosen_total < opponent_total:
                final_result_str = f"{opponent_team_initials} WINS."
            else:
                final_result_str = f"{opponent_team_initials} and {affiliated_team_initials} DRAW."
                affiliated_team_draws += 1

            print(
                f"{opponent_team_initials} {expand_combination(opponent_combination)} ({opponent_points} points, "
                f"{opponent_total} total) and "
                f"{affiliated_team_initials} {expand_combination(chosen_combination)} ({chosen_points} points, "
                f"{chosen_total} total) "
                f"{final_result_str}"
            )

    total_possible_scenarios = len(round_combinations) ** 2
    affiliated_team_losses = total_possible_scenarios - affiliated_team_wins - affiliated_team_draws
    print(
        f"\nOut of {total_possible_scenarios} total scenarios "
        f"{affiliated_team['name']} wins {affiliated_team_wins}, "
        f"draws {affiliated_team_draws} ",
        f"and loses {affiliated_team_losses}."
    )


def get_name_initials(name):
    return ''.join([word[0] for word in name.split()]).upper()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--file-path', type=str, help='Path to JSON file with precomputed result combinations.'
    )
    args = parser.parse_args()

    file_path = args.file_path

    if file_path is None:
        print('Please provide argument --file-path and try again.')
        exit(1)

    try:
        with open(file_path, 'r') as file:
            result_combinations = json.load(file)
    except FileNotFoundError:
        print('Path provided for --file-path does not exist.')
        exit(1)

    main(result_combinations)
