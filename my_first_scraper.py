import requests
from bs4 import BeautifulSoup

def request_github_trending(url):
    return requests.get(url)


def extract(page):
    stew = BeautifulSoup(page.text, "html.parser")
    return stew.find_all("article")

def transform(html_repos):
    jorabek = []

    for r in html_repos:
        repository = ''.join(r.select_one('h1.h3.lh-condensed').text.split())
        stars = ' '.join(r.select_one("span.d-inline-block.float-sm-right").text.split())
        try:
            NAME = r.select_one('img.avatar.mb-1.avatar-user')['alt']
        except:
            NAME = 'hidden_name'
        jorabek.append({'developer': NAME , 'repository': repository, 'nbr_stars': stars})
         
    return jorabek

def format(repositories_data):
    jorabek = ["Developer, Repository Name, Number of Stars"]

    for repo in repositories_data:
        r = [repo['developer'], repo['repository'], repo['nbr_stars']]
        jorabek.append(', '.join(r))

    return "\n".join(jorabek)


def _main():
    url ="https://github.com/trending"
    page = request_github_trending(url)
    html_repos = extract(page)
    repositories_data = transform(html_repos)
    print(format(repositories_data))
    
_main()