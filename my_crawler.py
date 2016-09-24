"""
This module is used to crawl shopping.com to get overview and detailed information about a product listed on the website.
"""

__author__ = "jainaka"

import re
import sys

import requests
from bs4 import BeautifulSoup

url_product_main = "http://www.shopping.com/products?KW={0}"
url_product_pagewise = "http://www.shopping.com/products~PG-{0}?KW={1}"


def search_info(search_query):
    """
    Provides the count of total number of products available for the given search query
    :param search_query: string to search the website
    """
    print "Fetching product information"
    try:
        html_response = requests.get(url_product_main.format(search_query))
    except requests.exceptions.RequestException as e:
        print "ERROR: ", e.message
        return
    status_code = html_response.status_code
    if html_response.status_code != 200:
        print "ERROR: ", requests.status_codes._codes[status_code][0]
        return
    html_dump = BeautifulSoup(html_response.text, "lxml")
    search_result_count = html_dump.find(class_='numTotalResults')
    if not search_result_count:
        print "No results were found for the given keyword"
        return
    print "Number of products found::", search_result_count.text.split()[-1]


def search_detailed(search_query, page_number):
    """
    Provides the detailed information about the product given in the search query
    :param search_query: string to search the website
    :param page_number: integer to get the information of particular page number of result
    """
    print "Fetching product information for given page"
    try:
        check = int(page_number)
    except ValueError:
        print "Page number should be an integer"
        return
    try:
        html_response = requests.get(url_product_pagewise.format(page_number, search_query))
    except requests.exceptions.RequestException as e:
        print "ERROR: ", e.message
        return
    status_code = html_response.status_code
    if html_response.status_code != 200:
        print "ERROR: ", requests.status_codes._codes[status_code][0]
        return
    html_dump = BeautifulSoup(html_response.text, "lxml")
    products = html_dump.find_all(id=re.compile("quickLookItem"))
    total_products = len(products)
    print "Total products:: " + str(total_products)
    for index in range(len(products)):
        product = products[index]
        print "---------------------------"
        print "Product {}".format(index + 1)
        title = product.find(class_="quickLookGridItemFullName")
        title_text = title.text.strip() if title else "Not available"
        print "Title::", title_text.encode('ascii', 'ignore')

        price = product.find(class_="productPrice")
        price_text = price.text.strip() if price else "Not available"
        print "Price::", price_text.encode('ascii', 'ignore')

        if product.find(class_="placeholderImg"):
            img_url = product.find(class_="placeholderImg").text.split("?")[0]
        elif product.find('img'):
            img_url = product.find('img').get("src").split("?")[0]
        else:
            img_url = None
        print "Image url::", img_url.encode('ascii', 'ignore')

        shipping = product.find(class_="taxShippingArea")
        shipping_text = shipping.text.strip() if shipping else "Not available"
        print "Shipping::", shipping_text.encode('ascii', 'ignore')

        merchant = product.find(class_="newMerchantName")
        merchant_text = merchant.text.strip() if merchant else "Not available"
        print "Merchant::", merchant_text.encode('ascii', 'ignore')


if __name__ == '__main__':
    try:
        if len(sys.argv) == 2:
            search_info(sys.argv[1])
        elif len(sys.argv) == 3:
            search_detailed(sys.argv[1], sys.argv[2])
        else:
            print "ERROR: Invalid command"
    except Exception, e:
        print "ERROR:", e
