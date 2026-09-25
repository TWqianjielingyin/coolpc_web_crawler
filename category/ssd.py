import re

SSD_INCLUDE = [
    "PCIe 4.0", "PCIe4.0", "PCI-E 4.0", "PCIe 5.0", "PCIe5.0", "PCI-E 5.0",
    "Gen4", "Gen 4", "Gen5", "Gen 5"
]

SSD_EXCLUDE = [
    "PCIe 3.0", "PCIe3.0", "PCI-E 3.0", "Gen3", "Gen 3",
    "2.5吋", "2.5\"", "2230", "2242"
]

BRAND_MAP = {
    "鎧俠": "KIOXIA",
    "KIOXIA": "KIOXIA",

    "威剛": "ADATA",
    "XPG": "ADATA",
    "ADATA": "ADATA",

    "佰維": "Biwin",
    "Biwin": "Biwin",

    "宏碁": "Acer",
    "ACER": "Acer",
    "Acer": "Acer",
    "Predator": "Acer",

    "海盜船": "Corsair",
    "Corsair": "Corsair",

    "金士頓": "Kingston",
    "Kingston": "Kingston",
    "FURY": "Kingston",

    "致態": "ZhiTai",
    "ZhiTai": "ZhiTai",

    "黑標": "WD",
    "WD": "WD",
    "Western Digital": "WD",

    "美光": "Micron",
    "Micron": "Micron",
    "Crucial": "Micron",

    "十銓": "TeamGroup",
    "TeamGroup": "TeamGroup",
    "Team Group": "TeamGroup",

    "微星": "MSI",
    "MSI": "MSI",

    "三星": "Samsung",
    "Samsung": "Samsung",

    "KLEVV": "KLEVV",
    "科賦": "KLEVV",

    "Seagate": "Seagate",
    "seagate": "Seagate",
}
PRODUCT_MAP = {
    "KIOXIA": [
        ("EXCERIA G3", r"EXCERIA G3"),
        ("EXCERIA PLUS G4", r"EXCERIA PLUS G4"),
        ("EXCERIA PLUS G3", r"EXCERIA PLUS G3"),
        ("EXCERIA BASIC", r"EXCERIA BASIC"),
    ],
    "ADATA": [
        ("XPG MARS 980Blade", r"MARS\s*980\s*Blade|MARS"),
        ("LEGEND 970", r"LEGEND\s*970"),
        ("LEGEND 960", r"LEGEND\s*960"),
        ("LEGEND 900", r"LEGEND\s*900"),
        ("LEGEND 860", r"LEGEND\s*860"),
        ("S70 BLADE", r"S70\s*BLADE|S70"),
    ],
    "Biwin": [
        ("X570 PRO", r"X570 PRO"),
        ("X570", r"X570"),
        ("NV7400", r"NV7400"),
        ("M350", r"M350"),
    ],
    "Acer": [
        ("Predator GM9000", r"GM9000"),
        ("Predator GM9", r"GM9"),
        ("FA200", r"FA200"),
        ("Predator GM7000", r"GM7000"),
        ("Predator GM7", r"GM7"),
    ],
    "Corsair": [
        ("MP700 PRO XT", r"MP700 PRO XT"),
        ("MP700 PRO", r"MP700 PRO"),
        ("MP700 ELITE", r"MP700 ELITE"),
        ("MP600 ELITE", r"MP600 ELITE"),
        ("MP600 PRO LPX", r"MP600 PRO LPX"),
        ("MP600 PRO", r"MP600 PRO"),
    ],
    "Kingston": [
        ("FURY Renegade G5", r"FURY Renegade G5"),
        ("NV3", r"NV3"),
        ("KC3000", r"KC3000"),
    ],
    "ZhiTai": [
        ("TiPlus 9100", r"TiPlus 9100"),
        ("TiPro 9000", r"TiPro9000"),
        ("e7", r"e7"),
        ("Ti 600", r"Ti600"),
        ("TiPlus 7100s", r"7100s"),
    ],
    "WD": [
        ("SN8100", r"SN8100"),
        ("SN7100", r"SN7100"),
        ("SN850X", r"SN850X"),
        ("SN770", r"SN770"),
        ("SN580", r"SN580"),
        ("SN5100", r"SN5100"),
    ],
    "Micron": [
        ("Crucial P510", r"P510"),
        ("Crucial T700", r"T700"),
        ("Crucial T705", r"T705"),
        ("Crucial T710", r"T710"),
        ("Crucial T500", r"T500"),
        ("Crucial P310", r"P310"),
        ("Crucial E100", r"E100"),
    ],
    "TeamGroup": [
        ("T-Force GC PRO", r"GC PRO"),
        ("T-Force Z540", r"Z540"),
        ("MP44L", r"MP44L"),
        ("G70 PRO", r"G70"),
    ],
    "MSI": [
        ("SPATIUM M560", r"M560"),
        ("M450 V1", r"M450"),
        ("M470 PRO", r"M470"),
        ("M480 PRO", r"M480"),
    ],
    "Samsung": [
        ("9100 PRO", r"9100\s*PRO"),
        ("990 EVO PLUS", r"990\s*EVO\s*PLUS"),
        ("990 PRO", r"990\s*PRO"),
        ("980 PRO", r"980\s*PRO"),
    ],
    "KLEVV": [
        ("CRAS C910", r"C910"),
        ("CRAS C930", r"C930"),
    ],
    "Seagate": [
        ("FireCuda 530R", r"530R"),
    ],
}

