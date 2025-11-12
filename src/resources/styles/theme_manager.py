from ...config.configurations import PROJECT_STYLES
class ThemeManager:
    def __init__(self):
        self.current_theme = 'light'  
    
    def toggle_theme(self):
        self.current_theme = 'dark' if self.current_theme == 'light' else 'light'
        return self.current_theme