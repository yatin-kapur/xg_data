from requests_html import HTMLSession


session = HTMLSession()
url = 'https://www.whoscored.com/Players/5583/history/'
r = session.get(url)
r.html.encoding = 'ISO-8859-1'
r.html.render()

tournaments = r.html.find('.rank.tournament')
goals = r.html.find('.goal')[1:]
print(len(tournaments))

for i in range(0, len(tournaments)):
    print(tournaments[i].text, goals[i].text)
