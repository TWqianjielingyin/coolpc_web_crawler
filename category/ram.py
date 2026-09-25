import re

RAM_INCLUDE = [
    "DDR5", "DDR4", "D5", "D4"
]
RAM_EXCLUDE = [
    "DDR3", "D3", "ECC", "四根"
]

BRAND_MAP = {
    "UMAX": "UMAX",

    "威剛": "ADATA",
    "XPG": "ADATA",

    "佰維": "Biwin",
    "Biwin": "Biwin",
    "Origin code": "Biwin",

    "宏碁": "Acer",
    "ACER": "Acer",
    "Acer": "Acer",

    "KLEVV": "KLEVV",
    "科賦": "KLEVV",

    "金士頓": "Kingston",
    "FURY": "Kingston",

    "十銓": "TeamGroup",
    "CREATE": "TeamGroup",

    "美光": "Micron",
    "Micron": "Micron",
    "Crucial": "Micron",

    "海盜船": "Corsair",
    "Corsair": "Corsair",

    "芝奇": "G.SKILL",
}
PRODUCT_MAP = {
    "ADATA": [
        ("XPG Lancer Blade RGB", r"DTLABR"),
        ("XPG Lancer Blade", r"DTLAB"),
        ("XPG Lancer RGB", r"DCLAR"),
        ("XPG Lancer", r"DCLA"),
        ("XPG D10", r"D10"),
        ("XPG D50 RGB", r"D50"),
        ("", r"AD5|SGN"),
    ],
    "Biwin": [
        ("Black Opal HX100", r"HX100"),
        ("Black Opal DW100 RGB", r"DW100"),
        ("Origin code Vortex RGB", r"Origin code")
    ],
    "Acer": [
        ("Predator Vesta II RGB", r"Vesta"),
        ("Predator Hera RGB", r"Hera")
    ],
    "KLEVV": [
        ("URBANE V RGB", r"URBANE"),
        ("CRAS V RGB", r"CRAS"),
        ("BOLT V", r"BOLT"),
    ],
    "Kingston": [
        ("FURY Beast RGB", r"FURY\s*Beast\s*RGB"),
        ("FURY Beast", r"FURY\s*Beast|KV4"),
        ("FURY Renegade RGB", r"Renegade"),
    ],
    "TeamGroup": [
        ("T-CREATE EXPERT", r"T[-\s]?CREATE\s*EXPERT"),
        ("T-FORCE DELTA RGB", r"DELTA"),
        ("T-FORCE VULCAN", r"VULCAN"),
        ("XTREEM", r"XTREEM"),
    ],
    "Micron": [
        ("Crucial PRO", r"Crucial\s*PRO"),
        ("Crucial", r"Crucial"),
    ],
    "Corsair": [
        ("VENGEANCE RGB", r"CMH"),
        ("VENGEANCE", r"CMK"),
        ("DOMINATOR TITANIUM RGB", r"CMP"),
    ],
    "G.SKILL": [
        ("Trident Z5 Royal Neo RGB Silver", r"TR5NS"),
        ("Trident Z5 Royal Neo RGB Gold", r"TR5NG"),
        ("Trident Z5 Royal RGB Silver", r"TR5S"),
        ("Trident Z5 Royal RGB Gold", r"TR5G"),
        ("Trident Z5 Neo RGB White", r"TZ5NRW"),
        ("Trident Z5 Neo RGB Black", r"TZ5NR"),
        ("Trident Z5 RGB Black", r"TZ5RK"),
        ("Trident Z5 RGB White", r"TZ5RW"),
        ("Ripjaws M5 Neo RGB Black", r"RM5NRK"),
        ("Ripjaws M5 Neo RGB White", r"RM5NRW"),
        ("Ripjaws M5 RGB Black", r"RM5RK"),
        ("Ripjaws M5 RGB White", r"RM5RW"),
        ("Ripjaws S5 Black", r"RS5K"),
        ("Ripjaws S5 White", r"RS5W"),
        ("Flare X5 White", r"FX5W"),
        ("Flare X5 Black", r"FX5"),
        ("Trident Z Neo", r"GTZN"),
        ("Trident Z RGB", r"GTZR"),
        ("Trident Z Royal Silver", r"GTRS"),
        ("Ripjaws V", r"GVK")
    ],
}

def name_wanted(text):
    lower_name = text.lower()
    for keyword in RAM_EXCLUDE:
        if keyword.lower() in lower_name:
            return False
    for keyword in RAM_INCLUDE:
        if keyword.lower() in lower_name:
            return True

    return False

