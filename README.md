# Israel Tree Removal Permit Scraper

Basic Python utilities to download and make some basic parsing/normalization to Israel's tree removal permit Excel files published by the Ministry of Agriculture.   

URLs are collected from: <https://www.moag.gov.il/yhidotmisrad/forest_commissioner/rishyonot_krita/Pages/default.aspx>


## Requirements

* Python 3.8+ (Tested on Python 3.9 on linux)
* [poetry](https://python-poetry.org/docs/#installation)

## Setup

1. Clone the project locally (with `--recurse-submodules` !) and cd into it.


   * Using https:
        
         git clone --recurse-submodules https://github.com/hasadna/israel_tree_removal_permit_scraper
         cd israel_tree_removal_permit_scraper
      
   * Using ssh:
      
         git clone --recurse-submodules git@github.com:hasadna/israel_tree_removal_permit_scraper.git
         cd israel_tree_removal_permit_scraper
  
2. Install python requirements:
   
       poetry install

## Running

      poetry run run.py


----


Published under the MIT License.
