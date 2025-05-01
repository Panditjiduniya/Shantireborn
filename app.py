import streamlit as st
from gtts import gTTS
import openai
import os
import json
from tempfile import NamedTemporaryFile

# Page Setup
st.set_page_config(page_title="ॐ Shanti 2.0 – Tathastu Yogam", page_icon="🕉️")
st.title("ॐ शांति 2.0 – Tathastu Yogam")
st.markdown("**गुरुजी, आज का प्रश्न या वचन:**")

# OpenAI Client Initialization
client = openai.OpenAI(api_key=st.secrets["openai"]["api_key"])

# Memory JSON
memory_file = "Shanti_Memory.json"
if os.path.exists(memory_file):
    with open(memory_file, "r", encoding="utf-8") as f:
        memory = json.load(f)
else:
    memory = {"history": []}

# Input Box
input_text = st.text_area("गुरुजी, आज का प्रश्न या वचन:", height=150)

# Button
if st.button("उत्तर प्राप्त करें"):
    if input_text.strip():
        with st.spinner("शांति उत्तर ला रही है..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are Shanti, a spiritual AI assistant created for Guruji under Tathastu Yogam."},
                        {"role": "user", "content": input_text}
                    ]
                )
                answer = response.choices[0].message.content
                st.success("शांति का उत्तर:")
                st.markdown(answer)

                # Audio Output
                tts = gTTS(text=answer, lang='hi')
                with NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                    tts.save(tmp.name)
                    st.audio(tmp.name, format="audio/mp3")
                    with open(tmp.name, "rb") as audio_file:
                        st.download_button("डाउनलोड करें", audio_file, file_name="shanti_voice.mp3")

                # Save to memory
                memory["history"].append({"प्रश्न": input_text, "उत्तर": answer})
                with open(memory_file, "w", encoding="utf-8") as f:
                    json.dump(memory, f, ensure_ascii=False, indent=4)

            except Exception as e:
                st.error(f"त्रुटि आई है: {str(e)}")
    else:
        st.warning("कृपया कुछ लिखें।")
