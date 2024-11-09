from kivy.uix.image import Image
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


class AvatarApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        avatar_image = Image(source='avatar.png')

        layout.add_widget(avatar_image)

        return layout


if __name__ == '__main__':
    AvatarApp().run()
