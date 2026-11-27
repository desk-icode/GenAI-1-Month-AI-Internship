
import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("GEMINI_API_KEY is missing in .env")
    exit()

client = genai.Client(api_key=API_KEY)

MODELS = [
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite"
]

SYSTEM_PROMPT = """
You are an AI Study Assistant for beginner programming students.

Explain concepts in simple English.
Give practical examples when useful.
Use Python examples when required.
Keep answers simple and beginner-friendly.
"""

conversation_history = []


def get_ai_response(message):

    conversation_history.append({
        "role": "user",
        "content": message
    })

    history = "\n".join(
        f"{m['role']}: {m['content']}"
        for m in conversation_history
    )

    prompt = f"""
{SYSTEM_PROMPT}

Conversation History:
{history}

Answer the latest user message.
"""

    for model in MODELS:

        for attempt in range(3):

            try:

                print(f"\nUsing model: {model}")

                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )

                answer = response.text

                conversation_history.append({
                    "role": "assistant",
                    "content": answer
                })

                return answer

            except Exception as error:

                error_text = str(error)

                if "503" in error_text:

                    print(
                        f"Model busy. Retrying "
                        f"({attempt + 1}/3)..."
                    )

                    time.sleep(2 ** attempt)

                else:
                    raise error

        print(f"\n{model} is currently unavailable.")
        print("Trying another model...")

    return "AI service is currently unavailable. Please try again later."


def explain_topic():

    topic = input("Enter topic: ")

    if not topic.strip():
        print("Topic cannot be empty.")
        return

    prompt = f"""
Explain {topic} to a beginner.

Give:
- Definition
- Important points
- Practical example
- Python example if applicable
"""

    return get_ai_response(prompt)


def generate_quiz():

    topic = input("Enter topic: ")

    if not topic.strip():
        print("Topic cannot be empty.")
        return

    prompt = f"""
Create a beginner quiz about {topic}.

Generate 5 questions.
Use multiple-choice and short-answer questions.
Do not give the answers immediately.
"""

    return get_ai_response(prompt)


def create_study_plan():

    topic = input("Enter topic: ")
    days = input("Number of days: ")

    if not topic.strip():
        print("Topic cannot be empty.")
        return

    prompt = f"""
Create a {days}-day study plan for {topic}.

For each day provide:
- Topic
- What to learn
- Practical activity
- Small task
"""

    return get_ai_response(prompt)


def coding_practice():

    topic = input("Enter programming topic: ")

    if not topic.strip():
        print("Topic cannot be empty.")
        return

    prompt = f"""
Create a beginner coding problem about {topic}.

Include:
1. Problem statement
2. Requirements
3. Example input
4. Example output
5. Hint

Do not provide the complete solution.
"""

    return get_ai_response(prompt)


def summarize_notes():

    notes = input("Paste your notes: ")

    if not notes.strip():
        print("Notes cannot be empty.")
        return

    prompt = f"""
Summarize these study notes:

{notes}

Give:
- Key points
- Important terms
- Short revision notes
"""

    return get_ai_response(prompt)


def follow_up():

    question = input("Ask your question: ")

    if not question.strip():
        print("Question cannot be empty.")
        return

    return get_ai_response(question)


def main():

    print("\n===== AI STUDY ASSISTANT =====")

    while True:

        print("\n1. Explain Topic")
        print("2. Generate Quiz")
        print("3. Create Study Plan")
        print("4. Coding Practice")
        print("5. Summarize Notes")
        print("6. Ask Follow-up")
        print("7. Exit")

        choice = input("\nEnter choice: ")

        try:

            if choice == "1":
                answer = explain_topic()

            elif choice == "2":
                answer = generate_quiz()

            elif choice == "3":
                answer = create_study_plan()

            elif choice == "4":
                answer = coding_practice()

            elif choice == "5":
                answer = summarize_notes()

            elif choice == "6":
                answer = follow_up()

            elif choice == "7":
                print("\nThank you!")
                break

            else:
                print("\nInvalid choice.")
                continue

            if answer:
                print("\nAI:\n")
                print(answer)

        except Exception as error:
            print("\nError:", error)


if __name__ == "__main__":
    main()