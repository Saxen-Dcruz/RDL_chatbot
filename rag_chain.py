# rag_chain.py
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from prompts import RDL_PROMPT
from LLM_setup import load_api_key, initialize_llm

# 🔹 Import Hugging Face zero-shot classifier
from transformers import pipeline

# Load zero-shot classifier once at startup
exit_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")


def detect_exit_intent(user_input: str, threshold: float = 0.8) -> bool:
    """
    Detect if the user wants to end the conversation using rules + zero-shot classification.
    Returns True if intent is clearly 'end_conversation'.
    """
    normalized = user_input.strip().lower()

    # 🛑 Fast rule-based exits
    hard_exits = {"exit", "quit", "bye", "goodbye", "stop", "end"}
    if normalized in hard_exits:
        return True

    # 🧪 Special handling for short "no"
    if normalized == "no":
        labels = ["continue_conversation", "end_conversation"]
        result = exit_classifier(user_input, candidate_labels=labels)
        top_label, score = result["labels"][0], result["scores"][0]

        if top_label == "end_conversation" and score >= threshold:
            return True
        return False  # If not strongly "end", continue

    # 🚦 For longer inputs, run classifier
    if len(normalized.split()) > 2:
        labels = ["continue_conversation", "end_conversation"]
        result = exit_classifier(user_input, candidate_labels=labels)
        top_label, score = result["labels"][0], result["scores"][0]

        if top_label == "end_conversation" and score >= threshold:
            return True

    return False


def load_vectorstore(index_path=r"C:\Users\gerar\Desktop\rdl_data\knowledge_base\faiss_index"):
    print("📦 Loading FAISS vector store...")
    embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")
    vectorstore = FAISS.load_local(
        index_path,
        embeddings=embedding_model,
        allow_dangerous_deserialization=True
    )
    print("✅ Vector store loaded.")
    return vectorstore


def build_conv_rag_chain(llm, vectorstore, k=3):
    """
    Build a Conversational RAG chain with short-term buffer memory.
    """
    print("🔧 Building Conversational QA chain...")
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})

    # 🧠 Short-term memory (in RAM only)
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"   # ✅ tell memory which output to track
    )

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": RDL_PROMPT},
        return_source_documents=True
    )
    print("✅ Conversational QA chain ready with short-term memory.")
    return chain


if __name__ == "__main__":
    # 🔑 Load API key and initialize LLM
    api_key = load_api_key()
    llm = initialize_llm(api_key)

    # 📦 Load vector store
    vectorstore = load_vectorstore()

    # 🔧 Build chain
    rag_chain = build_conv_rag_chain(llm, vectorstore, k=4)

    print("\n💬 RDL Assistant ready. Type 'exit' to quit. (Short-term memory enabled)")

    while True:
        query = input("\n Enter your question (or type 'exit' to quit): ").strip()

        # ✅ Smart exit detection
        if detect_exit_intent(query):
            print("✅ Chat session closed. Have a great day!")
            break

        # 🚀 Invoke the chain
        result = rag_chain.invoke({"question": query})

        # 🖨️ Display response
        print("\n🤖 Answer:", result["answer"])
