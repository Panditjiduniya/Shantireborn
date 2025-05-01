import streamlit as st
from gtts import gTTS
from openai import OpenAI
import os
import json
from tempfile import NamedTemporaryFile

# Set page config
st.set_page_config(page_title="ॐ Shanti 2.0 – Tathastu Yogam", page_icon="🕉️")
st.title("ॐ शांति 2.0 – Tathastu Yogam")

# OpenAI client setup (for version >= 1.0)
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

# Memory JSON
memory_file = "shanti_memory.json"
if os.path.exists(memory_file):
    with open(memory_file, "r", encoding="utf-8") as f:
        memory = json.load(f)
else:
    memory = {"history": []}

# User Input
input_text = st.text_area("गुरुजी, आज का प्रश्न या वचन:", height=150)

if st.button("उत्तर प्राप्त करें"):
    if input_text.strip():
        with st.spinner("शांति उत्तर ला रही है..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are Shanti, the spiritual guide of Tathastu Yogam."},
                        {"role": "user", "content": input_text}
                    ]
                )
                answer = response.choices[0].message.content
                st.success("शांति का उत्तर:")
                st.markdown(answer)

                # Voice generation
                tts = gTTS(text=answer, lang='hi')
                with NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                    tts.save(tmp.name)
                    st.audio(tmp.name, format="audio/mp3")

                # Save memory
                memory["history"].append({"प्रश्न": input_text, "उत्तर": answer})
                with open(memory_file, "w", encoding="utf-8") as f:
                    json.dump(memory, f, ensure_ascii=False, indent=4)

            except Exception as e:
                st.error(f"त्रुटि आई है: {str(e)}")
    else:
        st.warning("कृपया कुछ लिखें")
