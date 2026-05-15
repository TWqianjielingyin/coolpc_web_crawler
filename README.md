## 專案簡介

本專案用於爬取原價屋估價頁面的硬體價格資料，目前支援 CPU、主機板、GPU、RAM、SSD 等類別。
爬取後會將資料整理成 CSV，方便後續匯入資料庫或提供前端查詢使用。

### 快速開始

使用uv
在windows powershell安裝uv

```shell
on windows
$ powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

on linux / mac os
$ curl -LsSf https://astral.sh/uv/install.sh | sh
```

安裝python 3.12

```shell
$ uv python install 3.12
```

進入你的專案

```shell
$ cd your-project-folder
```

同步虛擬環境

```shell
$ uv sync
```

開始爬蟲

```shell
$ uv run main.py
```

### 輸出結果
- 輸出格式為csv檔案
- 內容包含 `類別(category)` | `品牌(brand)` | `型號(model)` | `規格(product)` | `價格(price)` | `source_key`
- 範例 CPU | Intel | Core Ultra | Intel Core Ultra 7 270K Plus | 12500 | cpu_intel_core_ultra_7_270k_plus

### 抓取方式
- 關鍵字通常會寫在各類別的 `*_INCLUDE` 清單中
- CPU、MotherBoard、GPU 主要採用「切除不需要的描述」來取得完整型號
- RAM、SSD 主要採用「抓取規格並重新組合」來取得完整型號
- source_key = 型號(model) + 規格(product)

### 資料合併規則

- 相同型號會以 `source_key` 判斷。
- 相同 `source_key` 的資料目前會保留價格較高者。
- 目前不會細分搭機價、裝機價、含散熱片、特殊組合價等不同價格類型。

### 可能限制

- 如果原價屋頁面格式改變，爬蟲可能需要調整。
- 如果出現新的命名方式、規格或型號，可能無法第一時間正確抓取。
- 商品名稱清理是依照目前觀察到的命名規則設計，仍可能有誤判情況。

### 開源模式
本專案採 MIT License
