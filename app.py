# MealMeter prototype 
from PIL import Image
import google.generativeai as genai
import streamlit as st


# Configure Gemini API
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def get_gemini_response(input_prompt: str, image_data: list, user_input: str) -> str:
    """Get response from Gemini API"""
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_prompt, image_data[0], user_input])
    return response.text


def input_image_setup(uploaded_file):
    """Setup image data for Gemini API"""
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


def main():
    """Main function for Streamlit app"""
    st.set_page_config(
    page_title="MealMeter App",
    page_icon=":curry:",
    layout="wide",
    initial_sidebar_state="expanded"
    )
    st.header("🍛MealMeter App")

    user_input = st.text_input("Input Prompt: ", key="input")
    uploaded_file = st.file_uploader(
        "Choose an image...", type=["jpg", "jpeg", "png"])
    image = None
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_container_width=True)

    submit = st.button("See Calorie Info")

    input_prompt = """
    You are a nutrition expert. Analyze the food items in the image and provide a detailed nutritional breakdown.
    Identify each food item in the image.
    For each item, list:
    Name of the food
    Estimated calories
    Macronutrient breakdown:
    Carbohydrates (g)
    Protein (g)
    Fat (g)
    Fiber (g)
    ----
    ----
    """

    if submit:
        if uploaded_file is None:
            st.error("Please upload an image")
            return
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt, image_data, user_input)
        st.subheader("The Response is")
        st.write(response)


if __name__ == "__main__":
    main()