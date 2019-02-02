from requests_html import HTMLSession
from parse_json import parse_json
from get_session import get_session
import insert


class League:
    def __init__(self, name, year, competition):
        self.competition = competition
        self.name = name
        self.year = year
        self.page = get_session('league/' + competition + '/' + str(year))
        self.league_records = self._fetch_league_records()



