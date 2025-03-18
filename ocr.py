import gradio as gr
import os
import tkinter as tk
from tkinter import filedialog
import threading
from dotenv import load_dotenv
import os
import time
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt

from text_translation import translate_text

# Import namespaces
# import namespaces
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential


LANGUAGES = {'English':'en',
             'Spanish':'es',
             "German":'de',
             'Chinese':'zh-Hans',
             'Japanese':'ja',
             'French':'fr',
             'Italian':'it',
             'Arabic':'ar',
             'Tamil':'ta',
             "Malayalam":'ml',
             'Kannada':'kn',
             'Telugu':'te',
             'Hindi':'hi',
            
             }

# EXTRACTED_TEXT = ""

load_dotenv()
ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
ai_key = os.getenv('AI_SERVICE_KEY')

# Authenticate Azure AI Vision client
# Authenticate Azure AI Vision client
cv_client = ImageAnalysisClient(
    endpoint=ai_endpoint,
    credential=AzureKeyCredential(ai_key)
)

def GetTextRead(image_file):
    print('\n')

    # Open image file
    with open(image_file, "rb") as f:
            image_data = f.read()

    # Use Analyze image function to read text in image
    # Use Analyze image function to read text in image
    result = cv_client.analyze(
        image_data=image_data,
        visual_features=[VisualFeatures.READ]
    )

    # Display the image and overlay it with the extracted text
    if result.read is not None:
        print("\nText:")# Prepare image for drawing
    image = Image.open(image_file)
    fig = plt.figure(figsize=(image.width/100, image.height/100))
    plt.axis('off')
    draw = ImageDraw.Draw(image)
    color = 'cyan'
    sentence = ''
    for line in result.read.blocks[0].lines:
        # Return the text detected in the image
        # Return the text detected in the image
        print(f"  {line.text}")    
        sentence += " "+ line.text
        # drawLinePolygon = True

        # r = line.bounding_polygon
        # bounding_polygon = ((r[0].x, r[0].y),(r[1].x, r[1].y),(r[2].x, r[2].y),(r[3].x, r[3].y))

        # Return the position bounding box around each line
        # Return the position bounding box around each line
        # print("   Bounding Polygon: {}".format(bounding_polygon))

        # # Return each word detected in the image and the position bounding box around each word with the confidence level of each word
        # # Return each word detected in the image and the position bounding box around each word with the confidence level of each word
        # for word in line.words:
        #     r = word.bounding_polygon
        #     bounding_polygon = ((r[0].x, r[0].y),(r[1].x, r[1].y),(r[2].x, r[2].y),(r[3].x, r[3].y))
        #     print(f"    Word: '{word.text}', Bounding Polygon: {bounding_polygon}, Confidence: {word.confidence:.4f}")# Draw word bounding polygon
        # drawLinePolygon = False
        # draw.polygon(bounding_polygon, outline=color, width=3)

        # Draw line bounding polygon
        # if drawLinePolygon:
        #     draw.polygon(bounding_polygon, outline=color, width=3)

        #     # Save image
        #     plt.imshow(image)
        #     plt.tight_layout(pad=0)
        #     outputfile = 'text.jpg'
        #     fig.savefig(outputfile)
        #     print('\n  Results saved in', outputfile)
    return sentence

def process_image(file):
    global image_path  # Access the global variable to store the file path

    if file is None:
        image_path = ""
    else:
        # Save the image path to the variable
        image_path = file.name
    print(image_path)
        # Display the image and store the path
    global EXTRACTED_TEXT
    EXTRACTED_TEXT = GetTextRead(image_path)
    return file, EXTRACTED_TEXT

def dd_change(dropdown):
    print(dropdown)
    print(EXTRACTED_TEXT)
    translated_text = translate_text(EXTRACTED_TEXT, LANGUAGES[dropdown])
    return translated_text
# Create the Gradio interface
with gr.Blocks(title="Folder Selector") as app:


    gr.Markdown("# Folder Selector")
    gr.Markdown("Select a folder using the picker below.")
    # with gr.Row():
    #     folder_input = gr.Textbox(label="Folder Path", interactive=False)
    #     browse_btn = gr.Button("BROWSE")
    file_input = gr.File(label="Upload Image", file_types=["image"], height=100)
    image_display = gr.Image(label="Selected Image", type="pil", height=400, width=700)
    with gr.Row():
        path_text = gr.Textbox(label="Extracted Text" ,interactive=False)
        # dropdown = gr.Dropdown(label="Select Language", choices=["English","Tamil"], elem_id="dropdown")
        dropdown = gr.Dropdown(label="Select Language", choices=list(LANGUAGES.keys()), elem_id="dropdown")
    # browse_btn.click(fn=process_directory, outputs=[folder_input,label])
    translated_text = gr.Textbox(label="Translated Text", interactive=False)
    file_input.change(fn=process_image, inputs=file_input, outputs=[image_display,path_text])
    dropdown.change(fn=dd_change, inputs = dropdown, outputs=[translated_text])

# Launch the app
if __name__ == "__main__":
    app.launch()
