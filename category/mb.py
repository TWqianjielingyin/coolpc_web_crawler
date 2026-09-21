import re

MB_INCLUDE = [
    "H610", "B760", "Z790", "H810", "B860", "Z890",
    "A520", "B550", "A620", "B650E", "B650", "B840", "B850", "X870E", "X870"
]
MB_EXCLUDE = [
    "WS", "AI TOP"
]

Brand_MAP = {
        "華碩": "ASUS",
        "微星": "MSI",
        "技嘉": "GIGABYTE",
        "華擎": "ASRock",
    }

def name_wanted(text):
    lower_name = text.lower()
    for keyword in MB_EXCLUDE:
        if keyword.lower() in lower_name:
            return False
    for keyword in MB_INCLUDE:
        if keyword.lower() in lower_name:
            return True

    return False

def replace_brand(text):
    for zh_brand, en_brand in sorted(Brand_MAP.items(), key=lambda x: len(x[0]), reverse=True):
        text = text.replace(zh_brand, en_brand)

    return text.strip()

def get_brand(text):
    product = text
    if product.startswith("ASUS"):
        brand = "ASUS"
        model = get_model(product)
        return brand, model, product
    if product.startswith("MSI"):
        brand = "MSI"
        model = get_model(product)
        return brand, model, product
    if product.startswith("GIGABYTE"):
        brand = "GIGABYTE"
        model = get_model(product)
        return brand, model, product
    if product.startswith("ASRock"):
        brand = "ASRock"
        model = get_model(product)
        return brand, model, product

    return "Unknown", "Unknown", product
def get_model(text):
    models = [
        "H610", "B760", "Z790", "H810", "B860", "Z890",
        "A520", "B550", "A620", "B650E", "B650", "B840", "B850", "X870E", "X870"
    ]
    for model in models:
        if model in text:
            return model
    return "Unknown"

def drop_leading_square_brackets(text):
    if re.match(r"^\s*[\[［][^\]］]*[\]］]", text):
        return ""
    return text
def extract_braced_product(text):
    match = re.search(r"[{｛]([^{}｛｝]+)[}｝]", text)
    if match:
        return match.group(1).strip()
    return text

def get_product(text):
    name = drop_leading_square_brackets(text)
    name = extract_braced_product(name)
    name = re.split(r"\s*,?\s*\$", name)[0]
    name = name.split("(")[0]
    name = re.sub(r"\s+", " ", name).strip()
    return name
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

def get_mb(select):
    results = []
    options = select.find_all("option")

    for option in options:
        text = option.get_text(strip=True)
        if "共有商品" in text:
            continue
        if "開學" in text:
            continue
        if text.startswith("↪") or text.startswith("❤"):
            continue

        price = get_price(text)

        text = replace_brand(text)
        name = get_product(text)

        if len(name) < 3:
            continue

        if not name_wanted(name):
            continue

        category = "MotherBoard"
        brand, model, product = get_brand(name)
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
