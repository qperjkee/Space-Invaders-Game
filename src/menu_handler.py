class MenuHandler:
    def __init__(self):
        from .menu import Menu
        self.menu = Menu()

    def show_end_menu(self, score):
        return self.menu.end_menu(round(score))

    def show_main_menu(self):
        return self.menu.main_menu()