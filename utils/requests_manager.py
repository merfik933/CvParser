import requests
import bs4
import re
import time

# Headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
}

# Get page content
def get_page(url, tries=3):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        return soup
    except Exception as e:
        if tries > 0:
            print(f"Error while getting page: {e}")
            print(f"Retrying... {tries} tries left")
            time.sleep(3)
            return get_page(url, tries - 1)
        else:
            print(f"Error while getting page: {e}")
            return None
        
# Get text from element
def get_text(element, selector=None, default=""):
    try:
        if selector:
            return element.select_one(selector).text.strip()
        return element.text.strip()
    except Exception as e:
        # print(f"Note: Text not found. Selector: {selector}")
        return default
    
# Get attribute from element
def get_attribute(element, attribute, selector = None, default=""):
    try:
        if selector:
            return element.select_one(selector).get(attribute)
        return element.get(attribute)
    except Exception as e:
        # print(f"Note: Attribute not found. Selector: {selector}")
        return default
    
def get_element(element, selector, default=None):
    try:
        element = element.select_one(selector)
        if not element:
            raise Exception("Data does not exist")
        return element
    except Exception as e:
        return default
    
# Get elements by selector
def get_elements(element, selector, default=[]):
    try:
        elements = element.select(selector)
        if not elements:
            raise Exception("Data does not exist")
        return elements
    except Exception as e:
        return default
    
# Find values by keys in box
def find_values_by_keys_in_box(box, key_selector, value_selector, keys, default=""):
    try:
        keys_elements = get_elements(box, key_selector)
        values_elements = get_elements(box, value_selector)

        if len(keys_elements) != len(values_elements):
            raise Exception("Keys and values count mismatch")

        results = []
        for key in keys:
            matched_value = default
            for key_element, value_element in zip(keys_elements, values_elements):
                if key in key_element.text.strip():
                    matched_value = value_element.text.strip()
                    break
            results.append(matched_value)
        
        return tuple(results)
    except Exception as e:
        # print(f"Error: {e}")
        return tuple([default] * len(keys))

        
        