from parse_json import parse_json
from get_session import get_session
import insert


class Match:
    def __init__(self, id):
        self.id = id
        self.page = get_session('match/' + str(self.id))
        self.match_info = self._fetch_match_info()
        self.shot_data = self._fetch_shot_data()
        self.rosters = self._fetch_rosters()

    def _fetch_match_info(self):
        divs = self.page.html.find('.block-content')
        mi = divs[0].find('script')[0].text.split('(')[2].split(')')[0][1:-1]

        data = parse_json(mi)
        data.

        return data

    def _fetch_shot_data(self):
        divs = self.page.html.find('.block-content')
        sdata = divs[0].find('script')[0].text.split('(')[1].split(')')[0][1:-1]

        data = parse_json(sdata)
        translate = {'EPL': 'EPL',
                     'La liga': 'La_Liga',
                     'Bundesliga': 'Bundesliga',
                     'Serie A': 'Serie_A',
                     'Ligue 1': 'Ligue_1'}
        data['league'] = translate[data['league']]

        return data

    def _fetch_rosters(self):
        divs = self.page.html.find('.block-content')
        rosters = divs[1].find('script')[0].text.split('(')[1].split(')')[0][1:-1]

        data = parse_json(rosters)

        return data

    def insert_match_info(self):
        lodicts = [self.match_info]
        insert.insert('match_info', lodicts)

    def insert_rosters(self):
        lodicts = []
        for k, team in self.rosters.items():
            for j, player in team.items():
                player['competition'] = self.match_info['league']
                player['season'] = self.match_info['season']
                player['position_order'] = player.pop('positionOrder')
                lodicts.append(player)

        insert.insert('roster_data', lodicts)

    def insert_shot_data(self):
        lodicts = []
        for k, team in self.shot_data.items():
            for shot in team:
                shot['last_action'] = shot.pop('lastAction')
                shot['shot_type'] = shot.pop('shotType')
                shot['team'] = shot['h_team'] if shot['h_a'] == 'h' else \
                    shot['a_team']
                shot['competition'] = self.match_info['league']
                lodicts.append(shot)

        insert.insert('shot_data', lodicts)
