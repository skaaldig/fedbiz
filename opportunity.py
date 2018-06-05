import time
from bs4 import BeautifulSoup


def get_total_num_pages(soup):
    pages = soup.find('a', {'title': 'last page'}).contents
    max_pages = pages[0].strip('[]')
    total_pages = [str(page_num) for page_num in range(2, int(max_pages) + 1)]
    return total_pages


def get_opportunity_rows(soup):
    time.sleep(2)
    first_row = soup.find_all('tr', {'id': 'row_0'})
    even_rows = soup.find_all('tr', {'class': 'lst-rw lst-rw-even'})
    odd_rows = soup.find_all('tr', {'class': 'lst-rw lst-rw-odd'})
    rows = first_row + even_rows + odd_rows
    return rows


def parse_opportunities(soup):
    rows = get_opportunity_rows(soup)
    opportunities = []
    for row in rows:
        opp_dict = {}
        opp_dict['title'] = row.find(
            'div', {'class': 'solt'}
        ).next.strip()
        opp_dict['solicitation_number'] = row.find(
            'div', {'class': 'soln'}
        ).next.strip()
        opp_dict['code'] = row.find(
            'div', {'class': 'solcc'}
        ).next.strip()
        try:  # sometimes there are opporunities without an agency.
            opp_dict['agency'] = row.find(
                'div', {'class': 'pagency'}
            ).next.strip()
        except AttributeError:
            opp_dict['agency'] = 'None Listed'
        opp_dict['type'] = row.find(
            'td', {'headers': 'lh_base_type'}
        ).next.strip()
        opp_dict['posted'] = row.find(
            'td', {'headers': 'lh_current_posted_date'}
        ).next.strip()
        opportunities.append(opp_dict)
    return opportunities


def get_opportunities(driver):  # ugly but it works
    r = driver.page_source
    soup = BeautifulSoup(r, 'html.parser')
    opportunities = parse_opportunities(soup)
    page_numbers = get_total_num_pages(soup)
    for link in page_numbers:
        driver.find_element_by_link_text(link).click()
        r = driver.page_source
        soup = BeautifulSoup(r, 'html.parser')
        opportunities += parse_opportunities(soup)
    print(opportunities)
    return opportunities
