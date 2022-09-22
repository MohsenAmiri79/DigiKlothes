# Digikala Clothes Images Dataset

## Introduction
This dataset contains:
- more than 55,000 clothing items from [digikala.com](https://www.digikala.com/)
- name, price, discount, rating, url and a list of the url for all of each item's images.

## Data

#### What each folder contains:
1. **raw_Data:** Contains everything except image urls.
2. **clean_Data:** Contains everything.
3. **clean_reduced_Data:** Contains only names, urls, and image urls.

## Reproducing the data

#### What each code file does:
1. **'category product scraper.py'** searches the input category in the website and extracts the name, price, discount, rating and url of each item.
2. **'preprocess_clean.ipynb'** uses the csv files in the *'raw_Data'* folder and finds the image links for each record of the csv file.
3. **'Single product image scraper.py'** extracts the image links of the input (have to be set by hand) link.
4. **'preprocess_reduce.ipynb'** uses the csv files in the *'clean_Data'* folder and drops the price, discount and rating columns.
