# Israel Tree Removal Permit Scraper

Basic Python utilities to download and make some basic parsing/normalization to Israel's tree removal permit Excel files published by the Ministry of Agriculture.   

URLs are collected from: <https://www.moag.gov.il/yhidotmisrad/forest_commissioner/rishyonot_krita/Pages/default.aspx>

🌳🌲🌴 Inspired By [Meirim](https://meirim.org/)! 🌴🌲🌳 


## Requirements

* Python 3.8+ (Tested on Python 3.9 on linux)
* [poetry](https://python-poetry.org/docs/#installation)

## Setup

1. Clone the project locally (with `--recurse-submodules` !) and cd into it.


   * Using https:
        
         git clone https://github.com/hasadna/israel_tree_removal_permit_scraper
         cd israel_tree_removal_permit_scraper
         git clone https://github.com/hasadna/israel_tree_removal_permits_raw.git downloads
         git clone https://github.com/hasadna/israel_tree_removal_permits_csv.git csv_exports
         git clone https://github.com/hasadna/israel_tree_removal_permits_text.git text_exports

      
   * Using ssh:
      
         git clone git@github.com:hasadna/israel_tree_removal_permit_scraper.git
         cd israel_tree_removal_permit_scraper
         git clone git@github.com:hasadna/israel_tree_removal_permits_raw.git downloads
         git clone git@github.com:hasadna/israel_tree_removal_permits_csv.git csv_exports
         git clone git@github.com:hasadna/israel_tree_removal_permits_text.git text_exports
  
2. Install python requirements:
   
       poetry install

## Running

      poetry run run.py


----


Published under the MIT License.
