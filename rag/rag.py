"""
总结服务类，用户提问，搜索参考资料，将提问和参考资料提交给模型，模型返回总结回复
"""
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from utils.config_loder import load_rag_config
from utils.prompts_loder import get_rag_summarize_prompt
from rag.vector_service import VectorService
from model.model import get_chat_model, llm

def p_pro(prompt):
    print(prompt.to_string())
    print("-----------------"*3)
    return prompt


def create_rag_chain():
    vector_service = VectorService()
    retriever = vector_service.get_retriever()

    prompt = PromptTemplate.from_template(get_rag_summarize_prompt())

    def format_docs(docs):
        return "\n".join([doc.page_content for doc in docs])

    chain = (
        {"context": retriever | format_docs, "input": RunnablePassthrough()}
        | prompt | p_pro
        | llm
        | StrOutputParser()
    )
    return chain


def rag_query(query: str):
    chain = create_rag_chain()
    return chain.invoke(query)


if __name__ == "__main__":
    result = rag_query("扫地机器人如何清洁？")
    print(result)
