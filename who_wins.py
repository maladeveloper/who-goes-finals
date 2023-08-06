current_round = 15
teams = [
    {
        "name": "Greater Dandenong Warriors Hockey Club",
        "current_points": 20
    },
    {
        "name": "Monash University Hockey Club",
        "current_points": 24
    }
]
chosen_team_name = "Monash University Hockey Club"


def main():
    chosen_team, opposing_teams = filter_chosen_team(chosen_team_name, teams)
    for opponent_team in opposing_teams:
        calculate_scenarios(chosen_team, opponent_team, current_round)


def filter_chosen_team(chosen_team_name, teams):
    try:
        chosen_team = list(filter(lambda x: x["name"] == chosen_team_name, teams)).pop()
        opposing_teams = list(filter(lambda x: x["name"] != chosen_team_name, teams))
        return chosen_team, opposing_teams
    except IndexError:
        team_list = ",\n".join([team["name"] for team in teams])
        print(
            f"Chosen team '{chosen_team_name}' is not a valid team.\n"
            f"Check spelling or choose another team from the following:\n{team_list}"
        )
        exit(1)


def calculate_scenarios(chosen_team, opponent_team, current_round):
    rounds_remaining = TOTAL_ROUNDS - current_round + 1
    chosen_team_initals = get_name_initials(chosen_team["name"])
    opponent_team_initals = get_name_initials(opponent_team["name"])


def get_name_initials(name):
    return ''.join([word[0] for word in name.split()]).upper()


if __name__ == "__main__":
    main()
