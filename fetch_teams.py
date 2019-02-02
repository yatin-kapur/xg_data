from requests_html import HTMLSession
from get_session import get_session


class League:
    def __init__(self, name, year, competition):
        self.competition = competition
        self.name = name
        self.year = year
        self.league_records = self._fetch_league_records()




def get_teams(competition, year):
    page = get_session(competition + '/' + str(year))

    teams = page.html.absolute_links
    teams = [link.split('/')[-2] for link in teams if 'team' in link]

    return teams
