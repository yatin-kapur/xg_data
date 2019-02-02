from team_page import Team
from league_page import League
from fetch_teams import get_teams
import argparse


def main():
    parser = argparse.ArgumentParser(description='Update xG data for Leagues')
    parser.add_argument('-l', help='select league (EPL, Ligue_1, Serie_A, \
                        La_Liga, Bundesliga)', required=True)
    parser.add_argument('-s', help='select season in the format 20xx',
                        required=True)
    parser.add_argument('-t', help='type team name; "all" to update all \
                        teams; "none" to only update league', required=True)

    # parse arguments
    args = vars(parser.parse_args())
    year = args['s']
    competition = args['l']
    teams_arg = args['t']

    # update league positions data
    L = League(competition, year)
    L.insert_league_records()
    print(competition + ' league records updated')

    # update teams in league
    if teams_arg == 'all':
        teams = get_teams(competition, year)
    elif teams_arg == 'none':
        teams = []
    else:
        # specified team
        teams = teams_arg

    # update teams selected
    for team in teams:
        print('starting ' + team)
        try:
            T = Team(team, year, L)
            T.insert_team_data()
            print('team data done')
            T.insert_player_data()
            print('player data done')
            T.insert_match_data()
            print('match data done')
        except:
            print(team + ' messed up')
        print(team + ' updated')

if __name__ == '__main__':
    main()
