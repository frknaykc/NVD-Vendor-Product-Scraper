import requests
import csv
import time

# NVD API temel URL
url = "https://services.nvd.nist.gov/rest/json/cves/2.0"

def fetch_cve_data(start_index=0, max_results=2000):
    """ NVD API'den CVE verilerini çekme """
    params = {
        'resultsPerPage': 2000,  # Sayfa başına maksimum sonuç sayısı
        'startIndex': start_index
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"API Error: {response.status_code}")
        return None

def process_cve_data(cve_data):
    """ CVE verilerini işleme ve vendor/product bilgilerini ayıklama """
    vendors = set()
    vendor_product_map = {}
    
    for cve_item in cve_data['vulnerabilities']:
        cve = cve_item.get('cve', {})
        configurations = cve.get('configurations', [])
        
        if not configurations:
            # Eğer 'configurations' yoksa, 'affected' listesini kontrol et
            affected = cve.get('affected', [])
            for item in affected:
                vendor_name = item.get('vendor', '')
                product_name = item.get('product', {}).get('name', '')
                
                if vendor_name and product_name:
                    vendors.add(vendor_name)
                    if vendor_name in vendor_product_map:
                        vendor_product_map[vendor_name].add(product_name)
                    else:
                        vendor_product_map[vendor_name] = {product_name}
        else:
            for config in configurations:
                for node in config.get('nodes', []):
                    for cpe_match in node.get('cpeMatch', []):
                        cpe_uri = cpe_match.get('criteria', '')
                        parts = cpe_uri.split(':')
                        if len(parts) > 4:
                            vendor_name = parts[3]
                            product_name = parts[4]
                            
                            vendors.add(vendor_name)
                            if vendor_name in vendor_product_map:
                                vendor_product_map[vendor_name].add(product_name)
                            else:
                                vendor_product_map[vendor_name] = {product_name}
    
    return vendors, vendor_product_map

def save_vendors_to_csv(vendors, filename="vendors.csv"):
    """ Vendor bilgilerini CSV dosyasına kaydetme """
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Vendor'])
        for vendor in vendors:
            writer.writerow([vendor])

def save_products_to_csv(vendor_product_map, filename="products.csv"):
    """ Product bilgilerini CSV dosyasına kaydetme ve vendor-product eşleştirmesini yapma """
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Vendor', 'Product'])
        for vendor, products in vendor_product_map.items():
            for product in products:
                writer.writerow([vendor, product])

def main():
    all_vendors = set()
    all_vendor_product_map = {}
    total_results = 0
    start_index = 0

    while True:
        print(f"Fetching data starting from index {start_index}...")
        cve_data = fetch_cve_data(start_index)

        if cve_data:
            total_results = cve_data.get('totalResults', 0)
            vulnerabilities = cve_data.get('vulnerabilities', [])
            
            if not vulnerabilities:
                break

            vendors, vendor_product_map = process_cve_data({'vulnerabilities': vulnerabilities})
            
            all_vendors.update(vendors)
            for vendor, products in vendor_product_map.items():
                if vendor in all_vendor_product_map:
                    all_vendor_product_map[vendor].update(products)
                else:
                    all_vendor_product_map[vendor] = products

            start_index += len(vulnerabilities)
            print(f"Processed {start_index} out of {total_results} results")

            if start_index >= total_results:
                break

            # API rate limit'e uymak için bekleme
            time.sleep(6)
        else:
            print("Failed to fetch data. Exiting.")
            break

    # Vendor bilgilerini CSV dosyasına kaydet
    save_vendors_to_csv(all_vendors)

    # Product bilgilerini ve eşleştirmeyi CSV dosyasına kaydet
    save_products_to_csv(all_vendor_product_map)

    print(f"Total vendors: {len(all_vendors)}")
    print(f"Total vendor-product pairs: {sum(len(products) for products in all_vendor_product_map.values())}")

if __name__ == '__main__':
    main()
