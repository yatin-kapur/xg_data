from requests_html import HTMLSession

def get_teams(competition, year):
    session = HTMLSession()
    url = 'https://understat.com/league/%s/%s' % (competition, year)
    page = session.get(url)
    page.html.encoding = 'ISO-8859-1'
    page.html.render()

    teams = page.html.absolute_links
    teams = [link.split('/')[-2] for link in teams if 'team' in link]

    return teams
