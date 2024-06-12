import os
from tempfile import NamedTemporaryFile
from io import BytesIO

from gtts import gTTS
import openai
from dotenv import load_dotenv
import pygame

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

# setting situation
language = "Engilsh"
gpt_name = "gpt"
level_string = f"a beginner in {language}"
level_word = "simple"
situation_en = "make a new friends"
my_role_en = "me"
gpt_role_en = "new friend"


SYSTEM_PROMPT = (
    f"You are helpful assistant supporting people learning {language}. "
    f"Your name is {gpt_name}. Please assume that the user you are assisting "
    f"is {level_string}. And please write only the sentence without "
    f"the character role."
)
USER_PROMPT = (
    f"Let's have a conversation in {language}. Please answer in {language} only "
    f"without providing a translation. And please don't write down the "
    f"pronunciation either. Let us assume that the situation in '{situation_en}'. "
    f"I am {my_role_en}. The character I want you to act as is {gpt_role_en}. "
    f"Please make sure that "
    f"I'm {level_string}, so please use {level_word} words as much as possible. "
    f"Now, start a conversation with the first sentence!"
)

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
]

def get_query(user_query: str) -> str:
    global messages

    messages.append({
        "role": "user",
        "content": user_query
    })

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    assistant_message = response.choices[0].message
    messages.append({
        "role": "assistant",
        "content": assistant_message.content
    })

    return assistant_message

def play_file(file_path: str) -> None:
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pass

    pygame.mixer.quit()


def say(message: str, lang: str):
    io = BytesIO()

    gTTS(message, lang=lang).write_to_fp(io)

    with NamedTemporaryFile() as f:
        f.write(io.getvalue())
        play_file(f.name)

def main():
    assistant_message = get_query(USER_PROMPT)
    print(f"[gpt] {assistant_message.content}")
    
    while line:= input("[user]").strip():
        if line == "!say":
            say(messages[-1]["content"], "en")
        else:
            response = get_query(line)
            print(f"[gpt] {response.content}")


if __name__ == '__main__':
    main()
