import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import google.generativeai as genai
import os
from dotenv import load_dotenv

class GeminiChat(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        load_dotenv()
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)

        self.label = Label(text='Gemini AI Chat', font_size='20sp', size_hint=(1, 0.1))
        self.add_widget(self.label)

        self.chat_history = Label(text='', size_hint=(1, 0.6), halign='left', valign='top')
        self.chat_history.bind(size=self.chat_history.setter('text_size'))
        self.add_widget(self.chat_history)

        self.input_box = TextInput(hint_text='Type your message...', multiline=False, size_hint=(1, 0.1))
        self.add_widget(self.input_box)

        self.send_btn = Button(text='Send', size_hint=(1, 0.1))
        self.send_btn.bind(on_press=self.send_message)
        self.add_widget(self.send_btn)

        self.history = []

    def send_message(self, instance):
        user_text = self.input_box.text.strip()
        if not user_text:
            return
        self.history.append({'role': 'user', 'content': user_text})
        self.chat_history.text += f"\nYou: {user_text}"
        self.input_box.text = ''
        try:
            model = genai.GenerativeModel('gemini-pro')
            convo = model.start_chat(history=[{"role": msg["role"], "parts": [msg["content"]]} for msg in self.history])
            convo.send_message(user_text)
            reply = convo.last.text.strip()
            self.history.append({'role': 'assistant', 'content': reply})
            self.chat_history.text += f"\nGemini: {reply}"
        except Exception as e:
            self.chat_history.text += f"\n[Error]: {e}"

class GeminiKivyApp(App):
    def build(self):
        return GeminiChat()

if __name__ == '__main__':
    GeminiKivyApp().run()
