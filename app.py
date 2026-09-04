import streamlit as st
from src.agent.graph import ask

st.set_page_config(page_title="CBNU Student Assistant", page_icon="🎓")

st.markdown("## 🎓 CBNU International Student Assistant")
st.caption("Ask questions in English, Korean, or Chinese about academic rules, visas, part-time work, and more.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Ask a question...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = ask(user_input)
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})