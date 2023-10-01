import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

def check_un_link(url):
    # Checks if a link is a press release and contains the word "crisis"
    response = urllib.request.urlopen(url)
    soup = BeautifulSoup(response, features="lxml")
    press_release_link = soup.find('a', href=True, hreflang='en', string="Press Release")
    if press_release_link:
        title = soup.find('div', class_="field field--name-field-display-title field--type-string field--label-hidden field__item").text.strip()
        content = soup.find('div', class_="field field--name-body field--type-text-with-summary field--label-hidden field__item").text.strip()
        if "crisis" in title or "crisis" in content:
            return title, content
    return None

def get_un_press_releases():
    # Goes through 3 layers of links from the seed url to collect press releases
    seed_url = "https://press.un.org/en"
    press_releases = {}

    response = urllib.request.urlopen(seed_url)
    soup = BeautifulSoup(response, features="lxml")
    home_page_links = set([link['href'] for link in soup.find_all('a', href=True) if link['href'].startswith('/en')])
    for home_link in home_page_links:
        page_url = urllib.parse.urljoin(seed_url, home_link)
        res = check_un_link(page_url)
        if res and res[0] not in press_releases.keys():
            press_releases[res[0]] = res[1]
        if len(press_releases) >= 10:
            return press_releases
        
        response = urllib.request.urlopen(page_url)
        soup = BeautifulSoup(response, features="lxml")
        page_links = set([link['href'] for link in soup.find_all('a', href=True) if link['href'].startswith('/en')])
        for page_link in page_links:
            subpage_url = urllib.parse.urljoin(seed_url, page_link)
            res = check_un_link(subpage_url)
            if res and res[0] not in press_releases.keys():
                press_releases[res[0]] = res[1]
            if len(press_releases) >= 10:
                return press_releases
            
            response = urllib.request.urlopen(subpage_url)
            soup = BeautifulSoup(response, features="lxml")
            subpage_links = set([link['href'] for link in soup.find_all('a', href=True) if link['href'].startswith('/en')])
            for subpage_link in subpage_links:
                subsubpage_url = urllib.parse.urljoin(seed_url, subpage_link)
                res = check_un_link(subsubpage_url)
                if res and res[0] not in press_releases.keys():
                    press_releases[res[0]] = res[1]
    return press_releases


if __name__ == "__main__":
    result = get_un_press_releases()
    print(result)