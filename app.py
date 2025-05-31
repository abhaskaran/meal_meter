# MealMeter prototype - Enhanced UI
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
        image_parts = [{
            "mime_type": uploaded_file.type,
            "data": bytes_data
        }]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

def main():
    """Main function for Streamlit app"""
    st.set_page_config(
        page_title="MealMeter App",
        page_icon="🍛",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Sidebar
    with st.sidebar:
        st.title("🍴 MealMeter")
        st.markdown("A prototype app to analyze food images and provide nutritional information using AI.")
        st.markdown("---")
        st.markdown("👤 Built with Gemini API + Streamlit")
        st.markdown("📷 Upload a meal image and get a breakdown of calories & macros.")

    # Main header
    st.markdown("<h1 style='text-align: center;'>🍽️ MealMeter: AI Food Nutrition Analyzer</h1>", unsafe_allow_html=True)
    st.markdown("### 📸 Upload your meal and get detailed nutritional insights")

    # Layout in columns
    col1, col2 = st.columns([1, 2])
    with col1:
        uploaded_file = st.file_uploader("Choose a food image", type=["jpg", "jpeg", "png"])
        user_input = st.text_input("Optional description or prompt:", key="input")
        submit = st.button("🔍 Analyze Meal", use_container_width=True)

    with col2:
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="📷 Your Uploaded Meal", use_container_width=True)

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
        if not uploaded_file:
            st.error("🚫 Please upload an image first.")
            return

        with st.spinner("Analyzing image and calculating nutrition..."):
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_response(input_prompt, image_data, user_input)

        st.markdown("---")
        st.subheader("📊 Nutrition Breakdown")
        st.markdown(f"```{response}```")

if __name__ == "__main__":
    main()
