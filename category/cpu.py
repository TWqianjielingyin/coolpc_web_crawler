import re

CPU_INCLUDE = [
    "Core Ultra", "Intel i3", "Intel i5", "Intel i7", "Intel i9",
    "AMD R5", "AMD R7", "AMD R9"
]
CPU_EXCLUDE = [
    "Xeon", "Threadripper"
]

def name_wanted(text):
    lower_name = text.lower()
    for keyword in CPU_EXCLUDE:
        if keyword.lower() in lower_name:
            return False
    for keyword in CPU_INCLUDE:
        if keyword.lower() in lower_name:
            return True

    return False

def get_brand(text):
    product = text
    if product.startswith("Intel"):
        brand = "Intel"
        model = get_model(product)
        return brand, model, product
    if product.startswith("AMD"):
        brand = "AMD"
        model = get_model(product)
        return brand, model, product

    return "Unknown", "Unknown", product
def get_model(text):
    models = [
        "i3", "i5", "i7", "i9", "Core Ultra",
        "R5", "R7", "R9",
    ]
    for model in models:
        if model in text:
            return model
    return "Unknown"

def extract_braced_product(text):
    match = re.search(r"[{｛]([^{}｛｝]+)[}｝]", text)
    if match:
        return match.group(1).strip()

    return text
def extract_cpu_name(text):
    patterns = [
        r"\bAMD\s+R[3579]\s+\d{4,5}[A-Z0-9]*\b",
        r"\bIntel\s+i[3579][-\s]?\d{4,5}[A-Z]{0,2}\b",
        r"\bIntel\s+Core\s+Ultra\s+[3579]\s+\d{3,4}[A-Z]{0,2}\b",
        r"\bCore\s+Ultra\s+[3579]\s+\d{3,4}[A-Z]{0,2}\b",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            name = re.sub(r"\s+", " ", match.group(0).replace("-", " ")).strip()
            if name.lower().startswith("core ultra"):
                return f"Intel {name}"
            return name

    return text
def get_product(text):
    name = extract_braced_product(text)
    name = re.split(r"\s*,?\s*\$", name)[0]
    name = name.split("【")[0]
    rm_word = ["雙3D", "Tray盤", "MPK", "代理", "盒"]
    for word in rm_word:
        name = name.split(word)[0]
    name = name.strip()
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

def get_cpu(select):
    results = []
    options = select.find_all("option")

    for option in options:
        text = option.get_text(strip=True)
        if "共有商品" in text:
            continue
        if text.startswith("↪") or text.startswith("❤"):
            continue

        price = get_price(text)

        name = get_product(text)

        if len(name) < 3:
            continue

        if not name_wanted(name):
            continue

        category = "CPU"
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