def get_brand(text):
    lower_text = text.lower()

    for alias, brand in sorted(BRAND_MAP.items(), key=lambda x: len(x[0]), reverse=True):
        if alias.lower() in lower_text:
            return brand

    return "Unknown"
def get_model(text):
    if re.search(r"\bDDR5\b|\bD5[-\s]?\d{4,5}", text, flags=re.IGNORECASE):
        return "DDR5"

    if re.search(r"\bDDR4\b|\bD4[-\s]?\d{4,5}", text, flags=re.IGNORECASE):
        return "DDR4"
    return "Unknown"
def get_product(brand,text):
    patterns = PRODUCT_MAP.get(brand, [])

    for product_name, pattern in patterns:
        if re.search(pattern, text, flags=re.IGNORECASE):
            return product_name
    return ""
def get_nb(text):
    if "NB" in text:
        return "NB"
    return ""
def get_speed(text):
    match = re.search(r"DDR\s*[45]\s*[-/]?\s*(\d{4,5})", text, flags=re.IGNORECASE)
    if match:
        return int(match.group(1))
    match = re.search(r"\bD[45]\s*[-/]?\s*(\d{4,5})", text, flags=re.IGNORECASE)
    if match:
        return int(match.group(1))
    return ""
def get_cl(text):
    match = re.search(r"CL\s*[-:]?\s*(\d+)", text, flags=re.IGNORECASE)

    if match:
        cl = match.group(1)
        return f"CL{cl}"

    return ""
def get_capacity(text):
    match = re.search(r"(\d+)\s*G[B]?", text, flags=re.IGNORECASE)

    if match:
        return f"{match.group(1)}GB"

    return ""
def get_kit_type(capacity,text):
    if not capacity:
        return ""
    gb = int(capacity.replace("GB", ""))
    match = re.search(r"單條", text)
    if match:
        return ""

    match = re.search(r"[*xX×]\s*2", text)
    if match:
        gb = gb // 2
        return f"{gb}G×2"

    return ""
def get_color(brand,text):
    if brand == "Biwin":
        if re.search(r"黑", text):
            return "Black"
        if re.search(r"白", text):
            return "White"
        if re.search(r"銀", text):
            return "Silver"

    if brand == "Corsair" or brand == "ADATA":
        if re.search(r"黑|BK", text):
            return "Black"
        if re.search(r"白|WH", text):
            return "White"
        if re.search(r"灰", text):
            return "Gray"

    if brand == "Acer":
        if re.search(r"黑", text):
            return "Black"
        if re.search(r"銀", text):
            return "Silver"

    if brand == "KLEVV" or brand == "Kingston" or brand == "TeamGroup" or brand == "Micron":
        if re.search(r"黑", text):
            return "Black"
        if re.search(r"白", text):
            return "White"

    return ""
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

def get_product_result(brand, product, color, nb, capacity, kit_type, model, speed, cl):
    parts = []

    if brand:
        parts.append(brand)

    if product:
        parts.append(product)

    if color:
        current = " ".join(parts).lower()
        if color.lower().strip() not in current:
            parts.append(color.strip())
    if nb:
        parts.append(nb)
    if capacity:
        if kit_type:
            parts.append(f"{capacity}({kit_type})")
        else:
            parts.append(capacity)

    if model:
        if speed and cl:
            parts.append(f"{model}-{speed} {cl}")
        elif speed:
            parts.append(f"{model}-{speed}")
        else:
            parts.append(model)

    return " ".join(" ".join(parts).split())

def get_ram(select):
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

        brand = get_brand(text)
        model = get_model(text)
        product = get_product(brand,text)
        nb = get_nb(text)
        speed = get_speed(text)
        cl = get_cl(text)
        capacity = get_capacity(text)
        kit_type = get_kit_type(capacity,text)
        color = get_color(brand,text)
        price = get_price(text)

        if not name_wanted(text):
            continue

        product_result = get_product_result(
            brand=brand,
            product=product,
            color=color,
            nb=nb,
            capacity=capacity,
            kit_type=kit_type,
            model=model,
            speed=speed,
            cl=cl,
        )

        category = "RAM"
        source_key = get_source_key(category, product_result)
        results.append({
            "category": category,
            "brand": brand,
            "model": model,
            "product": product_result,
            "price": price,
            "source_key": source_key,
        })

    return results