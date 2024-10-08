import json
import time
from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .config import TAB


def tab_click(driver: webdriver.Chrome) -> None:
    tab = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, TAB)))
    tab.click()


def get_product_links(driver: webdriver.Chrome) -> List[str]:
    tab_click(driver)

    time.sleep(3)
    shop_container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "jsx-3055984232.shopContainer"))
    )

    products = shop_container.find_elements(By.CLASS_NAME, "jsx-3055984232")
    products_links = [
        product.get_attribute("href")
        for product in products
        if product.get_attribute("href")
    ]
    return products_links


def get_product_images(product_container) -> List[str]:
    images_containers = product_container.find_elements(
        By.CLASS_NAME, "jsx-2606422244.image-small"
    )

    images_link = []
    for image_container in images_containers:
        image = image_container.find_element(By.TAG_NAME, "img")
        images_link.append(image.get_attribute("src"))

    return images_link


def get_product_info(product_container) -> Dict[str, List[str]]:
    title_and_price_container = product_container.find_element(
        By.CLASS_NAME, "jsx-3762905273.spuBase"
    )
    try:
        title = title_and_price_container.find_element(
            By.CLASS_NAME, "jsx-1513790581.title"
        ).text
    except:
        title = title_and_price_container.find_element(
            By.CLASS_NAME, "jsx-1513790581.title.fold"
        ).text

    price = title_and_price_container.find_element(
        By.CLASS_NAME, "jsx-2407367240.amount"
    ).text

    sizes = product_container.find_elements(By.CLASS_NAME, "jsx-706577070.square")
    size_list = [size.text for size in sizes if size.isdigit()]

    product_info = {"title": title, "price": price, "size_list": size_list}

    return product_info


def get_products(driver: webdriver.Chrome) -> Dict[str, Dict[str, List[str]]]:
    products_link = get_product_links(driver)
    products = {}

    for link in products_link:
        driver.get(link)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "jsx-2606422244.image-small")
            )
        )

        product_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "jsx-2029617322.container"))
        )

        product_images = get_product_images(product_container)
        product_info = get_product_info(product_container)

        products[link] = {"product": product_info, "images": product_images}

    with open("products.json", "w", encoding="utf-8") as json_file:
        json.dump(products, json_file, ensure_ascii=False, indent=4)

    return products
