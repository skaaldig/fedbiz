# fedbiz
FBO Scraper - Search and Retrieve Basic Federal Business Opportunities Info

Installation:
------
From inside the project folder.
```
pip install requirements.txt
```
This project also requires the installation of the Mozilla Geckodriver: Download Below.  
https://github.com/mozilla/geckodriver/releases

Instructions for installing this driver can be found under the Selenium section of the below ReadMe.  
https://github.com/mozilla/geckodriver


Usage:
------
# Example Use:
```
scraper = FedBizOpps(naics_codes=['111110', '113'], states='NC', posted='90')
scraper.scrape_opportunities()
```

# Search Form Codes:
###### NAICS Codes: 
Six digit NAICS numbers and three digit prefixes can be entered as a string or list of strings. 
```
FedBizOpps(naics_codes='111110')
or
FedBizOpps(naics_codes=['111110', '113'])
```
###### JA Codes:
Federal Acquisition Regulation (FAR) codes can be entered using just the FAR prefix + Regulation number, substituting spaces and special characters for underscores.

```
FedBizOpps(ja_codes='far_6_302_1_c')
or
FedBizOpps(ja_codes=['far_6_302_4', 'far_6_302_5', 'far_6_302_3'])
```

#### Longer Code Arguments:
Much like JA Codes, for the below code types if the code on the search form is longer than a single word, only up to the first three words are required. Spaces and special characters must be substituted for underscores. 

###### Fair Opportunity / Limited Sources Justification Authority:
```
FedBizOpps(fair_opportunity_codes='other_statutory_authority')
or
FedBizOpps(fair_opportunity_codes=['follow_on_delivery', 'minimum_guarantee'])
```
###### Set Aside Codes:
```
FedBizOpps(set_aside='competitive_8_a')
or
FedBizOpps(set_aside=['total_hbcu_mi', 'very_small_business', 'partial_hbcu_mi')
```
### Opportunity/Procurement Type:
```
FedBizOpps(procurement_type='presolicitation')
or
FedBizOpps(procurement_type=['combined_synopsis_solicitation', 'fair_opportunity_limited'])
```
###### Classification Codes:
```
FedBizOpps(class_code='R')
or
FedBizOpps(class_code=['S', 'X', '1', '3', '94'])
```


