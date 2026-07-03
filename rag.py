from config import OPENAI_API_KEY
from vectorstore import VectorStoreManager

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate


class RAGPipeline:

    def __init__(self):

        self.vector_manager = VectorStoreManager()

        self.llm = ChatOpenAI(
            model="gpt-4.1-mini",
            api_key=OPENAI_API_KEY,
            temperature=0
        )

    def ask_question(self, question):

        vector_db = self.vector_manager.load_vector_store()

        if vector_db is None:

            response = self.llm.invoke(question)

            return {
                "answer": response.content,
                "sources": []
            }

        retriever = vector_db.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": 6,
                "fetch_k": 20,
            }
        )

        docs = retriever.invoke(question)

        print("=" * 60)
        print("Retrieved Documents:", len(docs))
        print("=" * 60)

        if len(docs) == 0:

            response = self.llm.invoke(question)

            return {
                "answer": response.content,
                "sources": []
            }

        context = "\n\n---\n\n".join(
            doc.page_content.strip() for doc in docs
        )

        prompt = ChatPromptTemplate.from_template(
            """
You are a helpful AI assistant that answers questions using the uploaded document.

Use the context below as your primary source. The context may use different words
than the question (for example, "vacation" vs "PTO", "remote work" vs "work from home").
Treat these as the same when the meaning matches.

Instructions:
1. Answer the question using information from the context.
2. Combine details from multiple context sections when needed.
3. Be specific and accurate. Quote or paraphrase the relevant parts.
4. Only say "I couldn't find that information in the uploaded document." if the
   context truly does not contain anything related to the question.

Context:
{context}

Question:
{question}

Answer:
"""
        )

        chain = prompt | self.llm

        response = chain.invoke(
            {
                "context": context,
                "question": question
            }
        )

        sources = []
        seen_sources = set()

        for doc in docs:

            metadata = doc.metadata

            source = {
                "file": metadata.get("source", "Unknown"),
                "page": metadata.get("page", metadata.get("page_number", "-"))
            }

            source_key = (source["file"], source["page"])
            if source_key in seen_sources:
                continue

            seen_sources.add(source_key)
            sources.append(source)

        return {
            "answer": response.content,
            "sources": sources
        }
