import pandas as pd
from datetime import datetime
from selenium import webdriver
from search import select_posted_date
from search import enter_zipcodes
from search import select_performance_state
from search import select_document_scope
from search import submit_form
from search import select_codes
from search import enter_date_ranges
from search import toggle_recovery_reinvestment_act
from opportunity import get_opportunities


class FedBizOpps:

    def __init__(self,
                 posted=None,
                 zipcodes=None,
                 states=None,
                 scope=None,
                 set_aside=None,
                 naics_codes=None,
                 class_codes=None,
                 ja_codes=None,
                 recovery_and_reinvestment=False,
                 fair_opportunity_codes=None,
                 posted_range_start=None,
                 posted_range_end=None,
                 response_date_start=None,
                 response_date_end=None,
                 last_modified_start=None,
                 last_modified_end=None,
                 award_date_start=None,
                 award_date_end=None):

        self.posted = posted
        self.zipcodes = zipcodes
        self.states = states
        self.scope = scope
        self.set_aside = set_aside
        self.naics_codes = naics_codes
        self.class_codes = class_codes
        self.ja_codes = ja_codes
        self.recovery_and_reinvestment = recovery_and_reinvestment
        self.fair_opportunity_codes = fair_opportunity_codes
        self.posted_range_start = posted_range_start
        self.posted_range_end = posted_range_end
        self.response_date_start = response_date_start
        self.response_date_end = response_date_end
        self.last_modified_start = last_modified_start
        self.last_modified_end = last_modified_end
        self.award_date_start = award_date_start
        self.award_date_end = award_date_end

    def _search(self):
        self.driver = webdriver.Firefox()
        self.driver.get(
            'https://www.fbo.gov/index.php?'
            's=opportunity&mode=list&tab=search&tabmode=list&='
        )
        if self.posted:
            select_posted_date(self.driver, self.posted)

        if self.zipcodes:
            enter_zipcodes(self.driver, self.zipcodes)

        if self.states:
            select_performance_state(self.driver, self.states)

        if self.scope:
            select_document_scope(self.driver, self.scope)

        if self.set_aside:
            select_codes(self.driver, self.set_aside, 'set_aside')

        if self.naics_codes:
            select_codes(self.driver, self.naics_codes, 'naics_codes')

        if self.class_codes:
            select_codes(self.driver, self.class_codes, 'class_codes')

        if self.ja_codes:
            select_codes(self.driver, self.ja_codes, 'ja')

        if self.fair_opportunity_codes:
            select_codes(self.driver, self.fair_opportunity_codes, 'fair_opportunity')

        if self.recovery_and_reinvestment:
            toggle_recovery_reinvestment_act(self.driver)

        if self.posted_range_start or self.posted_range_end:
            enter_date_ranges(
                self.driver,
                self.posted_range_start,
                self.posted_range_end,
                date_type='post_range')

        if self.response_date_start or self.response_date_end:
            enter_date_ranges(
                self.driver,
                self.response_date_start,
                self.response_date_end,
                date_type='response_date')

        if self.last_modified_start or self.last_modified_end:
            enter_date_ranges(
                self.driver,
                self.last_modified_start,
                self.last_modified_end,
                date_type='last_modified')

        if self.award_date_start or self.award_date_end:
            enter_date_ranges(
                self.driver,
                self.award_date_start,
                self.award_date_end,
                date_type='award_date')

        submit_form(self.driver)

    def scrape_opportunities(self):
        self._search()
        self.opportunities = get_opportunities(self.driver)

    def export_to_csv(self):
        date_stamp = str(datetime.today().strftime('%m-%d-%Y'))
        df = pd.DataFrame.from_dict(self.opportunities)
        df.to_csv(f'Opportunities {date_stamp}.csv')
