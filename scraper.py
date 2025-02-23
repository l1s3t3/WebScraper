import requests
from bs4 import BeautifulSoup
import re
from db import create_table, insert

start_url = "https://www.myprotein.ee/all-offers/zlava-50-na-doplnky-chudnutie.list"


def parse(url, results):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    product_data = soup.find_all("span", class_="js-enhanced-ecommerce-data")
    product_images = soup.find_all("div", class_="athenaProductBlock_imageContainer")

    if not product_data or not product_images:
        print(f"Leht {url} on tühi.")
        return


    for data, image in zip(product_data, product_images): # zip, sest muidu läheb pilt nihkesse
        title = data.get("data-product-title", "").strip()
        price_text = data.get("data-product-price", "").strip()

        img_tag = image.find("img")
        image_url = img_tag["src"]

        try:
            price_value = float(price_text.replace("€", "").replace(",", "."))
        except ValueError:
            price_value = 0.0

        results.append({
            "title": title,
            "price": price_value,
            "image": image_url
        })

    next_button = soup.find("button", class_="responsivePaginationNavigationButton paginationNavigationButtonNext")

    if next_button:
        match = re.search(r'pageNumber=(\d+)', url)
        if match:
            current_page = int(match.group(1))
            next_url = re.sub(r'pageNumber=\d+', f'pageNumber={current_page + 1}', url)
        else:
            next_url = f"{url}?pageNumber=2"
        parse(next_url, results)
    else:
        print("Lõpetame")


def scrape_all():
    results = []
    parse(start_url, results)
    return results


if __name__ == "__main__":
    create_table()
    all_data = scrape_all()
    print(f"Kokku {len(all_data)} toodet.")
    insert(all_data)
