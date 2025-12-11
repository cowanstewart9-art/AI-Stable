from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from manager import AIManager
import random
import time

# Mock AI function for demonstration
def dummy_ai_function(input_data):
    if "crash" in input_data:
        raise ValueError("Intentional Crash for Testing")
    time.sleep(1)
    return f"Processed: {input_data} (AI Result)"

class AIManagerApp(App):
    def build(self):
        self.manager = AIManager()
        self.manager.register_ai("DummyAI", dummy_ai_function)

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Input Area
        self.input_text = TextInput(hint_text="Enter input for AI (type 'crash' to test error handling)", size_hint=(1, 0.1))
        layout.add_widget(self.input_text)

        # Buttons
        btn_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)
        btn_run = Button(text="Run AI")
        btn_run.bind(on_press=self.run_ai)
        btn_layout.add_widget(btn_run)

        btn_refresh = Button(text="Refresh Logs")
        btn_refresh.bind(on_press=self.update_logs)
        btn_layout.add_widget(btn_refresh)

        layout.add_widget(btn_layout)

        # Log Display
        self.log_display = Label(text="Logs will appear here...", size_hint_y=None)
        self.log_display.bind(texture_size=self.log_display.setter('size'))

        scroll = ScrollView(size_hint=(1, 0.8))
        scroll.add_widget(self.log_display)
        layout.add_widget(scroll)

        return layout

    def run_ai(self, instance):
        input_data = self.input_text.text
        self.manager.execute_ai("DummyAI", input_data)
        self.update_logs(None)

    def update_logs(self, instance):
        logs = self.manager.get_history()
        log_text = ""
        for log in logs:
            # Format: [Timestamp] [Level] Message
            log_text += f"[{log[1]}] [{log[2]}] {log[4]}\n"
            if log[2] == "ERROR":
                 log_text += f"Details: {log[5]}\n"
            log_text += "-"*20 + "\n"
        self.log_display.text = log_text

if __name__ == '__main__':
    AIManagerApp().run()
