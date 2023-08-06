import argparse
import json
from constants import TOTAL_ROUNDS, RESULT_TO_POINTS_MAP
current_round = 16
teams = [
    {
        "name": "Greater Dandenong Warriors Hockey Club",
        "current_points": 23
    },
    {
        "name": "Monash University Hockey Club",
        "current_points": 27
    }
]
chosen_team_name = "Monash University Hockey Club"


def main(result_combinations):
    chosen_team, opposing_teams = filter_chosen_team(chosen_team_name, teams)
    for opponent_team in opposing_teams:
        calculate_scenarios(chosen_team, opponent_team, current_round, result_combinations)


def filter_chosen_team(chosen_team_name, teams):
    try:
        chosen_team = list(filter(lambda x: x["name"] == chosen_team_name, teams)).pop()
        opposing_teams = list(filter(lambda x: x["name"] != chosen_team_name, teams))
        return chosen_team, opposing_teams
    except IndexError:
        team_list = ",\n".join([team["name"] for team in teams])
        print(
            f"Chosen team '{chosen_team_name}' is not a valid team.\n"
            f"Check spelling or choose another team from the following:\n{team_list} "
        )
        exit(1)


def calculate_scenarios(chosen_team, opponent_team, current_round, result_combinations):
    chosen_team_initals = get_name_initials(chosen_team["name"])
    opponent_team_initals = get_name_initials(opponent_team["name"])
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

    chosen_team_wins = 0
    chosen_team_draws = 0
    for opponent_team_result in round_combinations:
        for chosen_team_result in round_combinations:
            opponent_combination, opponent_points = opponent_team_result
            chosen_combination, chosen_points = chosen_team_result
            opponent_total = opponent_team['current_points'] + opponent_points
            chosen_total = chosen_team['current_points'] + chosen_points

            if chosen_total > opponent_total:
                final_result_str = f"{chosen_team_initals} WINS."
                chosen_team_wins += 1
            elif chosen_total < opponent_total:
                final_result_str = f"{opponent_team_initals} WINS."
            else:
                final_result_str = f"{opponent_team_initals} and {chosen_team_initals} DRAW."
                chosen_team_draws += 1

            print(
                f"{opponent_team_initals} {expand_combination(opponent_combination)} ({opponent_points} points, "
                f"{opponent_total} total) and "
                f"{chosen_team_initals} {expand_combination(chosen_combination)} ({chosen_points} points, "
                f"{chosen_total} total) "
                f"{final_result_str}"
            )

    total_possible_scenarios = len(round_combinations)** 2
    chosen_team_losses = total_possible_scenarios - chosen_team_wins - chosen_team_draws
    print(
        f"\nOut of {total_possible_scenarios} total scenarios "
        f"{chosen_team['name']} wins {chosen_team_wins}, draws {chosen_team_draws} and loses {chosen_team_losses}."
          )


def get_name_initials(name):
    return ''.join([word[0] for word in name.split()]).upper()



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file-path', type=str, help='Path to JSON file with precomputed result combinations.')
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
