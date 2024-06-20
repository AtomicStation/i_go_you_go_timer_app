from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

class WorkoutTimeApp(App):
    def build(self):
        self.rounds = 0
        self.current_round = 0
        self.timer = 0
        self.is_counting_down = False
        self.ready_time = 10
        self.is_ready = True
        self.running = False

        self.layout = BoxLayout(orientation='vertical')

        self.label = Label(text='Enter number of rounds:', font_size='20sp')
        self.layout.add_widget(self.label)

        self.round_input = TextInput(multiline=False, input_filter='int')
        self.layout.add_widget(self.round_input)

        self.start_button = Button(text="Start", on_press=self.start_workout)
        self.layout.add_widget(self.start_button)

        self.timer_label = Label(text="Ready", font_size='40sp')
        self.layout.add_widget(self.timer_label)

        self.done_button = Button(text="Done", on_press=self.done_round)
        self.done_button.disabled = True
        self.layout.add_widget(self.done_button)

        self.reset_button = Button(text="Reset", on_press=self.reset)
        self.layout.add_widget(self.reset_button)

        return self.layout
    
    def start_workout(self, instance):
        self.rounds = int(self.round_input.text)
        self.current_round = 0
        self.timer = 0
        self.is_counting_down = False
        self.is_ready = True
        self.running = True
        self.start_button.disabled = True
        self.done_button.disabled = False
        Clock.schedule_interval(self.update_timer, 1)

    def reset(self, instance):
        self.start_button.disabled = False
        self.done_button.disabled = True
        self.running = False
        self.timer_label.text = "Ready"

    def update_timer(self, dt):
        if not self.running:
            return False
        
        if self.is_ready:
            if self.ready_time > 0:
                self.timer_label.text = f"Starting in: {self.ready_time}"
                self.ready_time -= 1
            else:
                self.is_ready = False
                self.timer_label.text = f"I GO - Round {self.current_round + 1}: {self.timer}"
        else:
            if self.is_counting_down:
                if self.timer > 0:
                    self.timer_label.text = f"YOU GO (rest) - Round {self.current_round + 1}: {self.timer}"
                    self.timer -= 1
                else:
                    self.is_counting_down = False
                    self.current_round += 1
                    if self.current_round >= self.rounds:
                        self.timer_label.text = "Workout Complete!"
                        self.running = False
                        self.done_button.disabled = True
                        self.start_button.disabled = False
                        Clock.unschedule(self.update_timer)
                    else:
                        self.ready_time = 10
                        self.is_ready = True
            else:
                self.timer += 1
                self.timer_label.text = f"I GO - Round {self.current_round + 1}: {self.timer}"

    def done_round(self, instance):
        self.is_counting_down = True

if __name__ == "__main__":
    WorkoutTimeApp().run()