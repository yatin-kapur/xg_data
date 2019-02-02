import team_page
import fetch_teams
import argparse


def main():
    parser = argparse.ArgumentParser(description='Update xG data for Leagues')
    parser.add_argument('-l', help='select league (EPL, Ligue_1, Serie_A, \
                        La_Liga, Bundesliga)', required=True)
    parser.add_argument('-s', help='select season in the format 20xx',
                        required=True)
    parser.add_argument('-t', help='select team')

    args = vars(parser.parse_args())

    year = args['s']
    L = args['l']

    # update teams in league
    if args['t'] is not None:
        teams = [args['t']]
    else:
        teams = fetch_teams.get_teams(L, year)

    for team in teams:
        print('starting ' + team)
        # if team in updated:
        #    print(team + ' skipped')
        #    continue
        try:
            T = team_page.Team(team, year, L)
            T.insert_team_data()
            print('team data done')
            T.insert_player_data()
            print('player data done')
            T.insert_match_data()
            print('match data done')
        except:
            print(team + ' messed up')
        print(team)
    print(L + ' all data updated')

if __name__ == '__main__':
    main()
