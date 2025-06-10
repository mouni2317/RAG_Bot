from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def setup_edge_driver():
    options = Options()
    options.add_argument("--start-maximized")
    return webdriver.Edge(options=options)

def get_overview_text(driver):
    # Try multiple known selectors that Bing uses for AI/Copilot/Knowledge answers
    selectors = [
        # Copilot smart answers
        "div.b_wpt_bl",
        "p.b_paractl",

        # Copilot chat UI
        "div.cib-chat",
        "div.cib-serp-main",

        # AI summaries from new GS cards
        "span.gs_cit_txt",
        "div.gs_text",
        "div.gs_temp_content",
        "div.gs_card_ans",

        # Classic smart answers
        "div.acs-rich-card",
        "div.b_focusTextLarge",
        "div.b_ans",
        "div.b_xlText",
        "div.b_entityTP",
        "div.b_vPanel",
    ]



    # Wait for results page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "b_content")))

    # Try each selector and return the first non-empty result
    for selector in selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            for element in elements:
                text = element.text.strip()
                if text:
                    return f"[Selector: {selector}]\n{text}"
        except Exception:
            continue
    return "No overview found using known selectors."

def search_and_extract(query):
    driver = setup_edge_driver()
    try:
        driver.get("https://www.bing.com")

        # Input the search query
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        # Allow time for AI or Copilot answers to load
        time.sleep(3)

        overview = get_overview_text(driver)
        print("\n=== Extracted Overview ===")
        print(overview)
    finally:
        driver.quit()

# Example usage
search_and_extract("What is DV01?")
