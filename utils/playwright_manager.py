from playwright.sync_api import sync_playwright

import time
import bs4

def launch_playwright(main_directory):
    try:
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        browser = context.new_page()
        return browser
    except Exception as e:
        print(f"Error while launching browser: {e}")
        input("Press Enter to exit...")
        exit()
        return None
    
def close_playwright(browser):
    browser.context().close()
    browser.close()
    
def goto_page(browser, url, tries=3, timeout=10000):
    try:
        browser.goto(url, timeout=timeout)
    except Exception as e:
        if tries > 0:
            print(f"Error while going to page: {e}")
            print(f"Retrying... {tries} tries left")
            time.sleep(3)
            return goto_page(browser, url, tries - 1)
        else:
            print(f"Error while going to page: {e}")
            return None
        
def get_current_page(browser):
    try:
        html = browser.content()
        soup = bs4.BeautifulSoup(html, "html.parser")
        return soup
    except Exception as e:
        print(f"Error while getting page: {e}")
        return None
    
def get_locator(browser, selector, default=None, search_text=None):
    try:
        if search_text:
            return browser.locator(selector, has_text=search_text)
        return browser.locator(selector)
    except Exception as e:
        # print(f"Error while getting locator: {e}")
        return default
    
def get_element(browser, selector, default=None):
    try:
        element = browser.query_selector(selector)
        if not element:
            raise Exception("Element does not exist")
        return element
    except Exception as e:
        # print(f"Error while getting element: {e}")
        return default
    
def get_elements(browser, selector, default=[]):
    try:
        elements = browser.query_selector_all(selector)
        if not elements:
            raise Exception("Elements do not exist")
        return elements
    except Exception as e:
        # print(f"Error while getting elements: {e}")
        return default
    
def wait_for(browser, selector, timeout=10000, default=None):
    try:
        element = browser.wait_for_selector(selector, timeout=timeout)
        soup = bs4.BeautifulSoup(element.inner_html(), "html.parser")
        return soup
    except Exception as e:
        # print(f"Error while waiting for selector: {e}")
        return None
    
def wait_for_detached(browser, locator, timeout=10000, default=None):
    try:
        locator.wait_for(state="detached", timeout=timeout)
        return True
    except Exception as e:
        return False  
    
def click_element(browser, selector, default=None):
    try:
        button = browser.query_selector(selector)
        if not button:
            raise Exception("Element does not exist")
        button.scroll_into_view_if_needed()
        button.click()
        return button
    except Exception as e:
        # print(f"Error while clicking element: {e}")
        return default
    
def click_locator(locator, default=None):
    try:
        locator.scroll_into_view_if_needed()
        locator.click()
        return locator
    except Exception as e:
        # print(f"Error while clicking locator: {e}")
        return default