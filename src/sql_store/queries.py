import sqlite3


def get_connection():
    return sqlite3.connect("data/cbnu.db")


def filter_chunks_by_language(language: str) -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, section_title FROM chunks_metadata WHERE language = ?",
        (language,)
    )
    results = cursor.fetchall()
    conn.close()
    return results


def search_faq(query_text: str, language: str = "en") -> str:
    conn = get_connection()
    cursor = conn.cursor()

    question_col = f"question_{language}"
    answer_col = f"answer_{language}"

    cursor.execute(
        f"SELECT {question_col}, {answer_col} FROM faq WHERE {question_col} LIKE ?",
        (f"%{query_text}%",)
    )
    results = cursor.fetchall()
    conn.close()

    if not results:
        return "No matching FAQ found."

    formatted = []
    for question, answer in results:
        formatted.append(f"Q: {question}\nA: {answer}")

    return "\n\n".join(formatted)