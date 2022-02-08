import time
from storage import LocalStorage
from retry import retry
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

@retry(delay=5)
def click_big_cookie(driver: webdriver.Firefox, n_times=100):
    _id = "bigCookie"
    elem_info = (By.ID, _id)
    element = wait_element(driver, elem_info)

    for i in range(n_times):
        element.click()
        time.sleep(0.001) ## can (and should) be reduced just here for debugging visually on the web page. 
    

def wait_element(driver: webdriver.Firefox, elem_info, timeout: int=30, message: str="Error"):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(elem_info)
        )
        return element 
    except Exception as err:
        print(err, file=sys.stderr)
        raise err


@retry(delay=2)
def open_option_menu(driver: webdriver.Firefox):
    _id = "prefsButton"
    elem_info = (By.ID, _id)
    element = wait_element(driver, elem_info)
    time.sleep(1)
    element.click()


def load(driver: webdriver.Firefox, filename: str):
    pass

@retry(delay=1, tries=5)
def save(driver: webdriver.Firefox, storage: LocalStorage, filename: str):
    actions = ActionChains(driver)
    actions.key_down(Keys.CONTROL).send_keys('s').key_up(Keys.CONTROL).perform()
    time.sleep(1)

    assert "CookieClickerGame" in storage.keys()
    assert filename is not None

    with open(filename, "w") as f:
        f.write(storage.get("CookieClickerGame"))
        
        
    
if __name__ == "__main__":
    driver = webdriver.Firefox()
    storage = LocalStorage(driver)
    url='https://orteil.dashnet.org/cookieclicker/'
    driver.get(url)

    click_big_cookie(driver, 10)
    save(driver, storage, f"/tmp/cookie_clicker_{int(time.time())}.sav")


