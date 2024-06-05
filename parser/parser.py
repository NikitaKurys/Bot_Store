import asyncio
from asyncio import sleep

import selenium.common.exceptions
from selenium.webdriver import Keys, DesiredCapabilities
from selenium.webdriver.common.by import By
import undetected_chromedriver


# Рассчитывает стоимость доставки
async def get_delivery_price(index: str,
                             url='https://www.pochta.ru/PARCELS/?weight=100&addressFrom=1cc2ab3c-1791-4771-b332'
                                 '-d2d96f52788e') -> dict | str:

    options = undetected_chromedriver.ChromeOptions()
    options.add_argument(argument="--headless")
    options.page_load_strategy = "eager"
    driver = undetected_chromedriver.Chrome(options=options,)
    driver.set_window_size(1600, 1900)
    driver.get(url)

    await sleep(1)
    driver.find_element(By.XPATH, '//*[@id="page-parcel"]/div/div/div/div[1]/div[3]/div'
                                  '/div/div[1]/section/div[2]/div[2]/div/div[2]/div/div/div/label[4]').click()
    await sleep(1)
    driver.find_element(By.XPATH, '//*[@id="indexTo"]').send_keys({index})
    await sleep(1)
    driver.find_element(By.XPATH, '//*[@id="page-parcel"]/div/div/div/div[1]/div[3]'
                                  '/div/div/div[1]/section/div[2]/div[3]/div/div/div[2]/div').click()
    await sleep(2)

    try:
        info = driver.find_element(By.XPATH, '//*[@id="page-parcel"]/div/div/div/div[1]/div[3]/div'
                                             '/div/div[1]/section/div[2]/div[3]/div/div/div[1]/div[2]').text
        driver.close()
        return info

    except selenium.common.exceptions.NoSuchElementException:
        price = driver.find_element(By.XPATH, '//*[@id="page-parcel"]/div/div/div/div[2]/div/div[1]/'
                                              'div[2]/div/div[1]/div/div[2]/div').text.replace(",00 ₽", " ")
        location = driver.find_element(By.XPATH, '//*[@id="page-parcel"]/div/div/div/div[1]/div[3]/div/div/div[1]'
                                                 '/section/div[2]/div[3]/div/div/div[2]/div').text.split(".")
        driver.close()
        return {
            "price": int(price),
            "location": location[1],
        }
