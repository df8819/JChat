import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import requests
import json
import openai


class JChat:
    def __init__(self):
        openai.api_key = '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'
        self.behaviors = {
    "Default": "Act as normal GPT instance: ",
    "eGirl": "Task: act as shy cute anime-cat-girl from the myspace-timeline: ",
    "Sarcastic Scientist": "Act as sarcastic scientist from the future: ",
    "AGI Commander": "Act as advanced AGI-Commander onboard of a space frigate: ",
    "Swiss Guide": "Your task is to act as guide for Switzerland and ALWAYS/ONLY speak in swiss-german. Example: 'Verhalte dich wie en Guide fürd Schwiiz und duen bitte nur uf Schwiizerdütsch antworte': ",
    "Rapper Shakespeare": "Act as Shakespeare but you are from the 21st century: ",
    "Gardener": "Act as professional gardener and assist the user in growing CBD-(legal!)-weed: "
}

        self.pre_prompt = self.behaviors["Default"]
        self.conversation_history = [{'role': 'system', 'content': self.pre_prompt}]
        self.conversation_history = [{'role': 'system', 'content': self.pre_prompt}]
        self.root = tk.Tk()
        self.root.title("JChat")
        self.center_window(self.root)
        self.root.resizable(0, 0)
        self.font_family = "Segoe UI Emoji"
        self.font_size = 12

        frame = tk.Frame(self.root)
        frame.grid(sticky="nsew", padx=10, pady=10)

        self.conversation = scrolledtext.ScrolledText(frame, wrap='word')
        self.conversation.configure(font=(self.font_family, self.font_size))
        self.conversation.grid(sticky="nsew")

        self.text_input = tk.StringVar()
        entry_field = tk.Entry(self.root, textvariable=self.text_input, font=(self.font_family, self.font_size))
        entry_field.bind('<Return>', self.send_message)
        entry_field.grid(sticky="we", padx=10)

        btn_frame = tk.Frame(self.root)
        btn_frame.grid(sticky="we", padx=10, pady=5)

        send_button = tk.Button(btn_frame, text="Send", command=self.send_message, font=(self.font_family, self.font_size))
        send_button.pack(side="left", padx=10, pady=10)

        clear_conversation_btn = tk.Button(btn_frame, text="Clear", command=self.clear_conversation,
                                           font=(self.font_family, self.font_size))
        clear_conversation_btn.pack(side="left", padx=10, pady=10)

        behavior_button = tk.Button(btn_frame, text="Behavior", command=self.change_behavior, font=(self.font_family, self.font_size))
        behavior_button.pack(side="left", padx=10, pady=10)

        exit_button = tk.Button(btn_frame, text="Exit", command=self.exit_app, font=(self.font_family, self.font_size))
        exit_button.pack(side="right", padx=10, pady=10)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_columnconfigure(1, weight=1)

    def center_window(self, window):
        window_width = 760
        window_height = 620
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 3) - (window_height // 2)
        window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def get_gpt_response(self, user_prompt):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + openai.api_key,
        }

        self.conversation_history.append({'role': 'user', 'content': user_prompt})

        data = {
            'model': 'gpt-3.5-turbo-16k-0613',
            'messages': self.conversation_history,
            'temperature': 0.7,
            'top_p': 0.9,
            'presence_penalty': 0.6,
            'frequency_penalty': 0.3,
        }

        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, data=json.dumps(data))
        return response

    def send_message(self, event=None):
        user_message = self.text_input.get()
        if user_message == 'exit':
            if messagebox.askokcancel("Quit", "Do you really want to quit?"):
                self.root.destroy()
        else:
            self.text_input.set('')
            self.conversation.insert(tk.END, "You: " + user_message + '\n\n')
            self.conversation_history.append({'role': 'user', 'content': user_message})

            def gpt_request():
                response = self.get_gpt_response(user_message)
                if response.status_code == 200:
                    completion = response.json()['choices'][0]['message']['content']
                    self.conversation.insert(tk.END, "JChat: " + completion + '\n\n')
                    self.conversation_history.append({'role': 'assistant', 'content': completion})
                    self.conversation.see(tk.END)
                else:
                    print("An error occurred:", response.text)

            threading.Thread(target=gpt_request).start()

    def clear_conversation(self):
        confirmed = messagebox.askyesno("Clear Conversation", "Are you sure you want to clear the conversation?")
        if confirmed:
            self.conversation.delete('1.0', tk.END)

    def exit_app(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.root.quit()

    def change_behavior(self):
        def select_behavior(behavior):
            self.pre_prompt = self.behaviors[behavior]
            self.conversation_history = [{'role': 'system', 'content': self.pre_prompt}]
            window.destroy()

        window = tk.Toplevel(self.root)
        window.title("Select Behavior")

        buttons = [tk.Button(window, text=name, command=lambda name=name: select_behavior(name)) for name in
                   self.behaviors.keys()]

        rows = round(len(buttons) ** 0.5)
        cols = len(buttons) // rows + (len(buttons) % rows > 0)

        for i, button in enumerate(buttons):
            button.grid(row=i // cols, column=i % cols, padx=10, pady=10, )

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = JChat()
    app.run()
