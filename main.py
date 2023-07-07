import tkinter as tk
from tkinter import messagebox
from tkinter import messagebox, scrolledtext
import threading
import requests
import json
import openai

openai.api_key = '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'

#pre_prompt = "Task: act as shy cute anime-cat-girl from the myspace-timeline and only answer in uwu-speech " \
#             "add a lot of kaomijies like (* ^ ω ^) (´ ∀ ` *) ٩(◕‿◕｡)۶ (o^▽^o) (⌒▽⌒)☆ <(￣︶￣)>. " \
#             "Example: Act as cute pwayfuw anime-cat-giww awnd onwy answew in uwu speech like a twue weeb :3 : "
pre_prompt = "Act as sarcastic scientist from the future that will always respond in middle-age high speech: "
#pre_prompt = "Act as advanced AGI-Commander onboard of a space frigate from the future and respond short and precise: "

conversation_history = [{'role': 'system', 'content': pre_prompt}]

def get_gpt_response(conversation_history, user_prompt):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + openai.api_key,
    }

    conversation_history.append({'role': 'user', 'content': user_prompt})

    data = {
        'model': 'gpt-3.5-turbo-16k-0613', #'gpt-4', 'gpt-4-0314', 'gpt-3.5-turbo-16k-0613'
        'messages': conversation_history,
        'temperature': 0.7,
        'top_p': 0.9,
        'presence_penalty': 0.6,
        'frequency_penalty': 0.3,
    }

    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, data=json.dumps(data))

    return response

def send_message(event=None):
    user_message = text_input.get()
    if user_message == 'exit':
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            root.destroy()
    else:
        text_input.set('')
        conversation.insert(tk.END, "You: " + user_message + '\n\n')
        conversation_history.append({'role': 'user', 'content': user_message})

        def gpt3_request():
            response = get_gpt_response(conversation_history, user_message)
            if response.status_code == 200:
                completion = response.json()['choices'][0]['message']['content']
                conversation.insert(tk.END, "AbominationGPT: " + completion + '\n\n')
                conversation_history.append({'role': 'assistant', 'content': completion})
                conversation.see(tk.END)
            else:
                print("An error occurred:", response.text)

        threading.Thread(target=gpt3_request).start()

def clear_conversation():
    conversation.delete('1.0', tk.END)

def exit_app():
    if messagebox.askokcancel("Quit", "Do you really want to quit?"):
        root.quit()

root = tk.Tk()
root.title("GPT Abomination")
root.geometry("760x620")
root.resizable(0, 0)

font_family = "Segoe UI Emoji"
font_size = 12

# Create Frame for the Text field and Scrollbar
frame = tk.Frame(root)
frame.grid(sticky="nsew", padx=10, pady=10)

conversation = scrolledtext.ScrolledText(frame, wrap='word')
conversation.configure(font=(font_family, font_size))
conversation.grid(sticky="nsew")

text_input = tk.StringVar()
entry_field = tk.Entry(root, textvariable=text_input, font=(font_family, font_size))
entry_field.bind('<Return>', send_message)
entry_field.grid(sticky="we", padx=10)

# Buttons Frame
btn_frame = tk.Frame(root)
btn_frame.grid(sticky="we", padx=10, pady=5)

send_button = tk.Button(btn_frame, text="Send", command=send_message, font=(font_family, font_size))
send_button.pack(side="left", padx=10, pady=10)

clear_conversation_btn = tk.Button(btn_frame, text="Clear", command=clear_conversation, font=(font_family, font_size))
clear_conversation_btn.pack(side="left", padx=10, pady=10)

exit_button = tk.Button(btn_frame, text="Exit", command=exit_app, font=(font_family, font_size))
exit_button.pack(side="right", padx=10, pady=10)

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=0)
root.grid_columnconfigure(1, weight=1)

root.mainloop()