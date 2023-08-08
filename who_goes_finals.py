import argparse
import json
import os
from constants import TOTAL_ROUNDS, RESULT_TO_POINTS_MAP
from input import current_round, opponent_team, affiliated_team, league
from helpers import expand_combination, get_name_initials, print_to_file_and_console


def main(result_combinations):
    affiliated_team_initials = get_name_initials(affiliated_team["name"])
    opponent_team_initials = get_name_initials(opponent_team["name"])
    rounds_remaining = TOTAL_ROUNDS - current_round + 1
    round_combinations = result_combinations[str(rounds_remaining)]
    initial_to_result_map = {
        result[0]: result for result in RESULT_TO_POINTS_MAP.keys()
    }
    affiliated_team_wins = 0
    affiliated_team_draws = 0

    results_fp = f"output/Round-{current_round}_{league}_{affiliated_team_initials}_vs_{opponent_team_initials}.txt"
    if os.path.exists(results_fp):
        os.remove(results_fp)

    print_to_file_and_console(
        f"Who goes finals?\n\n"
        f"With {rounds_remaining} more games to go, the points for the teams are as follows:\n"
        f"{opponent_team['name']} ({opponent_team_initials}): {opponent_team['current_points']} points\n"
        f"{affiliated_team['name']} ({affiliated_team_initials}): {affiliated_team['current_points']} points\n\n"
        f"The following scenarios are possible:",
        results_fp
    )

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

            print_to_file_and_console(
                f"{opponent_team_initials} {expand_combination(opponent_combination, initial_to_result_map)} "
                f"({opponent_points} points, {opponent_total} total) and "
                f"{affiliated_team_initials} {expand_combination(chosen_combination, initial_to_result_map)} "
                f"({chosen_points} points, {chosen_total} total) "
                f"- {final_result_str}",
                results_fp
            )

    total_possible_scenarios = len(round_combinations) ** 2
    affiliated_team_losses = total_possible_scenarios - affiliated_team_wins - affiliated_team_draws
    print_to_file_and_console(
        f"\nOut of {total_possible_scenarios} total scenarios "
        f"{affiliated_team['name']} goes through to finals {affiliated_team_wins} times, "
        f"goes through on goal difference {affiliated_team_draws} times "
        f"and doesn't go finals {affiliated_team_losses} times.",
        results_fp
    )


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
