import os
import json
import csv
from web3 import Web3
import sys

# Function to get XenMaps metadata
def get_xen_maps_metadata(token_id):
    try:
        metadata_tuple = xenmaps_contract.functions.getXenMapsMetadata(token_id).call()
        title, message, mintDate = metadata_tuple
        return {'token_id': token_id, 'title': title, 'message': message, 'mintDate': mintDate}
    except Exception as e:
        print(f"Error fetching metadata for token {token_id}: {e}")
        return None

def create_csv_and_json():
    data = []  # List to store data for CSV and JSON

    try:
        with open('xenmaps_messages.csv', 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['TokenID', 'Title', 'Message', 'MintDate'])

            for token_id in range(1, total_supply + 1):
                metadata = get_xen_maps_metadata(token_id)
                if metadata and "#StayXen" not in metadata['message']:
                    csv_writer.writerow([metadata['token_id'], metadata['title'], metadata['message'], metadata['mintDate']])
                    data.append(metadata)

                    # Green color definition
                    GREEN = '\033[92m'
                    RESET = '\033[0m'

                    # Print the token details with green colored values
                    print(f"Token ID: {GREEN}{metadata['token_id']}{RESET}  Xenmap: {GREEN}{metadata['title']}{RESET} Message: {GREEN}{metadata['message']}{RESET} Date Created: {GREEN}{metadata['mintDate']}{RESET}")

                # Write to the CSV file every 20 records
                if token_id % 20 == 0:
                    csv_file.flush()  # Flush the buffer to write to the file immediately

            print("CSV file created successfully.")

        # Save data as JSON with the updated file name
        with open('xenmaps_messages.json', 'w') as json_file:
            json.dump(data, json_file)

    except Exception as e:
        print(f"Error creating CSV file or JSON: {e}")

# Connect to X1 FastNet
rpc_url = 'https://x1-fastnet.infrafc.org'
w3 = Web3(Web3.HTTPProvider(rpc_url))

if not w3.is_connected():
    print("Failed to connect to X1 FastNet")
    exit()

# Load ABIs
with open('xenmapsABI.json', 'r') as file:
    xenmaps_abi = json.load(file)

# Contract address
xenmaps_address = '0x53BE48059b5999d032d0EFbeDe4dcDd637fC5Ec7'

# Create contract instance
xenmaps_contract = w3.eth.contract(address=xenmaps_address, abi=xenmaps_abi)

# Get total supply
try:
    total_supply = xenmaps_contract.functions.totalSupply().call()
except Exception as e:
    print(f"Error fetching total supply from the contract: {e}")
    exit()

# Run CSV and JSON creation
create_csv_and_json()

sys.exit(0)  # Exit gracefully with a success code
