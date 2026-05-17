import os

from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound
)

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableLambda
)

from langchain_core.output_parsers import StrOutputParser


# -----------------------------
# FETCH TRANSCRIPT
# -----------------------------
def fetch_transcript(video_id):

    try:
        api = YouTubeTranscriptApi()

        fetched_transcript = api.fetch(video_id)

        transcript_text = ""

        for chunk in fetched_transcript:
            transcript_text += chunk.text + " "

        return transcript_text

    except TranscriptsDisabled:
        raise RuntimeError(
            "Transcript is disabled for this video."
        )

    except NoTranscriptFound:
        raise RuntimeError(
            "No transcript found for this video."
        )

    except Exception as e:
        raise RuntimeError(f"Transcript Error: {e}")


# -----------------------------
# CREATE VECTOR STORE
# -----------------------------
def create_vector_store(transcript, api_key):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.create_documents([transcript])

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=api_key
    )

    vector_store = FAISS.from_documents(
        chunks,
        embeddings
    )

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    return retriever


# -----------------------------
# MAIN RAG CHAIN
# -----------------------------
def get_main_chain(retriever, api_key):

    prompt = PromptTemplate(
        template="""
You are a helpful assistant.

Answer ONLY from the provided transcript context.

If the answer is not available in the context,
just say:
"I don't know based on the transcript."

Context:
{context}

Question:
{question}
""",
        input_variables=["context", "question"]
    )

    # Format retrieved docs
    def format_docs(docs):
        return "\n\n".join(
            doc.page_content for doc in docs
        )

    # LLM
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.2,
        api_key=api_key
    )

    # Parallel chain
    parallel_chain = RunnableParallel({
        "context": retriever | RunnableLambda(format_docs),
        "question": RunnablePassthrough()
    })

    # Final chain
    chain = (
        parallel_chain
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain