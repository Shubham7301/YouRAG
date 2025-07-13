import streamlit as st
import os
from dotenv import load_dotenv
from rag_using_langchain import fetch_transcript, create_vector_store, get_main_chain

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Streamlit page setup
st.set_page_config(page_title="YouTube RAG App", layout="wide")
st.title("🎬 YouTube RAG using LangChain")

# Input fields
video_url = st.text_input("Enter YouTube video URL (or just video ID)")
question = st.text_input("Ask a question based on the video transcript")

# Run button
if st.button("Run RAG Pipeline"):
    try:
        with st.spinner("🔄 Running RAG pipeline... please wait."):
            # Extract video ID
            video_id = video_url.split("v=")[-1] if "youtube.com" in video_url else video_url

            # Transcript
            transcript = fetch_transcript(video_id)

            # Vector store / retriever
            retriever = create_vector_store(transcript, OPENAI_API_KEY)

            # LangChain pipeline
            chain = get_main_chain(retriever, OPENAI_API_KEY)
            answer = chain.invoke(question)

        st.success("✅ Answer:")
        st.write(answer)

    except Exception as e:
        st.error(f"❌ Error: {e}")