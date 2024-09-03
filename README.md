# NVD Vendor-Product Scraper

This repository contains a Python script that extracts vendor and product information from the National Vulnerability Database (NVD) via their API and exports the data into CSV files.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [CSV Output](#csv-output)
- [Limitations](#limitations)
- [License](#license)

## Overview

The `NVD-Vendor-Product-Scraper` script fetches vulnerability data from the NVD API and processes it to extract vendor and product information. The results are then saved into two separate CSV files:
- `vendors.csv` containing a list of all unique vendors.
- `products.csv` containing vendor-product pairs.

## Features

- Fetches CVE data from the NVD API.
- Extracts unique vendor names.
- Extracts and maps products to their corresponding vendors.
- Exports the vendor and product data to CSV files.
- Handles large datasets by paginating through the API results.

## Requirements

- Python 3.6 or higher
- `requests` library

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/nvd-vendor-product-extractor.git
    cd nvd-vendor-product-extractor
    ```

2. Install the required Python packages:
    ```bash
    pip install requests
    ```

## Usage

1. Run the script:
    ```bash
    python nvd_vendor_product_extractor.py
    ```

2. The script will start fetching data from the NVD API and process it in chunks. Depending on the size of the data, it may take a while to complete. The script pauses for 6 seconds between API requests to comply with rate limits.

3. Once completed, the script will generate two CSV files in the current directory:
    - `vendors.csv`
    - `products.csv`

## CSV Output

- **vendors.csv**: Contains a list of unique vendor names.
    ```
    Vendor
    vendor_name1
    vendor_name2
    ...
    ```

- **products.csv**: Contains a list of vendor-product pairs.
    ```
    Vendor,Product
    vendor_name1,product_name1
    vendor_name1,product_name2
    vendor_name2,product_name1
    ...
    ```

## Limitations

- The script relies on the NVD API's data structure, which may change over time.
- API rate limits are respected with a 6-second pause between requests, but this may still result in a lengthy data retrieval process depending on the dataset size.
- The script currently processes up to 2000 results per API call, which is the maximum allowed by the NVD API.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
