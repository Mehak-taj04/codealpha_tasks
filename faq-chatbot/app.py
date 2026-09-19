import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from faqs import faqs

st.set_page_config(page_title="FAQ Chatbot", page_icon="💬", layout="centered")

# ---- Custom CSS for chat bubble styling ----
st.markdown("""
<style>
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-top: 20px;
}
.user-bubble {
    align-self: flex-end;
    background-color: #4F46E5;
    color: white;
    padding: 10px 16px;
    border-radius: 18px 18px 4px 18px;
    max-width: 75%;
    font-size: 15px;
}
.bot-bubble {
    align-self: flex-start;
    background-color: #F1F1F4;
    color: #1a1a1a;
    padding: 10px 16px;
    border-radius: 18px 18px 18px 4px;
    max-width: 75%;
    font-size: 15px;
}
.chat-label {
    font-size: 12px;
    color: #888;
    margin-bottom: -6px;
}
</style>
""", unsafe_allow_html=True)

st.title("💬 FAQ Chatbot")
st.caption("Ask me a question and I'll find the closest matching answer!")

# Prepare the FAQ questions for matching
questions = [faq["question"] for faq in faqs]
vectorizer = TfidfVectorizer()
question_vectors = vectorizer.fit_transform(questions)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input row
col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_input("Type your question here:", label_visibility="collapsed", placeholder="e.g. How long does shipping take?")
with col2:
    send = st.button("Ask", use_container_width=True)

if send and user_input.strip():
    user_vector = vectorizer.transform([user_input])
    similarities = cosine_similarity(user_vector, question_vectors)[0]
    best_match_index = similarities.argmax()
    best_score = similarities[best_match_index]

    if best_score < 0.2:
        answer = "Sorry, I couldn't find a good match for that. Could you rephrase your question?"
    else:
        answer = faqs[best_match_index]["answer"]

    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Bot", answer))

# ---- Display chat as styled bubbles ----
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for speaker, message in st.session_state.chat_history:
    if speaker == "You":
        st.markdown(f'<div class="user-bubble">{message}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-bubble">🤖 {message}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Clear chat button
if st.session_state.chat_history:
    if st.button("🗑️ Clear chat"):
        st.session_state.chat_history = []
        st.rerun()