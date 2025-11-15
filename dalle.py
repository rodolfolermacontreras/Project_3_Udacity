# dalle.py

import os
from openai import AzureOpenAI
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
        # Initialize the Azure OpenAI client for DALL-E
        client = AzureOpenAI(
            api_key=config.DALLE_API_KEY,
            api_version=config.DALLE_API_VERSION,
            azure_endpoint=config.DALLE_ENDPOINT
        )
        
        # Call the DALL-E model to generate an image
        result = client.images.generate(
            model=config.DALLE_DEPLOYMENT,
            prompt=prompt,
            n=1,  # Number of images to generate
            size="1024x1024"  # Image size
        )
        
        # Get the image URL from the response
        image_url = result.data[0].url
        
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
