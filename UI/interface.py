import streamlit as st

option = st.sidebar.radio("Choose one of the options :", ["Upload image", "Descriptive text writing"])

if option == "Upload image":
    st.header("Upload an Image")
    uploaded_image = st.file_uploader("Choose an image", type=['jpg', 'jpeg', 'png'])


    if uploaded_image:
        st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
        st.write("Processing the image for recommendations...")


elif option == "Descriptive text writing":
    st.header("Enter a Descriptive Text")
    description_text = st.text_area("Enter the description of the place or restaurant here:")

    if description_text:
        st.write(f"Searching based on the description: {description_text}")
