import re
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select


def select_posted_date(driver, date):
    xpath = "//select[@id='dnf_class_values_procurement_notice__custom_posted_date_']"
    date_options = Select(driver.find_element_by_xpath(xpath))
    date_options.select_by_value(str(date))


def enter_zipcodes(driver, zipcodes):
    xpath = "//input[@id='dnf_class_values_procurement_notice__zipcode_']"
    zip_options = driver.find_element_by_xpath(xpath)
    if isinstance(zipcodes, (str, int)):
        zipcode_list = str(zipcodes)
    else:
        zipcode_list = [f'{zipcode},' for zipcode in zipcodes]
    for zipcode in zipcode_list:
        zip_options.send_keys(zipcode)


def select_performance_state(driver, states):
    xpath = "//select[@id='dnf_class_values_procurement_notice__zipstate___']"
    state_options = Select(driver.find_element_by_xpath(xpath))
    if isinstance(states, str):
        state_options.select_by_value(states.upper())
    else:
        for state in states:
            state_options.select_by_value(str(state).upper())


def select_document_scope(driver, document):
    scope = document.lower()
    if scope == 'active':
        xpath = "//input[@alt='Documents To Search Active Documents']"
        driver.find_element_by_xpath(xpath).click()

    if scope == 'archived':
        xpath = "//input[@alt='Documents To Search Archived Documents']"
        driver.find_element_by_xpath(xpath).click()

    if scope == 'both':
        xpath = "//input[@alt='Documents To Search Both']"
        driver.find_element_by_xpath(xpath).click()


def remove_special(text):
    return re.sub('[^A-Za-z0-9]+', '_', text).strip('_').lower()


def get_set_aside_codes(soup):
    set_aside_table = soup.find(
        'div',
        {'id': 'dnf_class_values_procurement_notice__set_aside____widget'}
    ).table
    set_aside_labels = set_aside_table.find_all('label')
    labels = [remove_special(label.string) for label in set_aside_labels]
    inputs = [x['alt'] for x in set_aside_table.find_all('input')]
    return dict(zip(labels, inputs))


def select_set_aside_codes(driver, codes):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    aside_codes = get_set_aside_codes(soup)
    if isinstance(codes, str):
        xpath = f"//input[@alt='{aside_codes[code]}']"
        driver.find_element_by_xpath(xpath).click()
    else:
        for code in codes:
            if code in aside_codes:
                xpath = f"//input[@alt='{aside_codes[code]}']"
                driver.find_element_by_xpath(xpath).click()


def submit_form(driver):
    xpath = "//input[@name='dnf_opt_submit']"
    driver.find_element_by_xpath(xpath).click()


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


