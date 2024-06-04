# PRIT - Price Tracker
#### Video Demo:  <https://youtu.be/C0MEcCHq5dU>
#### Description:

###### Introduction:
PRIT is a price tracking solution for any item that you wish to track on any e-commerce website on the internet. You can set the wanted price for any product, start the recording, and the program will track the price of the product and keep track of the price. Once the price reaches equal to or below the wanted price, then the program will product an alerting sound to notify you about the price drop.

Leverging basic web scraping and other tools, one can be assured of alerts as soon as the price drops to your wanted level.

###### Tools Used:
- **Selenium**: It is used to automate the process of web browsing and web scraping using the Firefox module (geckodriver).
- **Tabulate**: Used to tabulate the Product Name, Price, Threshold Price and the Last Updated Time.
- **Playsound**: It is used play the alert sound when the price drops.
- **Alive_Progress**: Used to display the progress bar when fetching data from the web browser for the current price of the product.

###### Usage:
Pip install the following python packages:
```
pip install selenium
pip install playsound
pip install textwrap
pip install tabulate
pip install alive-progress
```
and then run the program.

###### Note:
Currently only 2 e-commerce websites are supported, which can easily be expanded by using web scraping for the particular html file of any e-commerce website.

These websites are:
- www.amazon.in
- www.flipkart.com

###### Options:
1. *Add Item*: This option adds urls to the program, which is then saved into a "saved_url.txt" file.
2. *Start Recording*: This option is used to start the tracking of the prices of the product saved in the file.
3. *Set Threshold*: This option is used to set the threshold or desired price for a product. The default threshold price is -1, which denotes no threshold price is set.
4. *Delete Item*: This option is used to remove the products from the list of products you created.
5. EXIT

###### Additional Notes:
- Once the recording is started, you can exit out of it using Ctrl+C.
- You can also exit out the program by using Ctrl+D.
