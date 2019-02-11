from bs4 import BeautifulSoup
import requests
import re


# BAZAR
def scrape_bazar(keywords, price_range):
    '''
    Based on user's keywords(list) and the price_range(tuple) 
    this function searches the perfect products for
    the user in Bazar
    '''

    searched_products = {}

    try:
        for page in range(1, 10):
            url = "https://bazar.bg/obiavi?q=" + "%20".join(keywords) + "&page=" + str(page)

            source = requests.get(url).text

            soup = BeautifulSoup(source, "lxml")

            products = soup.find_all("span", class_="title")
            prices = soup.find_all("span", class_="price")
            product_urls = soup.find_all("a", class_="listItemLink")
            product_imgs = soup.find_all("img", class_="cover")

            if products:
                for i in range(len(products)-2):
                    # Name
                    curr_product = products[i].text.lstrip().split("\n")[0]

                    # Price
                    curr_price = int(prices[i].text.split()[0].split(",")[0])

                    # URL
                    curr_url = product_urls[i]["href"]

                    # Thumbnails
                    curr_img = product_imgs[i]["src"]

                    if curr_price > price_range[0] and curr_price < price_range[1]:
                        searched_products[curr_product] = (curr_price, curr_url, curr_img)
            else:
                print("No products found!")
    except Exception as e:
        print(e)

    print(searched_products)

    return searched_products


# EMAG
def scrape_emag(searched_words, price_range):
    '''
    Based on user's searched_words(list) and the price_range(tuple) 
    this function searches the perfect products for
    the user in Emag
    '''

    # An example for a link created with a user input that is: adidas shoe
    # https://www.emag.bg/search/adidas%20shoe?ref=effective_search#opensearch

    for page in range(1, 10):
        url = "https://www.emag.bg/search/" + "+".join(searched_words).lower() + "/p" + str(page)

        source = requests.get(url).text

        soup = BeautifulSoup(source, "lxml")

        items = soup.find_all("div", class_="card-item")

        item_inventory = {}

        suited_items = {}

        if items:
            print("All Products:")
            for item in items:
                try:
                    item_name = item["data-name"]
                    url = str(item.find("a", class_="thumbnail-wrapper")["href"])
                    img_url = str(item.find("img")["src"])
                    paragraph_price = str(item.find("p", "product-new-price"))
                    numbers = re.findall(r"(?<=>)(\d+)(?=<)", paragraph_price)
                    leva = numbers[0]
                    penny = numbers[1]
                    price = float(str(leva + "." + penny))

                    # Dictionary with a KEY - item name and VALUE - item price
                    item_inventory[item_name] = (price, url, img_url)

                except Exception as e:
                    pass

            print("\n\n\nItems that are perfect for you:")
            for item, values in item_inventory.items():
                if price_range[0] < values[0] and values[0] < price_range[1]:
                    suited_items[item] = (values[0], values[1], values[2])

        else:
            print("No items found!")

        return suited_items


# OLX
def scrape_olx(keywords, price_range):
    '''
    Based on user's keywords(list) and the price_range(tuple) 
    this function searches the perfect products for
    the user in Olx
    '''

    searched_products = {}

    try:
        for page in range(1, 10):
            url = "https://www.olx.bg/ads/q-" + "-".join(keywords) + "/" + "?page=" + str(page)

            print(url)

            source = requests.get(url).text

            soup = BeautifulSoup(source, "lxml")

            products = soup.find_all("a", class_="marginright5")

            prices = soup.find_all("p", class_="price")

            product_images = soup.find_all("img", class_="fleft")

            product_urls = soup.find_all("a", class_="thumb")

            if products:
                for i in range(len(products)):
                    # URL
                    curr_url = product_urls[i]["href"]

                    # Image
                    curr_image = product_images[i]["src"]

                    # Price
                    curr_price = int(float(prices[i].strong.text.split()[0]))
                    
                    # Product
                    curr_product = products[i].strong.text
                    if curr_price > price_range[0] and curr_price < price_range[1]:
                        searched_products[curr_product] = (curr_price, curr_url, curr_image)
                        
            else:
                print("No products found!")

    except Exception as e:
        pass

    print(searched_products)

    return searched_products



def mixed_search(keywords, price_range):
    '''Combination of Bazar, Olx and Emag search.'''

    items = {}

    items.update(scrape_bazar(keywords, price_range))
    items.update(scrape_olx(keywords, price_range))
    items.update(scrape_emag(keywords, price_range))

    return items