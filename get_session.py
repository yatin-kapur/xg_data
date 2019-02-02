from requests_html import HTMLSession


def get_session(argstring):
    session = HTMLSession()
    url = 'https://understat.com/' + argstring
    page = session.get(url)
    page.html.encoding = 'ISO-8859-1'
    page.html.render()

    return page
