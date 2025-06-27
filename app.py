import streamlit as st
import anthropic
import os

st.set_page_config(page_title="Claude Chatbot", page_icon="🤖")

st.title("🤖 Claude Chatbot")

if "client" not in st.session_state:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        st.error("Please set your ANTHROPIC_API_KEY environment variable")
        st.stop()
    st.session_state.client = anthropic.Anthropic(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What would you like to talk about?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            response = st.session_state.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[
                    {"role": m["role"], "content": m["content"]} 
                    for m in st.session_state.messages
                ]
            )
            
            assistant_response = response.content[0].text
            st.markdown(assistant_response)
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            
        except Exception as e:
            st.error(f"Error: {str(e)}")

with st.sidebar:
    st.header("Settings")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("**Note:** Set your `ANTHROPIC_API_KEY` environment variable to use this app.")