from kivy.animation import Animation
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout

Builder.load_file('animation.kv')


class MyLayout(FloatLayout):
    @staticmethod
    def animate_it(widget, *args):
        animate = Animation(background_color=(0, 0, 1, 1), duration=2.9)
        animate += Animation(opacity=0, duration=0.5)

        animate.start(widget)

    @staticmethod
    def calculate_animation_value(a, b, t):
        if a is None or b is None:
            return 0
        return (a * (1. - t)) + (b * t)


class MyApp(App):
    def build(self):
        layout = MyLayout()

        button = Button(
            text="Вземете ме на стаж! Моля :).",
            font_size=45,
            size_hint=(None, None),
            width=900,
            height=900,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            background_normal="avatar.png",
            background_color=(0.2, 0.2, 0.2, 1)
        )

        button.bind(on_press=lambda instance: layout.animate_it(button))

        layout.add_widget(button)

        return layout


if __name__ == '__main__':
    MyApp().run()
