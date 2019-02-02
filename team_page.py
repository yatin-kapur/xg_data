from parse_json import parse_json
from get_session import get_session
import insert


class Team:
    def __init__(self, name, year, competition):
        self.competition = competition
        self.name = name
        self.year = year
        self.page = get_session('team/' + team + '/' + str(year))
        self.team_data = self._fetch_team_data()
        self.players = self._fetch_player_data()
        self.matches = self._fetch_match_data()

    def _fetch_team_data(self):
        # get json data for team
        divs = self.page.html.find('.block-content')
        team_data_script = divs[1].text.split('(')[-1][1:-3]

        data = parse_json(team_data_script)

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
        divs = self.page.html.find('.block-content')
        player_data = divs[-1].text.split('(')[-1][1:-3]

        data = parse_json(player_data)
        for player in data:
            player['G'] = player.pop('goals')
            player['S'] = player.pop('shots')
            player['A'] = player.pop('assists')
            player['team'] = player.pop('team_title')
            player['name'] = player.pop('player_name')

        return data

    def _fetch_match_data(self):
        divs = self.page.html.find('.block-content')
        match_data = divs[0].text.split('(')[-1][1:-3]

        data = parse_json(match_data)
        # flatten with proper labels
        for match in data:
            if not match['isResult']:
                break
            match['forecast_w'] = match['forecast']['w']
            match['forecast_d'] = match['forecast']['d']
            match['forecast_l'] = match['forecast']['l']
            del match['forecast']
            match['h_goals'] = match['goals']['h']
            match['a_goals'] = match['goals']['a']
            del match['goals']
            match['h_xg'] = match['xG']['h']
            match['a_xg'] = match['xG']['a']
            del match['xG']
            match['h_id'] = match['h']['id']
            match['a_id'] = match['a']['id']
            match['h_title'] = match['h']['title']
            match['a_title'] = match['a']['title']
            del match['h']
            del match['a']

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

    def insert_match_data(self):
        data_dict = self.matches
        for match in data_dict:
            if not match['isResult']:
                break
            del match['isResult']
            match['competition'] = self.competition
            match['season'] = self.year
            insert.insert('match_data', **match)
