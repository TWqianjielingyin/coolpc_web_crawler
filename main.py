import requests
from bs4 import BeautifulSoup
import re
import csv
import os
from datetime import datetime

URL = "https://www.coolpc.com.tw/evaluate.php"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "zh-TW,zh;q=0.9",
}

CPU_INCLUDE = [
    "Core Ultra", "Intel i3", "Intel i5", "Intel i7", "Intel i9",
    "AMD R5", "AMD R7", "AMD R9"
]
CPU_EXCLUDE = [
    "Xeon", "Threadripper"
]
MB_INCLUDE = [
    "H610", "B760", "Z790", "H810", "B860", "Z890",
    "A520", "B550", "A620", "B650E", "B650", "B840", "B850", "X870E", "X870"
]
MB_EXCLUDE = [
    "WS", "AI TOP"
]
RAM_INCLUDE = [
    "DDR5", "DDR4", "D5", "D4"
]
RAM_EXCLUDE = [
    "DDR3", "D3", "ECC"
]
SSD_INCLUDE = [
    "PCIe 5.0", "PCIe 4.0", "Gen5", "Gen4",
]
SSD_EXCLUDE = [
    "2230","2242",
]
GPU_INCLUDE = [
    "ARC", "RTX", "RX"
]
GPU_EXCLUDE = [
    "NVIDIA RTX", "GTX", "GT", "ARC PRO"
]

