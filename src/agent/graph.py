from langchain_core.tools import tool
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
import os

from src.agent.tools import search_guidebook as _search_guidebook

load_dotenv()


@tool
def search_guidebook(query: str) -> str:
    """Search the CBNU international student guidebook (available in English,
    Korean, and Chinese) for information about academic rules, visas,
    part-time work regulations, insurance, and student support services."""
    return _search_guidebook(query)


model = ChatAnthropic(
    model="claude-sonnet-4-5",
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)


from langchain.agents import create_agent

agent = create_agent(model, tools=[search_guidebook])


def ask(question: str) -> str:
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    return result["messages"][-1].content


if __name__ == "__main__":
    test_questions = [
        "What are the working hour limits for undergraduate part-time work?",
        "국제학생이 건강보험에 가입해야 하나요?",
        "外国人登录需要什么材料？",
    ]

    for question in test_questions:
        print(f"Q: {question}")
        print(f"A: {ask(question)}")
        print("\n" + "=" * 80 + "\n")