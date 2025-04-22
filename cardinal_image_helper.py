import json
import time
from urllib.parse import quote_plus

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def main():
    INPUT_JSON  = 'cardinals.json'
    OUTPUT_JSON = 'cardinals_with_images.json'
    HEADLESS    = False

    opts = webdriver.ChromeOptions()
    if HEADLESS:
        opts.add_argument('--headless')
        opts.add_argument('--disable-gpu')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(), options=opts)
    wait   = WebDriverWait(driver, 10)

    with open(INPUT_JSON, 'r') as f:
        cardinals = json.load(f)

    for entry in cardinals:
        name = entry.get('name','').strip()
        if not name:
            continue

        print(f"\n→ Looking up: {name}")
        # Go to the exact wiki search page
        search_url = 'https://en.wikipedia.org/w/index.php?search=' + quote_plus(name)
        driver.get(search_url)

        # If this is still the search results page, click the first hit
        if '/w/index.php?search=' in driver.current_url:
            try:
                first = wait.until(EC.element_to_be_clickable((
                    By.CSS_SELECTOR, '.mw-search-result-heading a'
                )))
                first.click()
            except TimeoutException:
                print(f"  ⚠️ No Wikipedia page found for “{name}”")
                continue

        # Now on the article—grab the infobox image via CSS
        try:
            img = wait.until(EC.presence_of_element_located((
                By.CSS_SELECTOR,
                'table.infobox.vcard .infobox-image img'
            )))
            src = img.get_attribute('src')
            # prefix protocol if needed
            if src.startswith('//'):
                src = 'https:' + src

            entry['image'] = src
            print("  ✅ Got image:", src)

        except TimeoutException:
            print("  ⚠️ No infobox image found for", name)

        # polite pause
        time.sleep(1.0)

    # write results
    with open(OUTPUT_JSON, 'w') as f:
        json.dump(cardinals, f, indent=2, ensure_ascii=False)

    print(f"\nDone! 👉 {OUTPUT_JSON}")
    driver.quit()

if __name__ == '__main__':
    main()