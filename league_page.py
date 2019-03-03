from parse_json import parse_json
from get_session import get_session
import insert


class League:
    def __init__(self, competition, year):
        self.competition = competition
        self.year = year
        self.page = get_session('league/' + competition + '/' + str(year))
        self.league_records = self._fetch_league_records()
        self.matches = self._fetch_match_data()

    def _fetch_league_records(self):
        divs = self.page.html.find('.block-content')
        league_records = divs[1].find('script')[0].text.split('(')[-1][1:-3]

        data = parse_json(league_records)
        # iterate through teams and insert matchdays
        for i, team in data.items():
            team_id = team.pop('id')
            team_title = team.pop('title')
            # get the matchday data
            matchdays = team['history']
            for i, md in enumerate(matchdays):
                md['ppda_att'] = md['ppda']['att']
                md['ppda_def'] = md['ppda']['def']
                md['ppda_allowed_att'] = md['ppda_allowed']['att']
                md['ppda_allowed_def'] = md['ppda_allowed']['def']
                del md['ppda']
                del md['ppda_allowed']
                md['id'] = team_id
                md['title'] = team_title
                md['league'] = self.competition
                md['md'] = i + 1

        return data

    def _fetch_match_data(self):
        divs = self.page.html.find('.block-content')
        mdata = divs[0].text.split('=')[1].split('(')[1].split(')')[0][1:-1]

        data = parse_json(mdata)
        # flatten with proper labels
        for match in data:
            if match['isResult']:
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

    def insert_league_records(self):
        lodicts = []
        data_dict = self.league_records
        for i, team in data_dict.items():
            for md in team['history']:
                lodicts.append(md)

        insert.insert('league_records', lodicts)

    def insert_match_data(self):
        lodicts = []
        data_dict = self.matches
        for match in data_dict:
            if match['isResult']:
                del match['isResult']
                match['competition'] = self.competition
                match['season'] = self.year
                lodicts.append(match)

        insert.insert('match_data', lodicts)
