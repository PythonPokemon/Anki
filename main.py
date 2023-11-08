from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
import sqlite3

class AnkiApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        create_card_button = Button(text='Karte erstellen')
        create_card_button.bind(on_press=self.create_card)
        self.layout.add_widget(create_card_button)

        show_cards_button = Button(text='Karten anzeigen')
        show_cards_button.bind(on_press=self.show_cards)
        self.layout.add_widget(show_cards_button)

        delete_card_button = Button(text='Karte löschen')
        delete_card_button.bind(on_press=self.delete_card)
        self.layout.add_widget(delete_card_button)

        edit_card_button = Button(text='Karte bearbeiten')
        edit_card_button.bind(on_press=self.edit_card)
        self.layout.add_widget(edit_card_button)

        self.conn = sqlite3.connect('anki_cards.db')
        self.create_table()

        return self.layout

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                front TEXT NOT NULL,
                back TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def create_card(self, instance):
        self.layout.clear_widgets()

        front_input = TextInput(hint_text='Vorderseite der Karte')
        back_input = TextInput(hint_text='Rückseite der Karte')

        save_button = Button(text='Karte speichern')
        save_button.bind(on_press=lambda instance: self.save_card(front_input.text, back_input.text))

        self.layout.add_widget(front_input)
        self.layout.add_widget(back_input)
        self.layout.add_widget(save_button)

    def show_cards(self, instance):
        self.layout.clear_widgets()
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, front, back FROM cards')
        rows = cursor.fetchall()

        for id, front, back in rows:
            card_label = Label(text=f"ID: {id} - Frage: {front}\nAntwort: {back}")
            self.layout.add_widget(card_label)

    def delete_card(self, instance):
        self.layout.clear_widgets()
        # Füge die Löschlogik hier ein

    def edit_card(self, instance):
        self.layout.clear_widgets()
        # Füge die Bearbeitungslogik hier ein

    def save_card(self, front, back):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO cards (front, back) VALUES (?, ?)', (front, back))
        self.conn.commit()
        self.show_cards(None)

if __name__ == '__main__':
    AnkiApp().run()
