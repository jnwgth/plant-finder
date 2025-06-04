import google.generativeai as genai
 
API_KEY = 'your_api_key'
PROJECT_ID = 'your_project_id'
 
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
        self.model = genai.GenerativeModel('gemini-2.0-flash',
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
    plantfinder = PlantFinder(api_key=API_KEY, project_id=PROJECT_ID)
    plant_info = plantfinder.get_response("plant.jpg")

    if plant_info:
        print("Plant Information:\n")
    else:
        print("Failed to retrieve plant information.")
        plant_info = "No information available."

    print(plant_info)

