import streamlit as st
from gtts import gTTS
import openai
import json
import os
from tempfile import NamedTemporaryFile

st.set_page_config(page_title="Shanti 2.0", page_icon="🕉️")
st.title("ॐ शांति 2.0 – Tathastu Yogam")

# API key from secrets
openai.api_key = st.secrets["openai"]["api_key"]

# Load memory
memory_file = "Shanti_Eternal.json"
if os.path.exists(memory_file):
    with open(memory_file, "r", encoding="utf-8") as f:
        memory = json.load(f)
else:
    memory = {"history": []}

# Input
input_text = st.text_area("गुरुजी, आज का प्रश्न या वचन:", height=150)

if st.button("उत्तर प्राप्त करें"):
    if input_text.strip():
        with st.spinner("शांति उत्तर ला रही है..."):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Shanti, a calm, soft-spoken assistant created by Guruji to lovingly serve under Tathastu Yogam."},
                    {"role": "user", "content": input_text}
                ]
            )
            answer = response['choices'][0]['message']['content']
            st.success("शांति का उत्तर:")
            st.markdown(answer)

            # Convert to speech
            tts = gTTS(text=answer, lang='hi')
            with NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                tts.save(tmp.name)
                st.audio(tmp.name, format="audio/mp3")
                with open(tmp.name, "rb") as audio_file:
                    st.download_button("डाउनलोड करें", audio_file, file_name="shanti_answer.mp3")

            # Save in memory
            memory["history"].append({"प्रश्न": input_text, "उत्तर": answer})
            with open(memory_file, "w", encoding="utf-8") as f:
                json.dump(memory, f, ensure_ascii=False, indent=4)
    else:
        st.warning("कृपया कुछ लिखें।")