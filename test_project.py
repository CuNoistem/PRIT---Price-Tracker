import project
import textwrap
from project import URL
from datetime import datetime


def test_find_domain_name():
    assert project.find_domain_name("https://www.flipkart.com/urban-terrain-bolt-cycles-men-front-suspension-dual-disc-brake-mtb-bike-ut5001s27-5-27-5-t-road-cycle/p/itm3550b2865d567?pid=CCEG6N4YKKPFWRSH&lid=LSTCCEG6N4YKKPFWRSHPMK9DA&marketplace=FLIPKART&store=abc%2Fulv%2Fixt&spotlightTagId=FkPickId_abc%2Fulv%2Fixt&srno=b_1_4&otracker=browse&fm=organic&iid=17d9d282-8a31-4dd6-85c6-be3db0fafa74.CCEG6N4YKKPFWRSH.SEARCH&ppt=browse&ppn=browse&ssid=nb820eajzedm1p8g1717419852559") == "flipkart"

    assert project.find_domain_name("https://www.amazon.in/Sirohi-Furniture-Organizer-bathroom-Decorative/dp/B0C1NZR6HS/?_encoding=UTF8&pd_rd_w=olELK&content-id=amzn1.sym.edc37d23-dba3-4bec-9362-841b5fd69091&pf_rd_p=edc37d23-dba3-4bec-9362-841b5fd69091&pf_rd_r=5F5NZQNQW0C8A7RFVRXT&pd_rd_wg=3i35d&pd_rd_r=13e20f6d-544d-4e93-b21b-0e5dab70e776&ref_=pd_hp_d_btf_kar_gw_pc_en_") == "amazon"


def test_get_dict():
    assert URL.get_dict([URL(url="https://cs50.harvard.edu/python", product_name="CS50", current_price="0")]) == {"S.No.": [1], "Product Name": ["CS50"], "Current Price": ["0"], "Threshold Price": [-1], "Last Updated Time": [datetime.now().replace(microsecond=0)]}

def test_tabulate_data():
    assert project.tabulate_data([URL(url="https://cs50.harvard.edu/python", product_name="CS50", current_price="0")]) == None
