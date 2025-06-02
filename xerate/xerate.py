import os
import requests
import json
from google.cloud import secretmanager, storage
from datetime import datetime
from google.api_core.exceptions import NotFound, PermissionDenied, GoogleAPICallError
import logging

# Set your GCP project ID and secret name
project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
secret_id = "api-key-exchangerate"  # the name you used when creating the secret
base_currency = "HKD"
bucket_name = "xerate"

def get_api_key(project_id, secret_id):

    # Create the Secret Manager client
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version
    secret_name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"

    # Access the secret
    try: 
        response = client.access_secret_version(name=secret_name)
        secret_value = response.payload.data.decode("UTF-8").strip()
        return secret_value
 
    # Exception Handling
    except NotFound:
        logging.error(f"Secret {secret_id} not found.")
    except PermissionDenied:
        logging.error(f"Access denied to secret {secret_id}.")
    except GoogleAPICallError as e:
        logging.error(f"API error when accessing secret {secret_id}: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

    return None

def get_exchange_rate(base_currency, api_key):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"

    try:
        response = requests.get(url)
        response.raise_for_status() # Raise an exception for HTTP error responses

        data = response.json()
    
        if data.get("result") != "success":
            return f"API Error: {data.get('error-type', 'Unknown error')}"

        return data

    except requests.exceptions.RequestException as e:
        logging.error(f"HTTP Error: {e}")

    except ValueError:
        logging.error("Error: Failed to parse JSON from response")

    except Exception as e:
        logging.error(f"Unexpected error: {e}")

def upload_to_gcs(bucket_name: str, file_name: str, content: str):
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)

        # Ensure content is string (convert dict to JSON string)
        if isinstance(content, dict):
            content = json.dumps(content)
        blob.upload_from_string(content)

        logging.info(f"Uploaded {file_name} to {bucket_name}")

    except (NotFound, PermissionDenied, GoogleAPICallError, Exception) as e:
        logging.error(f"Failed to upload file to GCS: {e}")