Brand_MAP = {
        "華碩": "ASUS",
        "微星": "MSI",
        "技嘉": "GIGABYTE",
        "華擎": "ASRock",
        "藍寶石": "SAPPHIRE",
        "撼訊": "PowerColor",
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

def clean_cpu_name(text):
    name = re.split(r"\s*,?\s*\$", text)[0]
    name = re.sub(r'^\[[^\]]*\]\s*', "", name)
    name = name.split("【")[0]
    name = name.split("(")[0]
    rm_word = ["雙3D", "Tray盤", "MPK", "代理", "盒"]
    for word in rm_word:
        name = name.split(word)[0]
    name = name.strip()
    return name
def cpu_wanted(name):
    lower_name = name.lower()
    for keyword in CPU_EXCLUDE:
        if keyword.lower() in lower_name:
            return False
    for keyword in CPU_INCLUDE:
        if keyword.lower() in lower_name:
            return True

    return False

def clean_mb_name(text):
    name = re.split(r"\s*,?\s*\$", text)[0]
    name = re.sub(r'^\[[^\]]*\]\s*', "", name)
    name = name.split("(")[0]
    name = re.sub(r"[\u4e00-\u9fff]+", "", name)
    name = name.strip()
    return name
def mb_wanted(name):
    lower_name = name.lower()
    for keyword in MB_EXCLUDE:
        if keyword.lower() in lower_name:
            return False
    for keyword in MB_INCLUDE:
        if keyword.lower() in lower_name:
            return True

    return False

def clean_gpu_name(text):
    name = re.split(r"\s*,?\s*\$", text)[0]
    name = re.sub(r'^\[[^\]]*\]\s*', "", name)
    name = re.sub(r"[\u4e00-\u9fff]+", "", name)
    name = re.sub(r"\[[^\]]*\]", " ", name)
    name = re.sub(r"/\s*\d+\s*PIN\b", "", name, flags=re.IGNORECASE)
    name = re.sub(r"\b[A-Z0-9-]*\s*\d{3,4}W\b.*$", "", name, flags=re.IGNORECASE)
    name = name.split("(")[0]
    name = name.split("【")[0]
    name = name.strip()
    return name
def gpu_wanted(name):
    lower_name = name.lower()
    for keyword in GPU_EXCLUDE:
        if keyword.lower() in lower_name:
            return False
    for keyword in GPU_INCLUDE:
        if keyword.lower() in lower_name:
            return True

    return False


def cpu_model(name):
    models = [
        "i3", "i5", "i7", "i9", "Core Ultra",
        "R5", "R7", "R9",
    ]
    for model in models:
        if model in name:
            return model
    return "Unknown"
def mb_model(name):
    models = [
        "H610", "B760", "Z790", "H810", "B860", "Z890",
        "A520", "B550", "A620", "B650E", "B650", "B840", "B850", "X870E", "X870"
    ]
    for model in models:
        if model in name:
            return model
    return "Unknown"
def gpu_model(name):
    models = [
        "ARC B570", "ARC B580",
        "RTX5090", "RTX5080", "RTX5070Ti", "RTX5070", "RTX5060Ti", "RTX5060", "RTX5050",
        "RTX4090", "RTX4080 SUPER", "RTX4080", "RTX4070Ti SUPER", "RTX4070Ti", "RTX4070 SUPER", "RTX4070", "RTX4060Ti", "RTX4060", "RTX4050",
        "RTX3090Ti", "RTX3090", "RTX3080Ti", "RTX3080", "RTX3070Ti", "RTX3070", "RTX3060Ti", "RTX3060", "RTX3050",
        "RX7650GRE", "RX9060XT", "RX9070GRE", "RX9070XT", "RX9070"
    ]
    for model in models:
        if model in name:
            return model
    return "Unknown"

def replace_brand(text):
    for zh_brand, en_brand in sorted(Brand_MAP.items(), key=lambda x: len(x[0]), reverse=True):
        text = text.replace(zh_brand, en_brand)

    return text.strip()
def get_cpu_brand(name):
    product = name
    if product.startswith("Intel"):
        brand = "Intel"
        model = cpu_model(product)
        return brand, model, product
    if product.startswith("AMD"):
        brand = "AMD"
        model = cpu_model(product)
        return brand, model, product

    return "Unknown", "Unknown", product
def get_mb_brand(name):
    product = name
    if product.startswith("ASUS"):
        brand = "ASUS"
        model = mb_model(product)
        return brand, model, product
    if product.startswith("MSI"):
        brand = "MSI"
        model = mb_model(product)
        return brand, model, product
    if product.startswith("GIGABYTE"):
        brand = "GIGABYTE"
        model = mb_model(product)
        return brand, model, product
    if product.startswith("ASRock"):
        brand = "ASRock"
        model = mb_model(product)
        return brand, model, product

    return "Unknown", "Unknown", product
def get_gpu_brand(name):
    product = name
    if product.startswith("ASUS"):
        brand = "ASUS"
        model = gpu_model(product)
        return brand, model, product
    if product.startswith("MSI"):
        brand = "MSI"
        model = gpu_model(product)
        return brand, model, product
    if product.startswith("GIGABYTE"):
        brand = "GIGABYTE"
        model = gpu_model(product)
        return brand, model, product
    if product.startswith("ASRock"):
        brand = "ASRock"
        model = gpu_model(product)
        return brand, model, product
    if product.startswith("Acer") or product.startswith("ACER"):
        brand = "Acer"
        model = gpu_model(product)
        return brand, model, product
    if product.startswith("ZOTAC"):
        brand = "ZOTAC"
        model = gpu_model(product)
        return brand, model, product
    if product.startswith("INNO3D"):
        brand = "INNO3D"
        model = gpu_model(product)
        return brand, model, product
    if product.startswith("SAPPHIRE"):
        brand = "SAPPHIRE"
        model = gpu_model(product)
        return brand, model, product
    if product.startswith("PowerColor"):
        brand = "PowerColor"
        model = gpu_model(product)
        return brand, model, product
    return "Unknown", "Unknown", product

def get_price(text):
    prices = re.findall(r"\$([0-9,]+)", text)
    if not prices:
        return None
    final_price = prices[-1].replace(",", "")
    return int(final_price)

def get_source_key(category, product):
    text = f"{category}_{product}"
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = text.strip("_")
    return text

def get_cpu_product(select):
    results = []
    options = select.find_all("option")

    for option in options:
        text = option.get_text(strip=True)
        if "共有商品" in text:
            continue
        if text.startswith("↪"):
            continue

        price = get_price(text)

        name = clean_cpu_name(text)

        if len(name) < 3:
            continue

        if not cpu_wanted(name):
            continue

        category = "CPU"
        brand, model, product = get_cpu_brand(name)
        source_key = get_source_key(category, product)
        results.append({
            "category": category,
            "brand": brand,
            "model": model,
            "product": product,
            "price": price,
            "source_key": source_key,
        })

    return results
def get_mb_product(select):
    results = []
    options = select.find_all("option")

    for option in options:
        text = option.get_text(strip=True)
        if "共有商品" in text:
            continue
        if text.startswith("↪"):
            continue

        price = get_price(text)

        text = replace_brand(text)
        name = clean_mb_name(text)

        if len(name) < 3:
            continue

        if not mb_wanted(name):
            continue

        category = "MotherBoard"
        brand, model, product = get_mb_brand(name)
        source_key = get_source_key(category, product)
        results.append({
            "category": category,
            "brand": brand,
            "model": model,
            "product": product,
            "price": price,
            "source_key": source_key,
        })

    return results
def get_gpu_product(select):
    results = []
    options = select.find_all("option")

    for option in options:
        text = option.get_text(strip=True)
        if "共有商品" in text:
            continue
        if text.startswith("↪") or text.startswith("❤"):
            continue

        price = get_price(text)

        text = replace_brand(text)
        name = clean_gpu_name(text)

        if len(name) < 3:
            continue

        if not gpu_wanted(name):
            continue

        category = "GPU"
        brand, model, product = get_gpu_brand(name)
        source_key = get_source_key(category, product)
        results.append({
            "category": category,
            "brand": brand,
            "model": model,
            "product": product,
            "price": price,
            "source_key": source_key,
        })

    return results

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
    cpu_results = get_cpu_product(cpu_select)
    all_results.extend(cpu_results)
    print(f"共抓到 {len(cpu_results)} 筆 CPU")

    print("正在抓取原價屋 MotherBoard 資料...")
    mb_select = find_mb_select(soup)
    mb_results = get_mb_product(mb_select)
    all_results.extend(mb_results)
    print(f"共抓到 {len(mb_results)} 筆 MotherBoard")

    print("正在抓取原價屋 GPU 資料...")
    gpu_select = find_gpu_select(soup)
    gpu_results = get_gpu_product(gpu_select)
    all_results.extend(gpu_results)
    print(f"共抓到 {len(gpu_results)} 筆 GPU")

    print(f"去重前總筆數：{len(all_results)}")
    all_results = duo_source(all_results)
    print(f"去重後總筆數：{len(all_results)}")

    filename = save_to_csv(all_results)
    print(f"已存成 CSV：{filename}")

if __name__ == "__main__":
    main()
