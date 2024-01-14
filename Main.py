from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.core.audio import SoundLoader
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.image import Image

from kivy.clock import Clock
import random


class StartMenu(Screen):
    def __init__(self, **kwargs):
        super(StartMenu, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        backgroundImage = 'background/who1.png'
        self.game_name = Button(text=' ', font_size=100, size_hint=(None, None), size=(1200, 400))
        self.game_name.background_normal = backgroundImage
        
        names_input = TextInput(hint_text="Enter Name", multiline=False, font_size=60)
        self.name_input = names_input
        self.name_input.background_color = (250/255, 255/255, 250/255, 1) 

        self.enter_button = Button(text="Save", on_press=self.callback, font_size=60, height=50)
        self.enter_button.background_color = (180/255, 255/255, 100/255, 1) 

        self.start_button = Button(text="Join without name", on_press=self.go_to_game, font_size=60, height=50)
        self.start_button.background_color = (1/255, 255/255, 1/255, 1)

        layout.add_widget(self.game_name)
        layout.add_widget(names_input)
        layout.add_widget(self.enter_button)
        layout.add_widget(self.start_button)

        self.add_widget(layout)

    def go_to_game(self, instance):
        self.manager.get_screen('Button_In_Game').start_game()
        self.manager.current = 'Button_In_Game'

    def callback(self, instance):
        self.start_button.text = 'Join with name :' + ' ' + self.name_input.text

class ButtonInGame(Screen):
    def __init__(self, **kwargs):
        super(ButtonInGame, self).__init__(**kwargs)

        self.is_paused = False
        self.is_game_started = False

        layout = BoxLayout(orientation='vertical')
        self.footballers = ["alisson", "beckham", "de gea", "de bruyne", "del piero"
                            , "ronaldo", "messi", "mbappe", "modric", "ronaldinho"
                            , "kaka", "gerrard", "haaland", "van dijk", "kane"
                            , "neymar",  "lewandowski", "neuer", "ibrahimovic", "hazard"]  
        
        self.current_footballer = None

#GameLogics
        self.image = Image(source='', size_hint_y=None, size=(1200, 400))

        self.text_input = TextInput(multiline=False, size_hint_y=None, size=(1200, 150))

        self.answer_button = Button(text='Answer', on_press=self.check_answer, size_hint_y=None,size=(1200, 150), font_size=40)
        self.answer_button.background_color = (1/255, 255/255, 1/255, 1)
        self.new_game()
    
#ExtraButtons
        self.pause_button = Button(text='Pause', on_press=self.toggle_pause, size_hint_y=None, size=(1200, 50), font_size=20)
        self.pause_button.background_color = (255/255, 255/255, 1/255, 1)
        
        self.exit_button = Button(text='Exit', on_press=self.exit, size_hint_y=None, size=(1200, 50), font_size=20)
        self.exit_button.background_color = (255/255, 1/255, 1/255, 1)
        
        self.score_label = Label(text="Score : " + ' ', size_hint_y=None, size=(1200, 50))
        self.timer_label = Label(text="Time : 30", size_hint_y=None, size=(1200, 50))
        

        layout.add_widget(self.image)
        layout.add_widget(self.text_input)
        layout.add_widget(self.answer_button)
        layout.add_widget(self.pause_button)
        layout.add_widget(self.exit_button)
        layout.add_widget(self.score_label)
        layout.add_widget(self.timer_label)
        
        self.add_widget(layout)
        Clock.schedule_interval(self.update_timer, 1)

    def new_game(self):
        self.current_footballer = random.choice(self.footballers)
        self.image.source = f'image/{self.current_footballer}.png'  
        self.text_input.text = ''
        
    def check_answer(self, instance):
        user_input = self.text_input.text.lower()
        if user_input == self.current_footballer:
            self.new_game()
        else:
            self.answer_button.text = f'Incorrect, Try Again'

    def start_game(self):
        self.is_game_started = True

    def exit(self, instance):
        self.manager.current = 'start_menu'
        self.reset_timer()
        popup = Popup(title='Game Over', content=Label(text='Try Again Later'), size_hint=(None, None),
                      size=(400, 200))
        popup.open()
        
    def reset_timer(self):
        self.timer_label.text = "Time remaining: 30"

    def toggle_pause(self, instance):
        self.is_paused = not self.is_paused
        if self.pause_button.text == 'Pause':
            self.pause_button.text = 'Resume'
        else:
            self.pause_button.text = 'Pause'

    def update_timer(self, dt):
        if self.is_game_started and not self.is_paused:
            remaining_time = int(self.timer_label.text.split()[-1])
            if remaining_time > 0:
                remaining_time -= 1
                self.timer_label.text = f"Time remaining: {remaining_time}"
            else:
                self.show_game_over_popup()
    

    def show_game_over_popup(self):
        self.is_game_started = False
        self.reset_timer()
        popup = Popup(title='Time Up', content=Label(text="Your Score :" + f"{score}"), size_hint=(None, None),
                      size=(400, 200))
        popup.open()
        self.exit


class GuessFootballerApp(App):
    def build(self):

        self.sound = SoundLoader.load('OleOla.mp3')
        if self.sound:
            self.sound.volume = 1
            self.sound.loop = True
            self.sound.play()

        sm = ScreenManager()
        sm.add_widget(StartMenu(name='start_menu'))
        sm.add_widget(ButtonInGame(name='Button_In_Game'))
        return sm
    

if __name__ == '__main__':
    GuessFootballerApp().run()
