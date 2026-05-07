from sahayakbrain import process_text
import requests


if __name__ == "__main__":

    print("\n🚨 Sahayak AI System Started 🚨")
    print("Type 'exit' to stop\n")

    context = {}

    while True:

        text = input("👤 Caller: ")

        if text.lower() == "exit":
            break

        result = process_text(text, context)

        print("\n🤖 AI:", result["response"])

        requests.post(
            "http://127.0.0.1:5000/update",
            json={
                "emotion": result["emotion"],
                "priority": result["priority"],
                "incident": result["incident"],
                "location": result["location"],
                "people": result["people"],
                "transcript": text,
                "response": result["response"]
            }
        )