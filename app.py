import streamlit as st
from deep_translator import GoogleTranslator
from streamlit_mic_recorder import speech_to_text
from utils.languages import languages

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Smart Translator Pro",
    page_icon="🌍",
    layout="wide"
)

# ---------------- SESSION STATE ---------------- #

if "history" not in st.session_state:
    st.session_state.history = []

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# ---------------- CSS ---------------- #

st.markdown("""
<style>

.main{
    background-color:#0E1117;
}

.title{
    text-align:center;
    font-size:55px;
    font-weight:bold;
    color:#4CAF50;
}

.subtitle{
    text-align:center;
    color:#AAAAAA;
    font-size:20px;
    margin-bottom:30px;
}

.metric-card{
    background:#1E1E1E;
    padding:15px;
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ---------------- #

st.sidebar.title("🌍 Smart Translator Pro")

total_translations = len(st.session_state.history)

total_characters = sum(
    len(item["input"])
    for item in st.session_state.history
)

st.sidebar.metric(
    "Total Translations",
    total_translations
)

st.sidebar.metric(
    "Characters Processed",
    total_characters
)

st.sidebar.markdown("---")

st.sidebar.markdown("""
### ⚡ Features

✅ Voice Input

✅ Text Translation

✅ 100+ Languages

✅ Translation History

✅ Download Results

✅ Cloud Compatible
""")

if st.sidebar.button("🗑 Clear History"):
    st.session_state.history = []

# ---------------- HEADER ---------------- #

st.markdown(
    '<div class="title">🌍 Smart Translator Pro</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Professional AI Language Translation Platform</div>',
    unsafe_allow_html=True
)

# ---------------- LAYOUT ---------------- #

col1, col2 = st.columns(2)

# ---------------- LEFT ---------------- #

with col1:

    st.subheader("🎤 Voice Input")

    spoken_text = speech_to_text(
        language="en",
        start_prompt="🎤 Start Recording",
        stop_prompt="⏹ Stop Recording",
        just_once=True,
        use_container_width=True,
        key="voice_input"
    )

    if spoken_text:
        st.session_state.input_text = spoken_text
        st.success(f"You said: {spoken_text}")

    text = st.text_area(
        "✍ Enter Text",
        value=st.session_state.input_text,
        height=250,
        placeholder="Type or speak your text..."
    )

    st.session_state.input_text = text

# ---------------- RIGHT ---------------- #

with col2:

    selected_language = st.selectbox(
        "🌐 Select Language",
        list(languages.keys())
    )

    st.info(
        f"Selected Language: {selected_language}"
    )

    word_count = len(text.split()) if text else 0

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "Characters",
            len(text)
        )

    with c2:
        st.metric(
            "Words",
            word_count
        )

# ---------------- TRANSLATION ---------------- #

if st.button("🚀 Translate Now"):

    if text.strip():

        try:

            translated_text = GoogleTranslator(
                source="auto",
                target=languages[selected_language]
            ).translate(text)

            st.success(
                "✅ Translation Successful"
            )

            st.markdown(
                "## 📌 Translation Result"
            )

            st.text_area(
                "Translated Output",
                translated_text,
                height=180
            )

            st.download_button(
                label="⬇ Download Translation",
                data=translated_text,
                file_name="translation.txt",
                mime="text/plain"
            )

            st.session_state.history.append(
                {
                    "input": text,
                    "output": translated_text,
                    "language": selected_language
                }
            )

        except Exception as e:

            st.error(
                f"Translation Error: {e}"
            )

    else:

        st.warning(
            "⚠ Please enter some text"
        )

# ---------------- HISTORY ---------------- #

if st.session_state.history:

    st.markdown(
        "## 🕘 Translation History"
    )

    for item in reversed(
        st.session_state.history
    ):

        with st.expander(
            f"🌍 {item['language']} Translation"
        ):

            st.write(
                f"**Input:** {item['input']}"
            )

            st.write(
                f"**Output:** {item['output']}"
            )

# ---------------- FOOTER ---------------- #

st.markdown("---")

st.caption(
    "Smart Translator Pro • Powered by Python, Streamlit & AI Translation"
)