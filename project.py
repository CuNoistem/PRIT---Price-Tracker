from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from alive_progress import alive_bar
from datetime import datetime
from tabulate import tabulate
from playsound import playsound
import re
import time
import os
import textwrap


UPDATE_TIME = 5


class URL:
    def __init__(self, url, product_name, current_price, threshold_price=-1):
        self.url = url
        self.product_name = product_name
        self.current_price = current_price
        self.threshold_price = threshold_price
        self.time = datetime.now().replace(microsecond=0)


    @classmethod
    def delete_item(cls, item_object):
        with open("saved_url.txt") as file:
            urls = file.readlines()

        with open("saved_url.txt", "w") as file:
            for url in urls:
                if url.strip('\n') != item_object.url:
                    file.write(url)


    @classmethod
    def save_item(cls, url):
        with open("saved_url.txt", "a") as file:
            file.write(f"{url}\n")


    @classmethod
    def load_item(cls):
        urls = [] 
        with open ("saved_url.txt") as file:
            for url in file:
                urls.append(url.rstrip())
        return urls


    @classmethod
    def get_dict(cls, url_objects):
        tabulate_dict = {"S.No.": [], "Product Name": [], "Current Price": [], "Threshold Price": [], "Last Updated Time": []}
        counter = 0

        for url_object in url_objects:
            tabulate_dict["S.No."].append(counter := counter + 1)
            tabulate_dict["Product Name"].append(url_object.product_name)
            tabulate_dict["Current Price"].append(url_object.current_price)
            tabulate_dict["Threshold Price"].append(url_object.threshold_price)
            tabulate_dict["Last Updated Time"].append(url_object.time)

        return tabulate_dict


    @classmethod
    def check_threshold(cls, url_objects):
        for url_object in url_objects:
            if url_object.threshold_price != -1:
                if int(url_object.current_price.replace(",", "").replace("₹", "")) <= url_object.threshold_price:
                    playsound('alert.mp3')


    @classmethod
    def update_price(cls, url_objects, driver):
        try:
            with alive_bar(len(url_objects), title="Updating Price...") as bar:
                for url_object in url_objects:

                    driver.get(url_object.url)
                    price = url_object.current_price

                    match find_domain_name(url_object.url):
                        case "amazon":
                            price = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "span.a-price:nth-child(3) > span:nth-child(2) > span:nth-child(2)"))
                            )
                            price = price.text
                        case "flipkart":
                            price = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, ".CxhGGd"))
                            )
                            price = price.text
                        case _:
                            print("Unknown Domain")

                    url_object.current_price = price
                    url_object.time = datetime.now()

                    bar()
        except Exception as e:
            print(e)
        finally:
            return url_objects


def driver_configuration():
    options = Options()

    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    profile = webdriver.FirefoxProfile()

    profile.set_preference('permissions.default.image', 2)
    profile.set_preference('javascript.enabled', False)
    options.profile = profile

    service = Service('geckodriver')

    driver = webdriver.Firefox(service=service, options=options)
    driver.set_page_load_timeout(30)

    return driver


def find_domain_name(url):
    if matches := re.match(r"^https://www\.(.+)\.(?:com|in)/", url):
        return matches.group(1)


def create_object(urls, driver):
    url_objects = []
    try:
        with alive_bar(len(urls), title="Fetching Products...") as bar:
            for url in urls:

                driver.get(url)

                match find_domain_name(url):
                    case "amazon":
                        # Finding product_name
                        name = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.ID, "productTitle"))
                        )
                        # Finding current_price
                        price = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "span.a-price:nth-child(3) > span:nth-child(2) > span:nth-child(2)"))
                        )
                        url_objects.append(URL(url=url, product_name=textwrap.shorten(text=name.text.split("|")[0], width=50) if "|" in name.text else textwrap.shorten(text=name.text, width=50), current_price=price.text))
                    case "flipkart":
                        name = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "VU-ZEz"))
                        )
                        price = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, ".CxhGGd"))
                        )
                        url_objects.append(URL(url=url, product_name=textwrap.shorten(text=name.text.split("|")[0], width=50) if "|" in name.text else textwrap.shorten(text=name.text, width=50), current_price=price.text))
                    case _:
                        print("Unknown Domain")

                bar()
    except Exception as e:
        print(e)
    finally:
        return url_objects


def tabulate_data(url_objects):
    print(tabulate(URL.get_dict(url_objects=url_objects), headers="keys", tablefmt="simple_outline", numalign="center"))


def user_save_url(driver):
    try:
        while True:
            url = input("URL: ")
            URL.save_item(url)
    except EOFError:
        print()
        pass
    finally:
        return create_object(URL.load_item(), driver)


def user_start_tabulate(url_objects, driver, update_time):
    while True:
        os.system('clear')
        URL.check_threshold(url_objects)
        tabulate_data(url_objects=url_objects)
        try:
            with alive_bar(update_time, title="Seconds") as bar:
                for _ in range(update_time):
                    time.sleep(1)
                    bar()
        except KeyboardInterrupt:
            os.system('clear')
            break
        url_objects = URL.update_price(url_objects, driver)


def user_set_threshold(url_objects):
    try:
        index = int(input("Enter index to set threshold: ")) - 1
        threshold_price = int(input("Enter new threshold price: "))
        url_objects[index].threshold_price = threshold_price
        tabulate_data(url_objects=url_objects)
    except TypeError:
        print("Not a valid integer value")


def user_delete_item(url_objects):
    while True:
        try:
            if (index := int(input("Enter index to delete: ")) - 1) <= len(url_objects) - 1:
                break
            else:
                raise TypeError
        except TypeError:
            print("Not a valid index")
    URL.delete_item(url_objects[index])
    del url_objects[index]
    tabulate_data(url_objects=url_objects)


def main():

    driver = driver_configuration()
    url_objects = create_object(URL.load_item(), driver)

    while True:
        os.system('clear')
        tabulate_data(url_objects)
        print("1. Save Item\n2. Start Recording\n3. Set Threshold\n4. Delete Item\n5. Exit")
        try:
            match(input("Choice: ")):
                case "1":
                    url_objects.clear()
                    url_objects = user_save_url(driver=driver)
                case "2":
                    user_start_tabulate(url_objects=url_objects, driver=driver, update_time=UPDATE_TIME)
                case "3":
                    user_set_threshold(url_objects=url_objects)
                case "4":
                    user_delete_item(url_objects=url_objects)
                case "5":
                    print("Exiting")
                    break
                case _:
                    print("Not in Options")
        except EOFError:
            print("Exiting")
            break
        except TypeError:
            print("Not an option")
        except Exception as e:
            print(e)

    driver.quit()


if __name__ == "__main__":
    main()
