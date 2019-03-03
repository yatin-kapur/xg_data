from parse_json import parse_json
from get_session import get_session
import insert


class Team:
    def __init__(self, name, year, competition):
        self.competition = competition
        self.name = name
        self.year = year
        self.page = get_session('team/' + self.name + '/' + str(self.year))
        self.team_data = self._fetch_team_data()
        self.players = self._fetch_player_data()

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

    def insert_team_data(self):
        # changing so i can edit stuff
        data_dict = self.team_data
        for category, v in data_dict.items():
            lodicts = []
            for meta_category, vi in v.items():
                vi['category'] = category
                vi['meta_category'] = meta_category
                vi['team'] = ' '.join(self.name.split('_'))
                vi['competition'] = self.competition
                vi['season'] = self.year
                lodicts.append(vi)
            insert.insert('team_data', lodicts)

    def insert_player_data(self):
        lodicts = []
        data_dict = self.players
        for player in data_dict:
            player['competition'] = self.competition
            player['season'] = self.year
            lodicts.append(player)

        insert.insert('player_data', lodicts)
