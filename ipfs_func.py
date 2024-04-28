import ipfshttpclient
from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO
openapi_client = OpenAI()

# Configuration for ipfs.io
ipfs_gateway_url = '/ip4/127.0.0.1/tcp/5001'

def upload_file_to_ipfs(client, file_path):
    """
    Uploads a file to IPFS and returns the file's hash.
    """
    res = client.add(file_path)
    return res['Hash']

def publish_to_ipns(client, ipfs_hash, key=None):
    """
    Publishes an IPFS hash to IPNS and returns the IPNS address.
    If this fails due to gateway limitations, you may need to use another service.
    """
    try:
        res = client.name.publish(ipfs_hash, key=key)
        return res['Name']
    except Exception as e:
        print(f"Error publishing to IPNS: {e}")
        return None

def build_dyanmic_nft ():
    url = "http://localhost:3999/extended/v1/address/ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM/transactions?limit=10&offset=0"

    payload = {}
    headers = {
    'Accept': 'application/vnd.github.inertia-preview+json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    txs_list = []
    txs = response.json()['results']
    for tx in txs:
        txs_list.append(tx['tx_id'])

    def generate_image(prompt):
        """
        Generates an image from a text prompt using OpenAI's DALL-E API.
        """
        response = openapi_client.images.generate(
            model="dall-e-3",  # Adjust as necessary based on the available model
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )
        image_url = response.data[0].url

        return image_url

    def download_image(url, filename):
        """
        Downloads an image from a URL and saves it to a local file.
        """
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
        image.save(filename)

    def create_combined_prompt(transactions):
        """
        Creates a combined creative prompt from a list of blockchain transactions.
        """
        combined_details = ', '.join(transactions)  # Combining transaction details into a single string
        return f"Artistic, abstract representation of multiple Bitcoin transactions involving: {combined_details}"
    
    combined_prompt = create_combined_prompt(txs_list)
    image_url = generate_image(combined_prompt)
    download_image(image_url, "combined_bitcoin_transactions.png")


def main():
    # Connect to the ipfs.io IPFS gateway
    build_dyanmic_nft()
    with ipfshttpclient.connect(ipfs_gateway_url) as client:
        # File to be uploaded
        file_path = 'combined_bitcoin_transactions.png'
        
        # Upload file
        ipfs_hash = upload_file_to_ipfs(client, file_path)
        print(f'IPFS hash: {ipfs_hash}')
        
        # Attempt to publish to IPNS
        ipns_address = publish_to_ipns(client, ipfs_hash, "self")
        if ipns_address:
            print(f'IPNS address: {ipns_address}')
        else:
            print("IPNS publication failed or not supported by the gateway.")

if __name__ == '__main__':
    main()
