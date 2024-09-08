import streamlit as st
import base64
import requests
import json
from PIL import Image
from io import BytesIO

prompt = """You are given an screenshot of an app. The image may include one or more of the following features (You are supposed to work with only these features):

1. Source, Destination, and Date Selection: User chooses the From (Start), To (End), and Date of Journey.
2. Bus Selection: User selects a bus and can filter and sort timings.
3. Seat Selection: An interactive seat map allowing users to pick their preferred seat, with filters for price and availability.
4. Pick-up and Drop-off Point Selection: User chooses Boarding and Dropping Points.
5. Offers: A dedicated section or pop-up displaying current discounts, deals, or promotional offers that can be applied to their booking.
6. Filters: Dynamic filtering and sorting options that appear during the Bus or Seat Selection process, allowing users to refine choices based on criteria like timing, price etc.
7. Bus Information: Any section providing comprehensive information about the bus, including amenities, real photos, and user reviews to help users make an informed choice.

Please provide a comprehensive, step-by-step guide specifically for testing the features visible in the image. For each visible feature, include the following details in the test cases:

- Description: What the test case is about.

- Pre-conditions: What needs to be set up before testing.

- Testing Steps: Clear instructions on how to perform the test.

- Expected Result: What should happen if the feature works correctly.

You are not allowed to take any assumptions or use any knowledge of the app outside of what is seen in the screenshot. Focus solely on the features that are present .
"""

url = "http://localhost:11434/api/chat"
def get_base64_encoded_image(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    encoded_string = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return encoded_string

st.title("RedBus App Test Cases Generator")
optional_context = st.text_area("Optional Context", "")
uploaded_images = st.file_uploader("Upload screenshots", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
final_result = {}
img_no = 0

if st.button("Describe Testing Instructions"):
    if uploaded_images:
        results = ""
        faults = 0
        if optional_context:
            prompt += "\n\n" + optional_context

        img_lst = []
        for image in uploaded_images:
            img_no += 1
            encoded_image = get_base64_encoded_image(Image.open(image))
            img_lst.append(encoded_image)
        
        data = {
            "model": "llama2",
            "messages": [
                {"role": "user", "content": f"Image(s): {img_lst}, Text: {prompt}"}
            ]
        }
            
        response = requests.post(url, json=data)
        json_strings = response.text.split('\n')
        for json_str in json_strings:
            try:
                chunk_json = json.loads(json_str)
                if 'message' in chunk_json and 'content' in chunk_json['message']:
                    results += chunk_json['message']['content']
            except json.JSONDecodeError:
                faults += 1

        st.write(results)
        # final_result[img_no] = results
    else:
        st.error("Please upload at least one image.")

# if img_no > 0:
#     st.write("### Generated Testing Instructions:")
#     for img_no, result in final_result.items():
#         st.write(result)
#         st.write("----")
