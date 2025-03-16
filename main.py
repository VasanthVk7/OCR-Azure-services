#pip install azure-ai-vision azure-ai-translation
from azure.ai.vision import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.text import TextTranslationClient
import os

# Azure credentials (replace these with your actual credentials)
COMPUTER_VISION_KEY = "YOUR_COMPUTER_VISION_KEY"
COMPUTER_VISION_ENDPOINT = "YOUR_COMPUTER_VISION_ENDPOINT"
TRANSLATOR_KEY = "YOUR_TRANSLATOR_KEY"
TRANSLATOR_ENDPOINT = "https://api.cognitive.microsofttranslator.com"

# Initialize clients for both services
def get_clients():
    # Image Analysis client for OCR
    vision_client = ImageAnalysisClient(
        endpoint=COMPUTER_VISION_ENDPOINT,
        credential=AzureKeyCredential(COMPUTER_VISION_KEY)
    )
    
    # Text Translation client
    translation_client = TextTranslationClient(
        endpoint=TRANSLATOR_ENDPOINT,
        credential=AzureKeyCredential(TRANSLATOR_KEY)
    )
    
    return vision_client, translation_client

# Perform OCR to extract text from the image
def ocr_image(image_path, vision_client):
    with open(image_path, "rb") as image_file:
        analysis_result = vision_client.read_in_stream(image_file, raw=True)

    # Wait for the OCR operation to complete
    result = analysis_result.result()

    # Extract text from the result
    text = ""
    for page_result in result.analyze_result.read_results:
        for line in page_result.lines:
            text += line.text + "\n"
    
    return text

# Translate text using the Translator client
def translate_text(text, target_language, translation_client):
    response = translation_client.translate(
        content=text,
        to=[target_language]
    )
    
    # Extract translated text
    translated_text = ""
    for translation in response:
        translated_text = translation.text

    return translated_text

# Main function to process the image and translate the extracted text
def process_image_and_translate(image_path, target_language):
    # Get the clients for both services
    vision_client, translation_client = get_clients()
    
    # Perform OCR to extract text
    extracted_text = ocr_image(image_path, vision_client)
    
    if not extracted_text:
        return "No text found in the image."

    # Translate the extracted text
    translated_text = translate_text(extracted_text, target_language, translation_client)
    return translated_text

# Example usage
if __name__ == "__main__":
    image_path = "path_to_your_image.jpg"  # Replace with the path to your image
    target_language = "es"  # Spanish
    translated_text = process_image_and_translate(image_path, target_language)
    print("Translated Text:", translated_text)
