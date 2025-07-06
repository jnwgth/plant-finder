import gradio as gr
from PIL import Image
from backend import PlantFinder
from dotenv import load_dotenv
import os

load_dotenv(override=True)
google_api_key = os.getenv("GOOGLE_API_KEY")
plantfinder = PlantFinder(api_key=google_api_key, project_id="")

def greet(name, image_pixels):
    print(type(image_pixels))
    print(image_pixels.shape)

    img = Image.fromarray(image_pixels)
    img.save("uploaded.jpg")
    print(img)

    plant_info = plantfinder.get_response("uploaded.jpg")

    return plant_info

demo = gr.Interface(fn=greet,
                    inputs=[
                        gr.Text(label="Plant Finder"),
                        gr.Image()
                    ],
                    outputs=gr.Text(label="Output:"))
demo.launch()
