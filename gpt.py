# gpt.py

import os
import json
from openai import AzureOpenAI
import config

# Function to classify the customer complaint based on the image description


def classify_with_gpt(transcription, image_description):
    """
    Classifies the customer complaint into a category/subcategory based on the transcription 
    and image description.

    Args:
    transcription (str): The transcribed text of the customer complaint.
    image_description (str): The description of the generated image.

    Returns:
    dict: A dictionary containing the category, subcategory, and reasoning.
    """
    try:
        # Load categories from JSON file
        with open(config.CATEGORIES_FILE, "r", encoding="utf-8") as f:
            categories = json.load(f)
        
        # Create a formatted string of available categories
        categories_text = json.dumps(categories, indent=2)
        
        # Initialize the Azure OpenAI client
        client = AzureOpenAI(
            api_key=config.AZURE_OPENAI_API_KEY,
            api_version=config.GPT4O_API_VERSION,
            azure_endpoint=config.AZURE_OPENAI_ENDPOINT
        )
        
        # Create the classification prompt
        system_prompt = """You are an expert customer service classifier. Your task is to categorize customer complaints into the appropriate category and subcategory based on the complaint details.

You will be provided with:
1. The customer's original complaint (transcribed from audio)
2. A description of an image representing the issue
3. A list of available categories and subcategories

Analyze the information carefully and classify the complaint into the most appropriate category and subcategory pair."""

        user_prompt = f"""Please classify the following customer complaint:

CUSTOMER COMPLAINT:
{transcription}

IMAGE DESCRIPTION:
{image_description}

AVAILABLE CATEGORIES AND SUBCATEGORIES:
{categories_text}

Based on the complaint and image description, determine:
1. The most appropriate CATEGORY
2. The most appropriate SUBCATEGORY within that category
3. A brief explanation of why this classification was chosen

Respond in the following JSON format:
{{
    "category": "Category Name",
    "subcategory": "Subcategory Name",
    "reasoning": "Brief explanation of the classification"
}}"""

        # Call the GPT model for classification
        response = client.chat.completions.create(
            model=config.GPT4O_DEPLOYMENT,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,  # Lower temperature for more consistent classification
            max_tokens=500,
            response_format={"type": "json_object"}
        )
        
        # Extract and parse the classification result
        classification_text = response.choices[0].message.content
        classification = json.loads(classification_text)
        
        # Save the classification to output directory
        classification_path = os.path.join(config.OUTPUT_DIR, "classification.json")
        with open(classification_path, "w", encoding="utf-8") as f:
            json.dump(classification, f, indent=2)
        
        # Also save as readable text
        classification_text_path = os.path.join(config.OUTPUT_DIR, "classification.txt")
        with open(classification_text_path, "w", encoding="utf-8") as f:
            f.write(f"Category: {classification['category']}\n")
            f.write(f"Subcategory: {classification['subcategory']}\n")
            f.write(f"Reasoning: {classification['reasoning']}\n")
        
        print(f"✓ Classification completed and saved to {classification_path}")
        return classification
    
    except Exception as e:
        print(f"✗ Error during classification: {str(e)}")
        raise