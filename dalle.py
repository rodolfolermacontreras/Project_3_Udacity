import os
import json
from urllib.parse import urljoin

import requests

import config

# Function to generate an image representing the customer complaint


def generate_image(prompt):
    """
    Generates an image based on a prompt using OpenAI's DALL-E model.

    Args:
    prompt (str): The prompt describing the image to generate.

    Returns:
    str: The path to the generated image.
    """
    try:
        # Build payload for Azure OpenAI image generation REST call
        payload = {
            "prompt": prompt,
            "n": 1,
            "size": "1024x1024"
        }

        headers = {
            "Content-Type": "application/json",
            "api-key": config.DALLE_API_KEY
        }

        base_endpoint = config.DALLE_ENDPOINT.rstrip("/")
        generate_url = f"{base_endpoint}/openai/deployments/{config.DALLE_DEPLOYMENT}/images/generations?api-version={config.DALLE_API_VERSION}"

        response = requests.post(
            generate_url,
            headers=headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()

        result = response.json()
        image_url = result["data"][0]["url"]
        
        # Download the generated image
        image_response = requests.get(image_url)
        image_response.raise_for_status()
        
        # Save the image locally
        image_path = os.path.join(config.OUTPUT_DIR, "generated_image.png")
        with open(image_path, "wb") as f:
            f.write(image_response.content)
        
        # Save the prompt used to generate the image
        prompt_path = os.path.join(config.OUTPUT_DIR, "image_prompt.txt")
        with open(prompt_path, "w", encoding="utf-8") as f:
            f.write(prompt)
        
        print(f"✓ Image generated and saved to {image_path}")
        return image_path
    
    except Exception as e:
        print(f"✗ Error during image generation: {str(e)}")
        raise
