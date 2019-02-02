from parse_json import parse_json
from get_session import get_session
import insert


class Match:
    def __init__(self, id):
        self.id = id
        self.page = get_session('match/' + str(self.id))
        self.shot_data = self._fetch_shot_data()

    def _fetch_shot_data(self):
        divs = self.page.html.find('.block-content')
        sdata = divs[0].find('script')[0].text.split('(')[1].split(')')[0][1:-1]

        data = parse_json(sdata)

        return data

    def insert_shot_data(self):
        for k, team in self.shot_data.items():
            for shot in team:
                shot['last_action'] = shot.pop('lastAction')
                shot['shot_type'] = shot.pop('shotType')
                insert.insert('shot_data', **shot)
