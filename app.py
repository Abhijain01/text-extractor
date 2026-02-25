import streamlit as st
import pytesseract
from PIL import Image
import json
import io

# Set Tesseract Path (Manually located)
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\abhis\tesseract.exe'

# Page Config
st.set_page_config(
    page_title="Local Text Extractor",
    page_icon="📂",
    layout="centered"
)

def extract_text(image):
    try:
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        st.error(f"Error extracting text: {e}")
        st.error("Please make sure Tesseract-OCR is installed on your Windows machine.")
        return None
def main():
    st.title("📂 Local Text Extractor")
    st.markdown("Extract text from images locally using Tesseract OCR (Offline).")

    # File Upload
    uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])

    if uploaded_file is not None:
        # Display Image
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)

        if st.button("Extract Text", type="primary"):
            with st.spinner('Extracting text...'):
                text = extract_text(image)

                if text:
                    # Metrics
                    col1, col2 = st.columns(2)
                    word_count = len(text.split())
                    with col1:
                        st.metric("Word Count", word_count)
                    with col2:
                        st.metric("Mode", "Local (Tesseract)")

                    # text Display
                    st.subheader("Extracted Text")
                    st.text_area("Content", text, height=300)

                    # JSON Structure
                    result = {
                        "image_name": uploaded_file.name,
                        "extracted_text": text,
                        "line_wise_text": [line for line in text.split('\n') if line.strip()],
                        "word_count": word_count,
                        "processing_mode": "local"
                    }

                    # JSON Download
                    json_str = json.dumps(result, indent=2)
                    st.download_button(
                        label="Download JSON",
                        data=json_str,
                        file_name="extracted_text.json",
                        mime="application/json"
                    )

if __name__ == "__main__":
    main()
