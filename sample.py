import gradio as gr
import os
import tkinter as tk
from tkinter import filedialog
import threading


def process_image(file):
    global image_path  # Access the global variable to store the file path

    if file is None:
        image_path = ""
    else:
        # Save the image path to the variable
        image_path = file.name
    print(image_path)
        # Display the image and store the path
    return file, image_path
def dd_change(dropdown):
    print(dropdown)
    return "uvhvhv"
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
        dropdown = gr.Dropdown(label="Select Language", choices=["English","Tamil"], elem_id="dropdown")
    # browse_btn.click(fn=process_directory, outputs=[folder_input,label])
    translated_text = gr.Textbox(label="Translated Text", interactive=False)
    file_input.change(fn=process_image, inputs=file_input, outputs=[image_display,path_text])
    dropdown.change(fn=dd_change, inputs = dropdown, outputs=[translated_text])

# Launch the app
if __name__ == "__main__":
    app.launch()