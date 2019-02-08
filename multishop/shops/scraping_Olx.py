from bs4 import BeautifulSoup
import requests
import re



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

if __name__ == "__main__":

    product = input("Enter keywords: ").split()
    p_range = (int(input("Minimum price: ")), int(input("Maximum price: ")))

    scrape_olx(product, p_range)