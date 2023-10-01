import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

def check_eu_link(url):
    # Checks if a link is a plenary session and contains the word "crisis"
    try:
        response = urllib.request.urlopen(url)
    except:
        return None
    soup = BeautifulSoup(response, features="lxml")
    plenary_session = soup.find("span", "ep_name", string="Plenary session")
    if plenary_session:
        title = soup.find('h1', class_="ep_title")
        if title:
            title = title.text.strip()
            content = []
            facts = soup.find('div', class_="ep-a_facts")
            if facts:
                content.append(facts.text.strip())
            div_tags = soup.find_all('div', class_="ep-a_text")
            for div_tag in div_tags:
                p_tags = div_tag.find_all('p')
                p_texts = [p.text.strip() for p in p_tags]
                content.extend(p_texts)
            content = " ".join(content)
            if "crisis" in title or "crisis" in content:
                print(url)
                return title, content
    return None

def get_eu_plenary_sessions():
    # Goes through 3 layers of links from the seed url to collect press releases
    seed_url = "https://www.europarl.europa.eu/news/en/press-room"
    plenary_sessions = {}

    response = urllib.request.urlopen(seed_url)
    soup = BeautifulSoup(response, features="lxml")
    home_page_links = set([link['href'] for link in soup.find_all('a', href=True) if link['href'].startswith(seed_url)])
    for home_link in home_page_links:
        page_url = urllib.parse.urljoin(seed_url, home_link)
        res = check_eu_link(page_url)
        if res and res[0] not in plenary_sessions.keys():
            plenary_sessions[res[0]] = res[1]
        if len(plenary_sessions) >= 10:
            return plenary_sessions
        
        response = urllib.request.urlopen(page_url)
        soup = BeautifulSoup(response, features="lxml")
        page_links = set([link['href'] for link in soup.find_all('a', href=True) if link['href'].startswith(seed_url)])
        for page_link in page_links:
            subpage_url = urllib.parse.urljoin(seed_url, page_link)
            res = check_eu_link(subpage_url)
            if res and res[0] not in plenary_sessions.keys():
                plenary_sessions[res[0]] = res[1]
            if len(plenary_sessions) >= 10:
                return plenary_sessions
            
            response = urllib.request.urlopen(subpage_url)
            soup = BeautifulSoup(response, features="lxml")
            subpage_links = set([link['href'] for link in soup.find_all('a', href=True) if link['href'].startswith(seed_url)])
            for subpage_link in subpage_links:
                subsubpage_url = urllib.parse.urljoin(seed_url, subpage_link)
                res = check_eu_link(subsubpage_url)
                if res and res[0] not in plenary_sessions.keys():
                    plenary_sessions[res[0]] = res[1]
    return plenary_sessions


if __name__ == "__main__":
    result = get_eu_plenary_sessions()
    print(result)