# Main Program
def main():

    api_key = get_api_key(project_id, secret_id)

    if api_key is not None:

        now = datetime.now()
        file_name = f"EXCHANGE_RATE_{base_currency}_{now.strftime('%Y%m%d_%H%M%S')}.txt"
        logging.info(f"Exchange rate from {base_currency} - {file_name}")
        exchange_data = get_exchange_rate(base_currency, api_key)

        #exchange_data = "{'result': 'success', 'documentation': 'https://www.exchangerate-api.com/docs', 'terms_of_use': 'https://www.exchangerate-api.com/terms', 'time_last_update_unix': 1748304001, 'time_last_update_utc': 'Tue, 27 May 2025 00:00:01 +0000', 'time_next_update_unix': 1748390401, 'time_next_update_utc': 'Wed, 28 May 2025 00:00:01 +0000', 'base_code': 'HKD', 'conversion_rates': {'HKD': 1, 'AED': 0.4686, 'AFN': 8.9058, 'ALL': 11.0398, 'AMD': 49.041, 'ANG': 0.2284, 'AOA': 118.8523, 'ARS': 145.4354, 'AUD': 0.1965, 'AWG': 0.2284, 'AZN': 0.2169, 'BAM': 0.2192, 'BBD': 0.2552, 'BDT': 15.5544, 'BGN': 0.2192, 'BHD': 0.04798, 'BIF': 379.3981, 'BMD': 0.1276, 'BND': 0.1639, 'BOB': 0.8806, 'BRL': 0.7216, 'BSD': 0.1276, 'BTN': 10.8544, 'BWP': 1.7202, 'BYN': 0.4139, 'BZD': 0.2552, 'CAD': 0.1752, 'CDF': 368.6604, 'CHF': 0.1048, 'CLP': 119.9421, 'CNY': 0.9167, 'COP': 528.9451, 'CRC': 64.774, 'CUP': 3.0623, 'CVE': 12.3586, 'CZK': 2.7869, 'DJF': 22.6761, 'DKK': 0.836, 'DOP': 7.5118, 'DZD': 16.8698, 'EGP': 6.3568, 'ERN': 1.9139, 'ETB': 17.3449, 'EUR': 0.1121, 'FJD': 0.2871, 'FKP': 0.09408, 'FOK': 0.836, 'GBP': 0.09409, 'GEL': 0.3492, 'GGP': 0.09408, 'GHS': 1.3547, 'GIP': 0.09408, 'GMD': 9.2828, 'GNF': 1110.1999, 'GTQ': 0.9788, 'GYD': 26.7291, 'HNL': 3.3197, 'HRK': 0.8445, 'HTG': 16.6857, 'HUF': 45.2032, 'IDR': 2068.674, 'ILS': 0.4544, 'IMP': 0.09408, 'INR': 10.8544, 'IQD': 167.0, 'IRR': 5558.9414, 'ISK': 16.2142, 'JEP': 0.09408, 'JMD': 20.263, 'JOD': 0.09046, 'JPY': 18.2151, 'KES': 16.4923, 'KGS': 11.1518, 'KHR': 507.5065, 'KID': 0.1965, 'KMF': 55.14, 'KRW': 174.8829, 'KWD': 0.03906, 'KYD': 0.1063, 'KZT': 65.2279, 'LAK': 2770.5534, 'LBP': 11419.659, 'LKR': 38.2, 'LRD': 25.5078, 'LSL': 2.2778, 'LYD': 0.6971, 'MAD': 1.1738, 'MDL': 2.204, 'MGA': 566.3478, 'MKD': 6.9563, 'MMK': 360.5244, 'MNT': 459.1816, 'MOP': 1.03, 'MRU': 5.0751, 'MUR': 5.7701, 'MVR': 1.9728, 'MWK': 222.2682, 'MXN': 2.4536, 'MYR': 0.5383, 'MZN': 8.1451, 'NAD': 2.2778, 'NGN': 202.53, 'NIO': 4.6928, 'NOK': 1.2881, 'NPR': 17.3671, 'NZD': 0.2126, 'OMR': 0.04906, 'PAB': 0.1276, 'PEN': 0.4664, 'PGK': 0.5226, 'PHP': 7.0727, 'PKR': 35.9862, 'PLN': 0.4755, 'PYG': 1022.0743, 'QAR': 0.4644, 'RON': 0.5675, 'RSD': 13.1496, 'RUB': 10.1789, 'RWF': 185.1296, 'SAR': 0.4785, 'SBD': 1.091, 'SCR': 1.8342, 'SDG': 57.0482, 'SEK': 1.2137, 'SGD': 0.1639, 'SHP': 0.09408, 'SLE': 2.9118, 'SLL': 2911.7797, 'SOS': 72.9067, 'SRD': 4.7316, 'SSP': 589.7532, 'STN': 2.746, 'SYP': 1642.8927, 'SZL': 2.2778, 'THB': 4.1576, 'TJS': 1.3568, 'TMT': 0.4469, 'TND': 0.3804, 'TOP': 0.305, 'TRY': 4.9776, 'TTD': 0.8663, 'TVD': 0.1965, 'TWD': 3.8213, 'TZS': 344.7357, 'UAH': 5.3059, 'UGX': 465.3753, 'USD': 0.1276, 'UYU': 5.2955, 'UZS': 1630.2544, 'VES': 12.1521, 'VND': 3305.2205, 'VUV': 15.3175, 'WST': 0.3506, 'XAF': 73.5201, 'XCD': 0.3445, 'XCG': 0.2284, 'XDR': 0.09326, 'XOF': 73.5201, 'XPF': 13.3748, 'YER': 31.1137, 'ZAR': 2.2778, 'ZMW': 3.5321, 'ZWL': 3.4318}}"

        #print(f"{exchange_data}")
        upload_to_gcs(bucket_name, file_name, exchange_data)

# This run only if the script is called directly (not imported)
if __name__ == "__main__":
    main()



