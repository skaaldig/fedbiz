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
#### Search Form Codes:
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

###### Fair Opportunity / Limited Sources Justification Authority:
Much like JA Codes, you only need enter the Fair Opportunity type as a string or list of strings. If type is longer than a single word, only up to the first three words are required (subsituting underscores for spaces). 

```
FedBizOpps(fair_opportunity_codes='other_statutory_authority')
or
FedBizOpps(fair_opportunity_codes=['follow_on_delivery', 'minimum_guarantee'])

