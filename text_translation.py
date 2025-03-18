from dotenv import load_dotenv
import os
import requests, json

 # import namespaces
from azure.ai.translation.text import *
from azure.ai.translation.text.models import InputTextItem

def translate_text(inputText, targetLanguage):
    global translator_endpoint
    global cog_key
    global cog_region

    try:
        # Get Configuration Settings
        load_dotenv()
        cog_key = os.getenv('COG_SERVICE_KEY')
        cog_region = os.getenv('COG_SERVICE_REGION')
         # Create client using endpoint and key
        credential = TranslatorCredential(cog_key, cog_region)
        client = TextTranslationClient(credential)  

         # Translate text

        input_text_elements = [InputTextItem(text=inputText)]
        translationResponse = client.translate(content=input_text_elements, to=[targetLanguage])
        translation = translationResponse[0] if translationResponse else None
        if translation:
            sourceLanguage = translation.detected_language
            for translated_text in translation.translations:
                print(f"'{inputText}' was translated from {sourceLanguage.language} to {translated_text.to} as '{translated_text.text}'.")
        return translated_text.text   
                
    except Exception as ex:
        print(ex)
    


if __name__ == "__main__":
    translate_text("who are you", 'hi')