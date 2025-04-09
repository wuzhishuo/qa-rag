from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableMap
from .vector_db import load_vector_db
from .config import OPENAI_API_BASE, OPENAI_API_KEY
import logging

# 配置日志记录
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_qa_template():
    template = """
       你是电商客服，请严格依据以下内容回答问题。如果无法从中找到答案，请说“我不确定，请联系人工客服”。

        ---
        {context}
        ---

        问题：{question}
        """
    return PromptTemplate.from_template(template)


def get_qa_chain(logging: bool = False):
    retriever = load_vector_db().as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )
    llm = ChatOpenAI(
        model_name="gpt-4",
        temperature=0, openai_api_base=OPENAI_API_BASE, api_key= OPENAI_API_KEY
    )
    prompt = get_qa_template()

    def custom_llm(q):
        try:
            response = llm.invoke(q)
            if logging:
                logger.debug(f"OpenAI API 原始响应: {response}")
            return response
        except Exception as e:
            logger.error(f"OpenAI API 请求失败: {e}")
            raise

    chain = (
        RunnableMap(
            {
                "context": lambda q: retriever.invoke(q["query"]),
                "question": lambda q: q["query"],
            }
        )
        | prompt
        | custom_llm
        | StrOutputParser()
    )

    return chain
