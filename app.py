import streamlit as st
from googletrans import Translator
from utils.languages import languages
from voice_utils import recognize_speech, speak_text

# Page configuration
st.set_page_config(
    page_title="AI Voice Translation Assistant",
    page_icon="🌍",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>

.main {
    background-color: #0E1117;
    color: white;
}

.title {
    text-align: center;
    font-size: 55px;
    font-weight: bold;
    color: #4CAF50;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    color: #AAAAAA;
    margin-bottom: 40px;
    font-size: 22px;
}

.stButton > button {
    width: 100%;
    background-color: #4CAF50;
    color: white;
    border-radius: 12px;
    height: 3.2em;
    font-size: 18px;
    font-weight: bold;
}

.stTextArea textarea {
    font-size: 18px;
}

.history-box {
    padding: 15px;
    border-radius: 10px;
    background-color: #1E1E1E;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🌍 AI Voice Translator")

st.sidebar.info(
    """
    ### Features
    ✅ Multi-language translation  
    ✅ Voice input  
    ✅ Voice output  
    ✅ Translation history  
    ✅ Character counter  
    ✅ Download translations  
    ✅ Interactive UI  
    """
)

# Clear history
if st.sidebar.button("🗑 Clear History"):
    st.session_state.history = []

# Title
st.markdown(
    '<div class="title">🌍 AI Voice Translation Assistant</div>',
    unsafe_allow_html=True
)

# Subtitle
st.markdown(
    '<div class="subtitle">Speak, Translate & Listen using AI + NLP</div>',
    unsafe_allow_html=True
)

# Translator object
translator = Translator()

# Layout
col1, col2 = st.columns(2)

# Initialize session state
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# LEFT COLUMN
with col1:

    # Voice input
    if st.button("🎤 Speak"):

        spoken_text = recognize_speech()

        st.session_state.input_text = spoken_text

        st.success(f"You said: {spoken_text}")

    # Text area
    text = st.text_area(
        "✍ Enter Text",
        value=st.session_state.input_text,
        height=250,
        placeholder="Type your text here..."
    )

    # Update session state
    st.session_state.input_text = text

# RIGHT COLUMN
with col2:

    selected_language = st.selectbox(
        "🌐 Select Language",
        list(languages.keys())
    )

    st.info(f"Selected Language: {selected_language}")

    st.metric(
        label="Character Count",
        value=len(text)
    )

# Translate button
if st.button("🚀 Translate Now"):

    if text.strip() != "":

        translated = translator.translate(
            text,
            dest=languages[selected_language]
        )

        st.success("✅ Translation Successful")

        st.markdown("## 📌 Translated Text")

        st.code(translated.text, language=None)

        # Speak translation
        if st.button("🔊 Speak Translation"):

            speak_text(translated.text)

        # Download translation
        st.download_button(
            label="⬇ Download Translation",
            data=translated.text,
            file_name="translation.txt",
            mime="text/plain"
        )

        # Store history
        if "history" not in st.session_state:
            st.session_state.history = []

        st.session_state.history.append({
            "input": text,
            "output": translated.text,
            "language": selected_language
        })

    else:
        st.warning("⚠ Please enter some text")

# Translation History
if "history" in st.session_state and st.session_state.history:

    st.markdown("## 🕘 Translation History")

    for item in reversed(st.session_state.history):

        st.markdown(
            f"""
            <div class="history-box">
                <h4>🌍 {item['language']}</h4>
                <p><b>Input:</b> {item['input']}</p>
                <p><b>Output:</b> {item['output']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# Footer
st.markdown("---")

st.caption(
    "Built with ❤️ using Python, Streamlit, SpeechRecognition & Google Translate API"
)