def name_wanted(text):
    lower_name = text.lower()
    for keyword in SSD_EXCLUDE:
        if keyword.lower() in lower_name:
            return False
    for keyword in SSD_INCLUDE:
        if keyword.lower() in lower_name:
            return True
    if re.search(r"FURY\s+Renegade\s+G5", text, flags=re.IGNORECASE):
        return True

    return False

def get_brand(text):
    lower_text = text.lower()

    for alias, brand in sorted(BRAND_MAP.items(), key=lambda x: len(x[0]), reverse=True):
        if alias.lower() in lower_text:
            return brand

    return "Unknown"
def get_model(text):
    upper_text = text.upper()

    if re.search(r"GEN\s*5", upper_text) or re.search(r"PCI[-\s]*E\s*5(?:\.0)?", upper_text):
        return "Gen5"
    if re.search(r"GEN\s*4", upper_text) or re.search(r"PCI[-\s]*E\s*4(?:\.0)?", upper_text):
        return "Gen4"

    if re.search(r"FURY\s+Renegade\s+G5", text, flags=re.IGNORECASE):
        return "Gen5"

    return ""
def get_product(brand,text):
    patterns = PRODUCT_MAP.get(brand, [])

    for product_name, pattern in patterns:
        if re.search(pattern, text, flags=re.IGNORECASE):
            return product_name

    return ""
def get_capacity(text):
    match = re.search(r"(\d+)\s*T[B]?(?=$|[^A-Za-z0-9])", text, flags=re.IGNORECASE)
    if match:
        return f"{match.group(1)}TB"

    match = re.search(r"(\d+)\s*G[B]?(?=$|[^A-Za-z0-9])", text, flags=re.IGNORECASE)
    if match:
        return f"{match.group(1)}GB"

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

def get_product_result(brand, product, capacity, model):
    parts = []

    if brand:
        parts.append(brand)

    if product:
        parts.append(product)

    if capacity and model:
        parts.append(f"{capacity}/{model}")
    elif capacity:
        parts.append(capacity)
    elif model:
        parts.append(model)

    return " ".join(" ".join(parts).split())

def get_ssd(select):
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
        capacity = get_capacity(text)
        price = get_price(text)

        if not name_wanted(text):
            continue

        product_result = get_product_result(
            brand=brand,
            product=product,
            capacity=capacity,
            model=model,
        )

        category = "SSD"
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