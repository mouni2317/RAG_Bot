from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def setup_edge():
    edge_options = Options()
    edge_options.use_chromium = True
    edge_options.add_argument("--start-maximized")
    edge_options.add_argument("--disable-blink-features=AutomationControlled")
    # Optional: edge_options.add_argument("--headless=new")
    driver = webdriver.Edge(options=edge_options)
    return driver


def get_overview_text(driver):
    selectors = [
        # Copilot smart answers
        "div.b_wpt_bl",
        "p.b_paractl",

        # Copilot chat style
        "div.cib-chat",
        "div.cib-serp-main",

        # GS cards / generated answers
        "span.gs_cit_txt",
        "div.gs_text",
        "div.gs_temp_content",
        "div.gs_card_ans",

        # Classic Bing AI answer panels
        "div.acs-rich-card",
        "div.b_focusTextLarge",
        "div.b_ans",
        "div.b_xlText",
        "div.b_entityTP",
        "div.b_vPanel",
    ]

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "b_content"))
        )
    except:
        return "Search results did not load in time."

    for selector in selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            for el in elements:
                text = el.text.strip()
                if text and len(text) > 40:
                    return f"[Selector: {selector}]\n{text}"
        except:
            continue

    return "No overview found using known selectors."


def search_and_extract(query):
    driver = setup_edge()
    try:
        url = f"https://www.bing.com/search?q={query.replace(' ', '+')}"
        driver.get(url)
        time.sleep(3)  # wait for AI modules to finish rendering
        overview = get_overview_text(driver)
        print("=== Extracted Overview ===\n" + overview)
    finally:
        driver.quit()


# === Example ===
search_and_extract("what are treasury bonds")
