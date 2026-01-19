import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def wake_up_apps(urls):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        for url in urls:
            print(f"Visiting {url}...")
            driver.get(url)
            time.sleep(10) # Wait for Streamlit to initialize
            print(f"Successfully pinged {url}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    # Add all your Streamlit URLs here
    my_apps =  "https://analytica-ai.streamlit.app/",
    wake_up_apps(my_apps)
