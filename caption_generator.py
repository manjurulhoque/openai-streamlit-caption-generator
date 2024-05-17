import base64

import requests
import streamlit as st
from PIL import Image


def main():
    st.set_page_config(page_title="Image Caption Generator")

    st.markdown(
        "<h1 style='text-align: center;'>Image Caption Generator</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align: center;'>Use AI to generate captions for any images.</p>",
        unsafe_allow_html=True,
    )

    # Image upload section
    uploaded_file = st.file_uploader(
        "Upload an image or photo (Max 4MB)", type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        new_image = image.resize((600, 400))
        # Display the uploaded image
        st.image(new_image, caption="Uploaded Image", use_column_width=False)

    # Select a vibe
    vibe = st.selectbox(
        "Select a Vibe",
        options=[
            "😆 Fun",
            "😜 Joke",
            "🤣 Funny",
            "🥳 Happy",
            "😑 Serious",
            "😭 Sad",
            "😡 Angry",
            "🙌🏻 Ecstatic",
            "🧐 Curious",
            "📔 Informative",
            "😻 Cute",
            "🧊 Cool",
            "😲 Controversial",
        ],
    )

    # Additional prompt (optional)
    additional_prompt = st.text_input(
        "Additional Prompt (Optional)", placeholder="e.g., the photo is in Byron Bay"
    )

    # Initialize or use existing session state variable for button press
    if 'button_pressed' not in st.session_state:
        st.session_state.button_pressed = False

    # Generate captions button
    if st.button("Generate Captions", disabled=st.session_state.button_pressed):
        if uploaded_file is not None:

            st.session_state.button_pressed = True
            with st.spinner('Generating captions... Please wait.'):
                captions = generate_caption(uploaded_file, vibe, additional_prompt)
                if captions:
                    for i, caption in enumerate(captions, 1):
                        st.code(caption, language="txt")
                else:
                    st.error("Failed to generate captions or no captions returned.")
            # Reset the button press state after processing
            st.session_state.button_pressed = False
        else:
            st.error("Please upload an image to generate captions.")


def generate_caption(uploaded_file, vibe, additional_prompt):
    vibe = vibe.split(" ")[1]
    if vibe == "Fun":
        prompt = "Generate a fun and playful caption for this image."
    elif vibe == "Joke":
        prompt = "Generate a humorous and joking caption for this image."
    elif vibe == "Funny":
        prompt = "Generate a funny and amusing caption for this image."
    elif vibe == "Happy":
        prompt = "Generate a happy and joyful caption for this image."
    elif vibe == "Serious":
        prompt = "Generate a serious and professional caption for this image."
    elif vibe == "Sad":
        prompt = "Generate a sad and emotional caption for this image."
    elif vibe == "Angry":
        prompt = "Generate an angry and intense caption for this image."
    elif vibe == "Ecstatic":
        prompt = "Generate an ecstatic and overly excited caption for this image."
    elif vibe == "Curious":
        prompt = "Generate a curious and inquisitive caption for this image."
    elif vibe == "Informative":
        prompt = "Generate an informative and educational caption for this image."
    elif vibe == "Cute":
        prompt = "Generate a cute and adorable caption for this image."
    elif vibe == "Cool":
        prompt = "Generate a cool and stylish caption for this image."
    elif vibe == "Controversial":
        prompt = "Generate a controversial and provocative caption for this image."
    else:
        st.error("Invalid vibe specified.")
        return

    if additional_prompt:
        prompt += f" and additionally, {additional_prompt}"

    try:
        base64_image = base64.b64encode(uploaded_file.getvalue()).decode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {st.secrets['OPENAI_API_KEY']}",
        }
        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            "max_tokens": 300,
            "n": 3,
        }
        response = requests.post(
            "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
        )
        response.raise_for_status()
        data = response.json()
        captions = [item.get('message', {}).get('content') for item in data.get('choices', [])]
        return captions
    except Exception as e:
        st.error(f"Failed to call OpenAI API: {str(e)}")
        return []


if __name__ == "__main__":
    main()
