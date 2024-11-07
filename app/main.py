import os
import streamlit as st
from PIL import Image
from dotenv import load_dotenv
from image_processing import processImage
from text_recognization import text_recognize
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
            
            croppedImages = image_predictions(imgTrans, key)
            
            for className, croppedImg in croppedImages.items():
                text = text_recognize(croppedImg)
                if text is not None:
                    st.subheader(f"{className}: {text[0]}")
                else:
                    st.subheader(f"{className}: No text found")
                st.image(croppedImg, channels="BGR")
if __name__ == "__main__":
    main()