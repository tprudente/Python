from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def get_facebook_images_selenium(group_url):
    # Set up the Selenium webdriver with Chrome
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(
        '--headless')  # Optional: run Chrome in headless mode (without opening a visible browser window)

    driver = webdriver.Chrome(options=chrome_options)  # You need to have ChromeDriver installed
    driver.get(group_url)

    try:
        # Wait for the dynamic content to load (adjust timeout as needed)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'XiG zI7 iyn Hsu'))
        )
    except Exception as e:
        print(f"Error waiting for dynamic content: {e}")

    # Get the page source after dynamic content has loaded
    page_source = driver.page_source

    # Close the webdriver
    driver.quit()

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find all img tags on the page
    image_tags = soup.find_all('img')

    if image_tags:
        # Print the src attribute of each img tag
        for img_tag in image_tags:
            img_url = img_tag.get('src')
            if img_url:
                print(img_url)
    else:
        print("No images found on the page.")


# Replace 'YOUR_FACEBOOK_GROUP_URL' with the actual URL of the Facebook group page
facebook_group_url = 'https://br.pinterest.com/vandaandreiamen/border-collie/'
get_facebook_images_selenium(facebook_group_url)




