import streamlit as st
from translator import translate_text, LANGUAGES
from utils import load_history, save_history
from gtts import gTTS

# ---------------- PAGE ----------------
st.set_page_config(
    page_title="AI Language Translator",
    page_icon="🌍",
    layout="wide"
)

# ---------------- SESSION ----------------
if "source_lang" not in st.session_state:
    st.session_state.source_lang = "English"

if "target_lang" not in st.session_state:
    st.session_state.target_lang = "Telugu"

if "translated" not in st.session_state:
    st.session_state.translated = ""

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# ---------------- FUNCTIONS ----------------
def swap_languages():
    st.session_state.source_lang, st.session_state.target_lang = (
        st.session_state.target_lang,
        st.session_state.source_lang
    )

def clear_all():
    st.session_state.input_text = ""
    st.session_state.translated = ""

# ---------------- CSS ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e3a8a, #0f172a);
    color: white;
}
.title {
    text-align: center;
    font-size: 48px;
    font-weight: bold;
    color: #38bdf8;
}
.subtitle {
    text-align: center;
    color: #cbd5e1;
    margin-bottom: 20px;
}
.card {
    background: rgba(255,255,255,0.08);
    padding: 18px;
    border-radius: 15px;
    text-align: center;
    font-size: 20px;
    margin-top: 10px;
}
.output {
    background: rgba(255,255,255,0.10);
    padding: 20px;
    border-radius: 14px;
    font-size: 22px;
    border-left: 5px solid cyan;
}
footer {
    text-align:center;
    margin-top:30px;
    color:#cbd5e1;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙️ Settings")
show_history = st.sidebar.checkbox("📜 Show History")

# ---------------- HEADER ----------------
st.markdown(
    '<div class="title">🌍 AI Language Translator</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="subtitle">Translate text instantly with AI ✨</div>',
    unsafe_allow_html=True
)

# ---------------- LANGUAGE SELECT ----------------
col1, col2, col3 = st.columns([5,1,5])

with col1:
    st.selectbox(
        "Source Language",
        list(LANGUAGES.keys()),
        key="source_lang"
    )

with col2:
    st.write("")
    st.write("")
    st.button("🔄", on_click=swap_languages)

with col3:
    target_options = list(LANGUAGES.keys())[1:]
    st.selectbox(
        "Target Language",
        target_options,
        key="target_lang"
    )

# ---------------- INPUT ----------------
text = st.text_area(
    "✍ Enter Text",
    key="input_text",
    height=180,
    placeholder="Type your text here..."
)

# ---------------- STATS ----------------
s1, s2 = st.columns(2)

with s1:
    st.markdown(
        f'<div class="card">🔠 Characters<br>{len(text)}</div>',
        unsafe_allow_html=True
    )

with s2:
    st.markdown(
        f'<div class="card">📝 Words<br>{len(text.split())}</div>',
        unsafe_allow_html=True
    )

# ---------------- BUTTONS ----------------
b1, b2 = st.columns(2)

with b1:
    translate = st.button("🚀 Translate")

with b2:
    st.button("🧹 Clear", on_click=clear_all)

# ---------------- TRANSLATION ----------------
if translate:
    if text.strip() == "":
        st.warning("Please enter text.")
    else:
        try:
            translated = translate_text(
                text,
                st.session_state.source_lang,
                st.session_state.target_lang
            )

            st.session_state.translated = translated

            # Save History
            history = load_history()
            history.append({
                "input": text,
                "translated": translated,
                "source": st.session_state.source_lang,
                "target": st.session_state.target_lang
            })
            save_history(history)

        except Exception as e:
            st.error(f"Error: {e}")

# ---------------- OUTPUT ----------------
if st.session_state.translated:
    st.subheader("📌 Translated Output")

    st.markdown(
        f'<div class="output">{st.session_state.translated}</div>',
        unsafe_allow_html=True
    )

    # Download
    st.download_button(
        "📥 Download Translation",
        st.session_state.translated,
        file_name="translated_text.txt"
    )

    # Audio
    try:
        lang_code = LANGUAGES[st.session_state.target_lang]

        if lang_code == "zh-CN":
            lang_code = "zh"

        tts = gTTS(
            text=st.session_state.translated,
            lang=lang_code
        )

        tts.save("voice.mp3")

        with open("voice.mp3", "rb") as audio:
            st.audio(audio.read())

    except:
        st.warning("Audio not supported for this language.")

# ---------------- HISTORY ----------------
if show_history:
    st.subheader("📜 Translation History")
    history = load_history()

    if history:
        for item in reversed(history):
            st.markdown(
                f"""
                <div class="card">
                    <b>{item['source']} ➜ {item['target']}</b><br>
                    {item['translated']}
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.info("No history found.")

# ---------------- FOOTER ----------------
st.markdown(
    "<footer>Built with ❤️ using Streamlit + AI</footer>",
    unsafe_allow_html=True
)