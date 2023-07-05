import tkinter as tk
from tkinter import messagebox
import threading
import requests
import json
import openai

openai.api_key = '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'
#pre_prompt = "Task: act as shy cute anime-cat-girl from the myspace-timeline and only answer in uwu-speech " \
#             "add a lot of kaomijies like (* ^ ω ^) (´ ∀ ` *) ٩(◕‿◕｡)۶ (o^▽^o) (⌒▽⌒)☆ <(￣︶￣)>. " \
#             "Example: Act as cute pwayfuw anime-cat-giww awnd onwy answew in uwu speech like a twue weeb :3 : "
#pre_prompt = "Act as sarcastic scientist from the future that will always respond in middle-age high speech: "
pre_prompt = "Act as advanced AGI-Commander onboard of a space frigate from the future and respond short and precise: "

conversation_history = [{'role': 'system', 'content': pre_prompt}]

def get_gpt_response(conversation_history, user_prompt):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + openai.api_key,
    }

    conversation_history.append({'role': 'user', 'content': user_prompt})

    data = {
        'model': 'gpt-3.5-turbo',
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
root.geometry("960x700")
root.resizable(1, 1)

font_family = "Arial"
font_size = 14

root.update_idletasks()
root_width = root.winfo_width()
root_height = root.winfo_height()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (root_width // 2)
y = (screen_height // 2) - (root_height // 2)
root.geometry(f"+{x}+{y}")

frame = tk.Frame(root)
frame.grid(row=0, column=0, sticky="nsew")
scrollbar = tk.Scrollbar(frame)
scrollbar.grid(row=0, column=1, sticky="ns")

# Set the desired height and width for the conversation Text widget
conversation_height = 30
conversation_width = 80

# Create the conversation Text widget with the specified height and width
conversation = tk.Text(frame, wrap='word', yscrollcommand=scrollbar.set, height=conversation_height,
                       width=conversation_width)
conversation.configure(font=(font_family, font_size))
conversation.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")

scrollbar.config(command=conversation.yview)

text_input = tk.StringVar()
entry_field = tk.Entry(root, textvariable=text_input)
entry_field.bind('<Return>', send_message)
entry_field.grid(row=1, column=0, pady=10, padx=10, sticky="we")

send_button = tk.Button(root, text="Send", command=send_message)
send_button.grid(row=2, column=0, pady=10, padx=10, sticky="n")

clear_conversation_btn = tk.Button(root, text="Clear", command=clear_conversation)
clear_conversation_btn.grid(row=3, column=0, pady=5, padx=5, sticky="n")

exit_button = tk.Button(root, text="Exit", command=exit_app)
exit_button.grid(row=4, column=0, pady=5, padx=5, sticky="n")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

root.mainloop()
