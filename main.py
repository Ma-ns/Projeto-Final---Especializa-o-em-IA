import json
import requests

class Message:
    def __init__(self, text, sender):
        self.text = text
        self.sender = sender

    def to_dict(self):
        return {
            "text": self.text,
            "sender": self.sender
        }

def getBotResponse(message):
    response = requests.post(
        "http://localhost:5678/webhook/9a164fab-6171-463d-b8fe-b45c4baa4e11",
        json={"message": message}
    )

    data = response.json()

    text_json = data["parts"][0]["text"]
    text_dict = json.loads(text_json)
    returnMessage = text_dict["message"] 

    return returnMessage

def saveMessage(message: Message):
    messages = []

    with open("messages.json", "r", encoding="utf-8") as file:
        messages = json.load(file)

    messages.append(message.to_dict())

    with open("messages.json", "w", encoding="utf-8") as file:
        json.dump(messages, file, ensure_ascii=False, indent=2)

def resetChat():
    with open("messages.json", "w", encoding="utf-8") as file:
        json.dump([], file, ensure_ascii=False, indent=2)

def main():
    resetChat()

    messageInput = ""

    print("CHATBOT\n")

    botFirstMessage = Message("Olá, como posso ajudar?", sender="bot")

    saveMessage(botFirstMessage)

    print(botFirstMessage.text)

    while("tchau" not in messageInput.lower()):
        messageInput = input()

        if "tchau" in messageInput.lower():
            resetChat()
            return

        message = Message(messageInput, "user")

        saveMessage(message)

        botMessage = getBotResponse(messageInput)

        print(botMessage)

        message = Message(botMessage, "bot")

        saveMessage(message)


if __name__ == "__main__":
    main()