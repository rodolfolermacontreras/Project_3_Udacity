# main.py

import os
import sys
import json
from datetime import datetime

# Import functions from other modules
from whisper import transcribe_audio
from dalle import generate_image
from vision import describe_image
from gpt import classify_with_gpt
import config

# Main function to orchestrate the workflow


def create_image_prompt(transcription):
    """
    Creates a detailed prompt for image generation based on the transcription.
    
    Args:
    transcription (str): The transcribed customer complaint.
    
    Returns:
    str: A well-formatted prompt for DALL-E image generation.
    """
    # Create a descriptive prompt that focuses on the visual representation of the issue
    prompt = f"A realistic photo showing: {transcription}. Focus on showing the product and the specific issue or problem mentioned. Make it clear and detailed."
    return prompt


def print_separator(title=""):
    """Prints a visual separator for better console output."""
    print("\n" + "=" * 70)
    if title:
        print(f"  {title}")
        print("=" * 70)
    print()


def save_summary(transcription, prompt, image_path, description, classification):
    """
    Saves a complete summary of the entire workflow.
    
    Args:
    transcription (str): The transcribed audio text.
    prompt (str): The image generation prompt.
    image_path (str): Path to the generated image.
    description (str): The image description.
    classification (dict): The classification results.
    """
    summary = {
        "timestamp": datetime.now().isoformat(),
        "workflow_steps": {
            "1_transcription": transcription,
            "2_image_prompt": prompt,
            "3_generated_image_path": image_path,
            "4_image_description": description,
            "5_classification": classification
        }
    }
    
    summary_path = os.path.join(config.OUTPUT_DIR, "workflow_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Complete workflow summary saved to {summary_path}")


def main(audio_file_path=None):
    """
    Orchestrates the workflow for handling customer complaints.
    
    Steps include:
    1. Transcribe the audio complaint.
    2. Create a prompt from the transcription.
    3. Generate an image representing the issue.
    4. Describe the generated image.
    5. Annotate the reported issue in the image.
    6. Classify the complaint into a category/subcategory pair.
    
    Args:
    audio_file_path (str): Path to the audio file. If None, will look for files in audio directory.
    
    Returns:
    dict: A dictionary containing all results from the workflow.
    """
    try:
        print_separator("CUSTOMER COMPLAINT CLASSIFICATION SYSTEM")
        print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Step 1: Find and transcribe the audio complaint
        print_separator("STEP 1: Audio Transcription")
        
        if audio_file_path is None:
            # Look for audio files in the audio directory
            audio_files = [f for f in os.listdir(config.AUDIO_DIR) 
                          if f.endswith(('.mp3', '.wav', '.m4a', '.ogg')) and f != '.gitkeep']
            
            if not audio_files:
                print("✗ No audio files found in the 'audio' directory.")
                print("  Please place an audio file (.mp3, .wav, .m4a, or .ogg) in the 'audio' folder.")
                return None
            
            audio_file_path = os.path.join(config.AUDIO_DIR, audio_files[0])
            print(f"Using audio file: {audio_file_path}")
        
        if not os.path.exists(audio_file_path):
            print(f"✗ Audio file not found: {audio_file_path}")
            return None
        
        transcription = transcribe_audio(audio_file_path)
        print(f"\nTranscription Result:\n{transcription}\n")
        
        # Step 2: Create a prompt from the transcription
        print_separator("STEP 2: Creating Image Generation Prompt")
        
        prompt = create_image_prompt(transcription)
        print(f"Generated Prompt:\n{prompt}\n")
        
        # Step 3: Generate an image based on the prompt
        print_separator("STEP 3: Generating Image with DALL-E 3")
        
        image_path = generate_image(prompt)
        print(f"\nImage generated successfully!\n")
        
        # Step 4: Describe the generated image
        print_separator("STEP 4: Analyzing Image with GPT-4o Vision")
        
        description = describe_image(image_path)
        print(f"\nImage Description:\n{description}\n")
        
        # Step 5: Image annotation is handled within describe_image()
        print_separator("STEP 5: Image Annotation")
        print("✓ Annotated image created with issue highlight\n")
        
        # Step 6: Classify the complaint based on the image description
        print_separator("STEP 6: Classifying Complaint")
        
        classification = classify_with_gpt(transcription, description)
        print(f"\nClassification Results:")
        print(f"  Category: {classification['category']}")
        print(f"  Subcategory: {classification['subcategory']}")
        print(f"  Reasoning: {classification['reasoning']}\n")
        
        # Save complete summary
        print_separator("WORKFLOW COMPLETE")
        save_summary(transcription, prompt, image_path, description, classification)
        
        print("\n📁 All intermediate results saved in the 'output' directory:")
        print("   - transcription.txt")
        print("   - image_prompt.txt")
        print("   - generated_image.png")
        print("   - image_description.txt")
        print("   - annotated_image.png")
        print("   - classification.json")
        print("   - classification.txt")
        print("   - workflow_summary.json")
        
        print_separator()
        print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("✓ Customer complaint processed successfully!\n")
        
        # Return all results
        return {
            "transcription": transcription,
            "prompt": prompt,
            "image_path": image_path,
            "description": description,
            "classification": classification
        }
    
    except Exception as e:
        print(f"\n✗ Error in workflow: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


# Example Usage
if __name__ == "__main__":
    # Check if an audio file path was provided as command line argument
    if len(sys.argv) > 1:
        audio_path = sys.argv[1]
        main(audio_path)
    else:
        # Run with default audio file search
        main()
