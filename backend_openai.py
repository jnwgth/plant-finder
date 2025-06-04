from openai import OpenAI
import base64

OPENAI_API_KEY = 'your_api_key'
PROJECT_ID = 'your_project_id'
 
# Back-End
class PlantFinder:

    def __init__(self, api_key, project_id):
        self.api_key = api_key
        self.project_id = project_id
        self.user_input = "test"

        self.client = OpenAI(
                    api_key=OPENAI_API_KEY,
                    base_url="https://generativelanguage.googleapis.com/v1beta/openai/")


    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

 
    def get_response(self, image_path):

        base64_image = self.encode_image(image_path)

        prompt = "Identify this plant."

        response = self.client.chat.completions.create(
            model="gemini-2.0-flash",
            messages=[
                {
                  "role": "user",
                  "content": [
                    {
                        "type": "text",
                        "text": f"{prompt}",
                    },
                    {   
                        "type": "image_url",
                        "image_url": {
                        "url":  f"data:image/jpeg;base64,{base64_image}"
                        },
                    },
                  ],
                }
              ],
            )

        return response.choices[0].message.content


if __name__ == "__main__":
    plantfinder = PlantFinder(api_key=OPENAI_API_KEY, project_id=PROJECT_ID)
    plant_info = plantfinder.get_response("plant.jpg")

    if plant_info:
        print("Plant Information:\n")
    else:
        print("Failed to retrieve plant information.")
        plant_info = "No information available."

    print(f"{plant_info}\n")

