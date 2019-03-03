from match_page import Match
from team_page import Team
from league_page import League
from fetch_teams import get_teams
from fetch_matches import get_match_ids
import argparse
from termcolor import colored


def main():
    parser = argparse.ArgumentParser(description='Update xG data for Leagues')
    parser.add_argument('-l', help='select league (EPL, Ligue_1, Serie_A, \
                        La_Liga, Bundesliga)')
    parser.add_argument('--skip-league', help="don't update league data, just \
                        teams", action='store_true')
    parser.add_argument('-s', help='select season in the format 20xx')
    parser.add_argument('-t', help='specify which team to update')
    parser.add_argument('--all', help='use this flag to use all teams',
                        action='store_true')
    parser.add_argument('--none', help='use this flag to update no team',
                        action='store_true')
    parser.add_argument('-m', help='enter match id to update match')
    parser.add_argument('--all-shots', help='update all the shots from \
                        matches in match_data table that are not in shots \
                        table already', action='store_true')

    # parse arguments
    args = vars(parser.parse_args())
    print(args)

    year = args['s']
    competition = args['l']
    teams_arg = args['t']
    match = args['m']

    # for matchids updating if competition is None
    query_comp = "('EPL', 'La_Liga', 'Serie_A', 'Bundesliga', 'Ligue_1')"

    # update league positions data
    if competition is not None:
        # for matchids updating if need be
        query_comp = "('" + competition + "')"

        # start league updating jobs via object
        if args['skip_league'] is False:
            print(colored('starting', 'yellow'), colored(competition, 'blue'))
            L = League(competition, year)
            L.insert_league_records()
            print(colored(competition, 'blue'),
                  colored('league records updated', 'green'))

    # update teams in league
    teams = []
    if args['all']:
        teams = get_teams(competition, year)
    elif args['none']:
        teams = []
    else:
        # specified team
        teams = [teams_arg] if teams_arg is not None else []

    # update teams selected
    for team in teams:
        try:
            print(colored('starting', 'yellow'), colored(team, 'white'))
            T = Team(team, year, competition)
            T.insert_team_data()
            print(colored('team data done', 'magenta'))
            T.insert_player_data()
            print(colored('player data done', 'cyan'))
        except Exception as e:
            print(e)
            print(colored(team, 'white'), colored('messed up', 'red'))
        print(colored(team, 'white'), colored('updated', 'green'))

    # match updating
    matches = []
    if args['all_shots']:
        matches = get_match_ids(query_comp, year)
    else:
        matches = [args['m']]

    # update matches
    for match in matches:
        if match is None:
            break

        try:
            print(colored('starting', 'yellow'), colored(match, 'white'))
            M = Match(match)
            M.insert_shot_data()
            M.insert_rosters()
            print(colored('shot data done', 'magenta'))
        except Exception as e:
            print(e)
            print(colored(match, 'white'), colored('messed up', 'red'))
        print(colored(match, 'white'), colored('updated', 'green'))


if __name__ == '__main__':
    main()
