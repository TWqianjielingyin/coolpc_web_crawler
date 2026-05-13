import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
import csv

from category.cpu import get_cpu
from category.mb import get_mb
from category.gpu import get_gpu
from category.ram import get_ram
from category.ssd import get_ssd

URL = "https://www.coolpc.com.tw/evaluate.php"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "zh-TW,zh;q=0.9",
}
def fetch_html():
    response = requests.get(URL, headers=HEADERS, timeout=15)
    response.raise_for_status()
    response.encoding = "big5"
    return response.text

def find_cpu_select(soup):
    return soup.find("select", {"name": "n4"})
def find_mb_select(soup):
    return soup.find("select", {"name": "n5"})
def find_ram_select(soup):
    return soup.find("select", {"name": "n6"})
def find_ssd_select(soup):
    return soup.find("select", {"name": "n7"})
def find_gpu_select(soup):
    return soup.find("select", {"name": "n12"})

def duo_source(results):
    product_map = {}

    for item in results:
        key = item["source_key"]

        if key not in product_map:
            product_map[key] = item
        else:
            if item["price"] > product_map[key]["price"]:
                product_map[key] = item

    return list(product_map.values())
def save_to_csv(results):
    now = datetime.now().strftime("%Y%m%d")

    os.makedirs("csv_data", exist_ok=True)
    filename = f"csv_data/coolpc_{now}.csv"

    with open(filename, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["category", "brand", "model", "product", "price", "source_key"]
        )

        writer.writeheader()
        writer.writerows(results)

    return filename

def main():
    html = fetch_html()
    soup = BeautifulSoup(html, "html.parser")
    all_results = []

    print("正在抓取原價屋 CPU 資料...")
    cpu_select = find_cpu_select(soup)
    cpu_results = get_cpu(cpu_select)
    all_results.extend(cpu_results)
    print(f"共抓到 {len(cpu_results)} 筆 CPU")

    print("正在抓取原價屋 MotherBoard 資料...")
    mb_select = find_mb_select(soup)
    mb_results = get_mb(mb_select)
    all_results.extend(mb_results)
    print(f"共抓到 {len(mb_results)} 筆 MotherBoard")

    print("正在抓取原價屋 GPU 資料...")
    gpu_select = find_gpu_select(soup)
    gpu_results = get_gpu(gpu_select)
    all_results.extend(gpu_results)
    print(f"共抓到 {len(gpu_results)} 筆 GPU")

    print("正在抓取原價屋 RAM 資料...")
    ram_select = find_ram_select(soup)
    ram_results = get_ram(ram_select)
    all_results.extend(ram_results)
    print(f"共抓到 {len(ram_results)} 筆 RAM")

    print("正在抓取原價屋 SSD 資料...")
    ssd_select = find_ssd_select(soup)
    ssd_results = get_ssd(ssd_select)
    all_results.extend(ssd_results)
    print(f"共抓到 {len(ssd_results)} 筆 SSD")

    print(f"去重前總筆數：{len(all_results)}")
    all_results = duo_source(all_results)
    print(f"去重後總筆數：{len(all_results)}")

    filename = save_to_csv(all_results)
    print(f"已存成 CSV：{filename}")

if __name__ == "__main__":
    main()