from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO

# Your OpenAI API key
client = OpenAI()
# client.set_api_key(api_key)

def generate_image(prompt):
    """
    Generates an image from a text prompt using OpenAI's DALL-E API.
    """
    response = client.images.generate(
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

# Example usage
tx_list = ['0x90602a746a414cef5edc8887475a68e4701f43825af1b7aa05e9776fe3d864b8', '0x2f744bdfb806f52afb0ac0c04a0e13a352bd50511dd08d2bc09b55a6e12e85db']
combined_prompt = create_combined_prompt(tx_list)
print(combined_prompt)
image_url = generate_image(combined_prompt)
download_image(image_url, "combined_bitcoin_transactions.png")
