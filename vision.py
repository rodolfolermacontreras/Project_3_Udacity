# vision.py

import os
import base64
from openai import AzureOpenAI
from PIL import Image, ImageDraw, ImageFont
import config

# Function to describe the generated image and annotate issues


def describe_image(image_path):
    """
    Describes an image and identifies key visual elements related to the customer complaint.

    Args:
    image_path (str): Path to the image file to describe.

    Returns:
    str: A description of the image, including the annotated details.
    """
    try:
        # Initialize the Azure OpenAI client
        client = AzureOpenAI(
            api_key=config.AZURE_OPENAI_API_KEY,
            api_version=config.GPT4O_API_VERSION,
            azure_endpoint=config.AZURE_OPENAI_ENDPOINT
        )
        
        # Read and encode the image to base64
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode("utf-8")
        
        # Create a prompt for the vision model to describe the image
        response = client.chat.completions.create(
            model=config.GPT4O_DEPLOYMENT,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert at analyzing product images and identifying defects, issues, or problems. Provide a detailed description of what you see in the image, focusing on any issues, damages, or problems visible."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Please describe this image in detail, focusing on any visible issues, problems, or defects. What product is shown? What is wrong with it?"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_data}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=500
        )
        
        # Extract the description
        description = response.choices[0].message.content
        
        # Save the description to output directory
        description_path = os.path.join(config.OUTPUT_DIR, "image_description.txt")
        with open(description_path, "w", encoding="utf-8") as f:
            f.write(description)
        
        print(f"✓ Image description completed and saved to {description_path}")
        
        # Create an annotated version of the image
        annotate_image(image_path, description)
        
        return description
    
    except Exception as e:
        print(f"✗ Error during image description: {str(e)}")
        raise


def annotate_image(image_path, description):
    """
    Annotates the image with a text overlay showing the issue description.

    Args:
    image_path (str): Path to the image file.
    description (str): The description of the issue.
    """
    try:
        # Open the image
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        
        # Add a semi-transparent overlay at the bottom
        width, height = img.size
        overlay_height = 150
        
        # Create a new image for the overlay
        overlay = Image.new('RGBA', (width, overlay_height), (0, 0, 0, 180))
        img.paste(overlay, (0, height - overlay_height), overlay)
        
        # Draw text on the image
        draw = ImageDraw.Draw(img)
        
        # Truncate description if too long
        text = "ISSUE DETECTED: " + (description[:150] + "..." if len(description) > 150 else description)
        
        # Use default font
        try:
            font = ImageFont.truetype("arial.ttf", 14)
        except:
            font = ImageFont.load_default()
        
        # Draw the text
        text_position = (10, height - overlay_height + 10)
        
        # Word wrap the text
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if len(test_line) * 8 < width - 20:  # Approximate character width
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Draw each line
        y_offset = text_position[1]
        for line in lines[:5]:  # Limit to 5 lines
            draw.text((text_position[0], y_offset), line, fill=(255, 255, 0), font=font)
            y_offset += 20
        
        # Save the annotated image
        annotated_path = os.path.join(config.OUTPUT_DIR, "annotated_image.png")
        img.save(annotated_path)
        
        print(f"✓ Annotated image saved to {annotated_path}")
    
    except Exception as e:
        print(f"✗ Error during image annotation: {str(e)}")
        # Don't raise, as this is a non-critical feature


# Example Usage (for testing purposes, remove/comment when deploying):
# if __name__ == "__main__":
#     image_path = "output/generated_image.png"
#     description = describe_image(image_path)
#     print(f"Description: {description}")
