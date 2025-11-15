# whisper.py

import os
from openai import AzureOpenAI
import config

# Function to transcribe customer audio complaints using the Whisper model


def transcribe_audio(audio_file_path):
    """
    Transcribes an audio file into text using OpenAI's Whisper model.

    Args:
    audio_file_path (str): Path to the audio file to transcribe.

    Returns:
    str: The transcribed text of the audio file.
    """
    try:
        # Initialize the Azure OpenAI client
        client = AzureOpenAI(
            api_key=config.AZURE_OPENAI_API_KEY,
            api_version=config.WHISPER_API_VERSION,
            azure_endpoint=config.AZURE_COGNITIVE_ENDPOINT
        )
        
        # Open and read the audio file
        with open(audio_file_path, "rb") as audio_file:
            # Call the Whisper model to transcribe the audio
            transcription = client.audio.transcriptions.create(
                model=config.WHISPER_DEPLOYMENT,
                file=audio_file
            )
        
        # Extract the transcribed text
        transcribed_text = transcription.text
        
        # Save the transcription to output directory
        output_path = os.path.join(config.OUTPUT_DIR, "transcription.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(transcribed_text)
        
        print(f"✓ Audio transcription completed and saved to {output_path}")
        return transcribed_text
    
    except Exception as e:
        print(f"✗ Error during audio transcription: {str(e)}")
        raise

# Example Usage (for testing purposes, remove/comment when deploying):
# if __name__ == "__main__":
#     audio_path = "audio/sample_complaint.mp3"
#     transcription = transcribe_audio(audio_path)
#     print(f"Transcription: {transcription}")
