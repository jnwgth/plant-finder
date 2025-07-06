import google.generativeai as genai
from dotenv import load_dotenv
import os
 
# Back-End

class PlantFinder:
    # Model Configuration
    model_config = {
        "temperature": 0.5,  # 1.0
        "top_p": 0.99,
        "top_k": 0,
        "max_output_tokens": 4096,
    }

    def __init__(self, api_key, project_id):
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.project_id = project_id
        self.user_input = "test"
        self.model = genai.GenerativeModel('gemini-2.5-flash',
                                    generation_config=self.model_config)
 
    def get_response(self, image_path):

        with open(image_path, "rb") as img_file:
            image_bytes = img_file.read()

        prompt = "Identify this plant."

        response = self.model.generate_content(
                    [prompt, {"mime_type": "image/jpeg", "data": image_bytes}])
        
        if response._error:
            print(f"Error: {response.error.message}")
            return None
        
        return response.text
 
if __name__ == "__main__":
    load_dotenv(override=True)
    google_api_key = os.getenv("GOOGLE_API_KEY")
    plantfinder = PlantFinder(api_key=google_api_key, project_id="")
    plant_info = plantfinder.get_response("plant.jpg")

    if plant_info:
        print("Plant Information:\n")
    else:
        print("Failed to retrieve plant information.")
        plant_info = "No information available."

    print(plant_info)

