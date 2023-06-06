from kivymd.app import MDApp

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = ("DeepPurple")

app = MainApp()
app.run()