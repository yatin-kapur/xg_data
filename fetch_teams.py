from requests_html import HTMLSession
from get_session import get_session


def get_teams(competition, year):
    page = get_session(competition + '/' + str(year))

    teams = page.html.absolute_links
    teams = [link.split('/')[-2] for link in teams if 'team' in link]

    return teams
