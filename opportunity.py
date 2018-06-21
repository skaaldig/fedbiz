import time
from bs4 import BeautifulSoup


def get_opportunity_rows(soup):
    # Sleep used to avoid bot detection.
    time.sleep(2)
    first_row = soup.find_all('tr', {'id': 'row_0'})
    even_rows = soup.find_all('tr', {'class': 'lst-rw lst-rw-even'})
    odd_rows = soup.find_all('tr', {'class': 'lst-rw lst-rw-odd'})
    rows = first_row + even_rows + odd_rows
    return rows


def rows_to_dictionary(soup):
    rows = get_opportunity_rows(soup)
    opportunities = []

    for row in rows:
        page_opportunities = {}
        page_opportunities['title'] = row.find(
            'div', {'class': 'solt'}
        ).next.strip()
        page_opportunities['solicitation_number'] = row.find(
            'div', {'class': 'soln'}
        ).next.strip()
        page_opportunities['code'] = row.find(
            'div', {'class': 'solcc'}
        ).next.strip()

        try:  # sometimes there are opporunities without an agency.
            page_opportunities['agency'] = row.find(
                'div', {'class': 'pagency'}
            ).next.strip()
        except AttributeError:
            page_opportunities['agency'] = 'None Listed'

        page_opportunities['type'] = row.find(
            'td', {'headers': 'lh_base_type'}
        ).next.strip()
        page_opportunities['posted'] = row.find(
            'td', {'headers': 'lh_current_posted_date'}
        ).next.strip()
        opportunities.append(page_opportunities)

    return opportunities


def get_total_num_pages(soup): # needs re-evaluation 

    try:
        pages = soup.find('a', {'title': 'last page'}).contents
        max_pages = pages[0].strip('[]')
        total_pages = [str(page_num) for page_num in range(2, int(max_pages) + 1)]
        return total_pages
    except AttributeError:
        next_page = soup.find('a', {'title': 'next page'})
        last_page = next_page.find_previous_sibling('a').contents
        max_pages = last_page[0].strip('[]')
        total_pages = [str(page_num) for page_num in range(2, int(max_pages) + 1)]
        return total_pages
    except AttributeError:
        return False


def get_opportunities(driver):
    r = driver.page_source
    soup = BeautifulSoup(r, 'html.parser')
    opportunities = rows_to_dictionary(soup)

    if get_total_num_pages(soup):
        page_numbers = get_total_num_pages(soup)
        for link in page_numbers:
            driver.find_element_by_link_text(link).click()
            r = driver.page_source
            soup = BeautifulSoup(r, 'html.parser')
            opportunities += rows_to_dictionary(soup)
    print(opportunities)
    return opportunities
