from langchain_core.tools import tool
from langchain_anthropic import ChatAnthropic
from langchain.agents import create_agent
from dotenv import load_dotenv
import os

from src.agent.tools import search_guidebook as _search_guidebook
from src.agent.tools import search_faq_tool as _search_faq_tool

load_dotenv()


@tool
def search_guidebook(query: str) -> str:
    """Search the CBNU international student guidebook (available in English,
    Korean, and Chinese) for information about academic rules, visas,
    part-time work regulations, insurance, and student support services."""
    return _search_guidebook(query)


@tool
def search_faq(query: str, language: str = "en") -> str:
    """Search frequently asked questions about CBNU academic rules,
    part-time work, leave of absence, and insurance. Use this for quick,
    direct questions before doing a full guidebook search. Language must
    be 'en', 'ko', or 'zh'."""
    return _search_faq_tool(query, language)


model = ChatAnthropic(
    model="claude-sonnet-4-5",
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

agent = create_agent(model, tools=[search_guidebook, search_faq])


def ask(question: str) -> str:
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    return result["messages"][-1].content


if __name__ == "__main__":
    test_questions = [
        "What are the working hour limits for undergraduate part-time work?",
        "국제학생이 건강보험에 가입해야 하나요?",
        "外国人登录需要什么材料？",
        "What GPA do I need from last semester to work part-time?",
    ]

    for question in test_questions:
        print(f"Q: {question}")
        print(f"A: {ask(question)}")
        print("\n" + "=" * 80 + "\n")