from requests_html import HTMLSession
import json
import insert


class Team:
    def __init__(self, name, year, competition):
        self.competition = competition
        self.name = name
        self.year = year
        self.team_data = self._fetch_team_data()
        self.players = self._fetch_player_data()

    def _parse_json(self, data):
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
        data = data.replace('\\x5B', '[')
        data = data.replace('\\x5D', ']')
        data = data.replace('\\x5C', '\\')
        data = data.replace('\\x26', '&')
        data = data.replace('\\x23', '#')
        data = data.replace('\\x3B', ';')
        data = data.replace('&#039;', "'")

        # dictionary of data
        data = json.loads(data)

        return data

    def _get_session(self):
        session = HTMLSession()
        url = 'https://understat.com/team/%s/%s' % (self.name, self.year)
        page = session.get(url)
        page.html.encoding = 'ISO-8859-1'
        page.html.render()

        return page

    def _fetch_team_data(self):
        page = self._get_session()
        # get json data for team
        divs = page.html.find('.block-content')
        team_data_script = divs[1].text.split('(')[-1][1:-3]

        data = self._parse_json(team_data_script)

        # flattening dictionary and putting correct labels
        for k, v in data.items():
            for ki, vi in v.items():
                vi['SA'] = vi['against']['shots']
                vi['GA'] = vi['against']['goals']
                vi['xGA'] = vi['against']['xG']
                del vi['against']
                vi['S'] = vi.pop('shots')
                vi['G'] = vi.pop('goals')
                if 'stat' in list(vi.keys()):
                    del vi['stat']

        return data

    def _fetch_player_data(self):
        page = self._get_session()
        # get json data for players
        divs = page.html.find('.block-content')
        player_data = divs[-1].text.split('(')[-1][1:-3]

        data = self._parse_json(player_data)
        for player in data:
            player['G'] = player.pop('goals')
            player['S'] = player.pop('shots')
            player['A'] = player.pop('assists')
            player['team'] = player.pop('team_title')
            player['name'] = player.pop('player_name')

        return data

    def insert_team_data(self):
        # changing so i can edit stuff
        data_dict = self.team_data
        for category, v in data_dict.items():
            for meta_category, vi in v.items():
                vi['category'] = category
                vi['meta_category'] = meta_category
                vi['team'] = ' '.join(self.name.split('_'))
                vi['competition'] = self.competition
                vi['season'] = self.year
                insert.insert('team_data', **vi)

    def insert_player_data(self):
        data_dict = self.players
        for player in data_dict:
            player['competition'] = self.competition
            player['season'] = self.year
            insert.insert('player_data', **player)


def get_teams(competition, year):
    session = HTMLSession()
    url = 'https://understat.com/league/%s/%s' % (competition, year)
    page = session.get(url)
    page.html.encoding = 'ISO-8859-1'
    page.html.render()

    teams = page.html.absolute_links
    teams = [link.split('/')[-2] for link in teams if 'team' in link]

    return teams


def main():
    L = 'Serie_A'
    year = '2018'
    teams = get_teams(L, year)
    f = open(L + '_updated.txt', 'r')
    updated = [x[:-1] for x in f]

    for team in teams:
        if team in updated:
            print(team + ' skipped')
            continue
        try:
            T = Team(team, year, L)
            T.insert_team_data()
            T.insert_player_data()
        except:
            print(team + ' messed up')
        print(team)
    print(L + ' all data updated')

if __name__ == '__main__':
    main()
