# fedbiz
FBO Scraper - Search and Retrieve Federal Business Opportunities

Installation:
------
```
mkvirtualenv fboscraper
pip install requirements.txt
```

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
