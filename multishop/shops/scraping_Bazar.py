from bs4 import BeautifulSoup
import requests
import re

def scrape_bazar(keywords, price_range):
    '''
    Based on user's keywords(list) and the price_range(tuple) 
    this function searches the perfect products for
    the user in Bazar
    '''

    searched_products = {}

    try:
        for page in range(1, 4):
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


if __name__ == '__main__':
    product = input("Enter keywords: ").split()
    p_range = (int(input("Minimum price: ")), int(input("Maximum price: ")))

    scrape_bazar(product, p_range)