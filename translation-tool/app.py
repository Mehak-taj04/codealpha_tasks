import streamlit as st
from deep_translator import MyMemoryTranslator

st.set_page_config(page_title="Language Translator", page_icon="🌐")
st.title("🌐 Language Translation Tool")

# Get MyMemory's own supported languages (its codes look like 'en-US', not just 'en')
languages = MyMemoryTranslator(source="english", target="french").get_supported_languages(as_dict=True)
lang_names = sorted(languages.keys())

col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("Source language", lang_names, index=lang_names.index("english"))
with col2:
    target_lang = st.selectbox("Target language", lang_names, index=lang_names.index("french"))

text_input = st.text_area("Enter text to translate", height=150)

if st.button("Translate"):
    if not text_input.strip():
        st.warning("Please enter some text first.")
    else:
        try:
            src_code = languages[source_lang]
            tgt_code = languages[target_lang]
            translated = MyMemoryTranslator(source=src_code, target=tgt_code).translate(text_input)

            st.subheader("Translated Text")
            st.code(translated, language=None)

        except Exception as e:
            st.error(f"Translation failed: {e}")