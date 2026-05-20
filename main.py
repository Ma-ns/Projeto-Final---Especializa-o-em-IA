import os
import subprocess
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
    contextFile = open("messages.json","r", encoding="utf-8")

    contextData = json.load(contextFile)

    response = requests.post(
        "http://localhost:5678/webhook/9a164fab-6171-463d-b8fe-b45c4baa4e11",
        json={
            "message": message,
            "context": contextData
        }
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

def cleanChat():
    subprocess.run("cls", shell=True)

def isMessagesNotEmpty():
    with open("messages.json", "r", encoding="utf-8") as file:
        messagesData = json.load(file)
        
        return len(messagesData) == 0

def main():
    op = ""

    if isMessagesNotEmpty:
        op = input("Deseja continuar a conversa anterior?(Sim, Não)\n")

    cleanChat()

    if "não" in op.lower():
        resetChat()

    messageInput = ""

    print("CHATBOT\nInstruções: Envie uma pergunta para que o bot te auxilie. Dê tchau para sair :)")

    botFirstMessage = ""

    if "sim" in op.lower():
        with open("messages.json", "r") as file:
            messages = json.load(file)

            for m in messages:
                print(m["text"] + "\n")
    else:
        botFirstMessage = Message("Olá, como posso ajudar?\n", sender="bot")

        print(botFirstMessage.text)

    while("tchau" not in messageInput.lower()):
        messageInput = input()

        if "tchau" in messageInput.lower():
            return
        
        if "não" in op.lower():
            saveMessage(botFirstMessage)

        message = Message(messageInput, "user")

        saveMessage(message)

        botMessage = getBotResponse(messageInput)

        print("\n" + botMessage + "\n")

        message = Message(botMessage, "bot")

        saveMessage(message)


if __name__ == "__main__":
    main()