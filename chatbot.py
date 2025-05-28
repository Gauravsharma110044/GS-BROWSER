import os
import openai

def main():
    print("Welcome to the AI Chatbot! Type 'exit' to quit.")
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        print("Error: Please set your OPENAI_API_KEY environment variable.")
        return
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_input}]
            )
            reply = response.choices[0].message['content'].strip()
            print(f"AI: {reply}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
