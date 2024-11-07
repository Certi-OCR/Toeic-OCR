import os
import streamlit as st
from PIL import Image
from dotenv import load_dotenv
from image_processing import processImage
from text_recognization import text_ocr
from inference import image_predictions

def main():
    st.set_page_config(page_title="Toeic Extractor")
    load_dotenv()
    key = os.getenv("API_KEY")
    
    st.title("Toeic Certificate Information Extractor")
    
    file = st.file_uploader("Upload your Toeic Certificate (L & R)", type=["jpg", "jpeg", "png", "webp"])
    
    if file is not None:
        imgOrg = Image.open(file)
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Original Image")
            st.image(imgOrg, use_column_width=True)
        
        file.seek(0) 
        imgTrans = processImage(file)
        
        if imgTrans is not None:
            with col2:
                st.subheader("Transformed Image")
                st.image(imgTrans, channels="BGR", use_column_width=True)
            
            cropped_images = image_predictions(imgTrans, key)
            
            for class_name, cropped_img in cropped_images.items():
                st.subheader(f"{class_name}: {text_ocr(cropped_img)[0]}")
                st.image(cropped_img, channels="BGR", use_column_width=True)
if __name__ == "__main__":
    main()