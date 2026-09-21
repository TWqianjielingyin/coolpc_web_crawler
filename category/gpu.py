import re

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
    #acer
    }

def name_wanted(text):
    lower_name = text.lower()
    for keyword in GPU_EXCLUDE:
        if keyword.lower() in lower_name:
            return False
    for keyword in GPU_INCLUDE:
        if keyword.lower() in lower_name:
            return True

    return False

def replace_brand(text):
    for zh_brand, en_brand in sorted(Brand_MAP.items(), key=lambda x: len(x[0]), reverse=True):
        text = text.replace(zh_brand, en_brand)

    return text.strip()

def get_brand(text):
    product = text
    if product.startswith("ASUS") or product.startswith("ROG"):
        brand = "ASUS"
        model = get_model(product)
        if product.startswith("ROG"):
            product = brand + " " + product
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
    if product.startswith("Acer") or product.startswith("ACER"):
        brand = "Acer"
        model = get_model(product)
        return brand, model, product
    if product.startswith("ZOTAC"):
        brand = "ZOTAC"
        model = get_model(product)
        return brand, model, product
    if product.startswith("INNO3D"):
        brand = "INNO3D"
        model = get_model(product)
        return brand, model, product
    if product.startswith("SAPPHIRE"):
        brand = "SAPPHIRE"
        model = get_model(product)
        return brand, model, product
    if product.startswith("PowerColor"):
        brand = "PowerColor"
        model = get_model(product)
        return brand, model, product
    return "Unknown", "Unknown", product
def get_model(text):
    normalized_text = re.sub(r"\s+", "", text.upper())
    models = [
        "ARC B570", "ARC B580",
        "RTX5090", "RTX5080", "RTX5070Ti", "RTX5070", "RTX5060Ti", "RTX5060", "RTX5050",
        "RTX4090", "RTX4080 SUPER", "RTX4080", "RTX4070Ti SUPER", "RTX4070Ti", "RTX4070 SUPER", "RTX4070", "RTX4060Ti", "RTX4060", "RTX4050",
        "RTX3090Ti", "RTX3090", "RTX3080Ti", "RTX3080", "RTX3070Ti", "RTX3070", "RTX3060Ti", "RTX3060", "RTX3050",
        "RX7650GRE", "RX9060XT", "RX9070GRE", "RX9070XT", "RX9070"
    ]
    for model in models:
        normalized_model = re.sub(r"\s+", "", model.upper())
        if normalized_model in normalized_text:
            return model
    return "Unknown"

def extract_braced_product(text):
    match = re.search(r"[{｛]([^{}｛｝]+)[}｝]", text)
    if match:
        return match.group(1).strip()
    return text
def remove_chinese(text):
    text = re.sub(r"[\u3400-\u9fff]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def get_product(text):
    name = extract_braced_product(text)
    name = remove_chinese(name)
    name = re.split(r"\s*,?\s*\$", name)[0]
    name = re.sub(r"\[[^\]]*\]", " ", name)
    name = re.sub(r"/\s*\d+\s*PIN\b", "", name, flags=re.IGNORECASE)
    name = re.sub(r"\b[A-Z0-9-]*\s*\d{3,4}W\b.*$", "", name, flags=re.IGNORECASE)
    name = name.split("(")[0]
    name = name.split("【")[0]
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

def get_gpu(select):
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

        if not name_wanted(name):
            continue

        category = "GPU"
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
