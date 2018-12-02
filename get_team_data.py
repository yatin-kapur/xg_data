from requests_html import HTMLSession
import pandas as pd
import json

league_data_gs = {}
league_data_xg = {}


def get_data(team, year):
    session = HTMLSession()
#    team = 'Manchester City'
#    team = '_'.join(team.split(' '))
#    year = '2018'
    url = 'https://understat.com/team/%s/%s' % (team, year)
    r = session.get(url)
    r.html.encoding = 'ISO-8859-1'
    r.html.render()

    # get JSON data for gamestate data
    script = r.html.find('script')[3].text
    data = script.split('(')[-1][1:-3]

    # replace all hex codes with ascii
    data = data.replace('\\x7B', '{')
    data = data.replace('\\x7D', '}')
    data = data.replace('\\x3A', ':')
    data = data.replace('\\x22', '"')
    data = data.replace('\\x20', ' ')
    data = data.replace('\\x2B', '+')
    data = data.replace('\\x2D', '-')
    data = data.replace('\\x3C', '<')
    data = data.replace('\\x3E', '>')

    # dictionary of data
    data = json.loads(data)

    return data


def retrieve_game_states(data, team):
    game_states = data['gameState']

    # make data frame
    for k, v in game_states.items():
        del v['stat']
        v['SA'] = v['against']['shots']
        v['GA'] = v['against']['goals']
        v['xGA'] = v['against']['xG']
        del v['against']
        v['S'] = v.pop('shots')
        v['G'] = v.pop('goals')

    # revise data keys
    for state in ['Goal diff 0', 'Goal diff +1', 'Goal diff -1',
                  'Goal diff < -1', 'Goal diff > +1']:
        score = state.split(' ')[-1]
        if '<' in state:
            score = '<' + score
        if '>' in state:
            score = '>' + score

        if state in game_states.keys():
            game_states[score] = game_states.pop(state)
        else:
            game_states[score] = {'S': 0, 'G': 0, 'xG': 0, 'SA': 0, 'GA': 0,
                                  'time': 0, 'xGA': 0}

    # create data frame and add more assimilated data
    game_states = pd.DataFrame(game_states)
    game_states['losing'] = game_states['-1'] + game_states['<-1']
    game_states['winning'] = game_states['+1'] + game_states['>+1']
    game_states = game_states.transpose()

    for x in game_states.columns:
        if x != 'time':
            game_states[x + '90'] = (game_states[x]*90/game_states['time'])

    game_states['xGD'] = game_states['xG'] - game_states['xGA']
    league_data_gs[team] = game_states


def retrieve_xg(data, team):
    xg_data = data['situation']

    # make data frame
    for k, v in xg_data.items():
        v['SA'] = v['against']['shots']
        v['GA'] = v['against']['goals']
        v['xGA'] = v['against']['xG']
        del v['against']
        v['S'] = v.pop('shots')
        v['G'] = v.pop('goals')


    xg_data = pd.DataFrame(xg_data).transpose()
    xg_data['xGD'] = xg_data['xG'] - xg_data['xGA']
    league_data_xg[team] = xg_data


def write_data(teams):
    writer = pd.ExcelWriter('epl2018_game_states.xlsx')
    for team in teams:
        league_data_gs[team].to_excel(writer, team + '_gameState')
        league_data_xg[team].to_excel(writer, team + '_xG')
    writer.save()


# get teams
session = HTMLSession()
url = 'https://understat.com/league/EPL'
r = session.get(url)
r.html.encoding = 'ISO-8859-1'
r.html.render()

teams = r.html.absolute_links
teams = [link.split('/')[-2] for link in teams if 'team' in link]
team_data = {}
for p in teams:
    team_data[p] = get_data(p, '2018')
    retrieve_xg(team_data[p], p)
    retrieve_game_states(team_data[p], p)


write_data(teams)
