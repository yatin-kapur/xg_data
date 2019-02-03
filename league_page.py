from requests_html import HTMLSession
from parse_json import parse_json
from get_session import get_session
import insert


class League:
    def __init__(self, competition, year):
        self.competition = competition
        self.year = year
        self.page = get_session('league/' + competition + '/' + str(year))
        self.league_records = self._fetch_league_records()

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

    def insert_league_records(self):
        data_dict = self.league_records
        for i, team in data_dict.items():
            for md in team['history']:
                insert.insert('league_records', **md)
