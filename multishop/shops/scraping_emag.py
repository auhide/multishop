from bs4 import BeautifulSoup
import requests
import re



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
                    print(item, "\nPrice:{}лв".format(values[0]))
                    print("----------------------------")
                    suited_items[item] = (values[0], values[1], values[2])

        else:
            print("No items found!")

        return suited_items


def run_app():
    user_input = input("Enter what you need to search in Emag: ")
    words = user_input.split()
    print("Enter price range:")

    minimum = float(input("Minimum: "))
    maximum = float(input("Maximum: "))

    # Tuple for price range
    price_range = (minimum, maximum)

    scrape_emag(words, price_range)



if __name__ == '__main__':
    run_app()