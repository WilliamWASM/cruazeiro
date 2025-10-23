class ComercialDarkStyles:
    COLOR1 = "#0C0C0D" #default background 
    COLOR2 = "#F22786" #card background
    COLOR3 = "#FF5BB5" #generate bttn background
    COLOR4 = "#F1F1F5" # texts color
    COLOR5 = "#F1F1F5" # buttons color
    COLOR6 = "#CF4A93" # hover generate
    COLOR7 = "#555555" #hover buttons
    COLOR8 = "#B91F67" # hover menu item
    COLOR9 = "#EB0C74" # pressed menuitem

    @staticmethod
    def card():
        card = {
            'card': f"""
                background-color: {ComercialDarkStyles.COLOR2};
                color: {ComercialDarkStyles.COLOR4};
                border-radius: 20px;
            """,
            'generate_btn': f"""
                QPushButton {{
                    background-color: {ComercialDarkStyles.COLOR3};
                    color: {ComercialDarkStyles.COLOR4};
                    border-radius: 10px;
                }}
                QPushButton:hover{{
                    background-color: {ComercialDarkStyles.COLOR6};
                }}
            """,
            'ask_button' : f"""
                QPushButton {{
                    background-color: {ComercialDarkStyles.COLOR1};
                    color: {ComercialDarkStyles.COLOR2};
                    border-radius: 12px;
                }}
            QPushButton:hover{{
                background-color: {ComercialDarkStyles.COLOR7};
            }}
            """,
            'button' : f"""
                QPushButton {{
                    background-color: {ComercialDarkStyles.COLOR1};
                    color: {ComercialDarkStyles.COLOR5};
                    border-radius: 10px;
                }}
                QPushButton:hover{{
                    background-color: {ComercialDarkStyles.COLOR7};
                }}
            """,
            'combo_box' : f"""
                QComboBox{{
                    background-color: transparent;
                    color: {ComercialDarkStyles.COLOR4};

                }}
                QComboBox QAbstractItemView {{
                    background-color: transparent;        
                    color: {ComercialDarkStyles.COLOR4};                   
                    selection-background-color: {ComercialDarkStyles.COLOR8};
                }}
            """
        }
        return card
    
    @staticmethod
    def menu_item():
        menu_item = {
            'default' : f"""
                background-color: {ComercialDarkStyles.COLOR2};
                color: {ComercialDarkStyles.COLOR4};
            """,
            'selected' : f"""
                QFrame[project="Comercial"] {{
                    background-color: {ComercialDarkStyles.COLOR9};
                    border-right: 2px solid {ComercialDarkStyles.COLOR1};
                }} 
            """,
            'hover': f"""
                background-color: {ComercialDarkStyles.COLOR8};
            """
        }
        return menu_item
        
    @staticmethod
    def card_area():
        return f"""
        background-color: {ComercialDarkStyles.COLOR1}
        """

    @staticmethod
    def project_menu_area():
        return f"""
        QWidget[project_menu="Comercial"]{{
            background-color: {ComercialDarkStyles.COLOR2};
            QComboBox{{
                background-color: transparent;
                color: {ComercialDarkStyles.COLOR4};
            }}
        }}
        QComboBox QAbstractItemView {{
            background-color: transparent;        
            color: {ComercialDarkStyles.COLOR4};                   
            selection-background-color: {ComercialDarkStyles.COLOR8};
        }}
        """
    
    @staticmethod
    def default_menu_area():
        return f"""
            background-color: {ComercialDarkStyles.COLOR2};
            QComboBox{{
                background-color: transparent;
                color: {ComercialDarkStyles.COLOR4};
            }}
            QComboBox QAbstractItemView {{
            j    background-color: transparent;        
                color: {ComercialDarkStyles.COLOR4};                   
                selection-background-color: {ComercialDarkStyles.COLOR8};
            }}
            """

class SiteOpsDarkStyles:
    COLOR1 = "#0C0C0D" #default background 
    COLOR2 = "#304FFE" #card background
    COLOR3 = "#333333" #generate bttn background
    COLOR4 = "#F5F5F5" # texts color
    COLOR5 = "#F5F5F5" # buttons color
    COLOR6 = "#202020" # hover generate
    COLOR7 = "#BDA8B0" #hover buttons
    COLOR8 = "#273FC5" # hover menu item
    COLOR9 = "#263CB6" # pressed menuitem

    @staticmethod
    def card():
        card = {
            'card': f"""
                background-color: {SiteOpsDarkStyles.COLOR2};
                color: {SiteOpsDarkStyles.COLOR4};
                border-radius: 20px;
            """,
            'generate_btn': f"""
                QPushButton {{
                    background-color: {SiteOpsDarkStyles.COLOR3};
                    color: {SiteOpsDarkStyles.COLOR4};
                    border-radius: 10px;
                }}
                QPushButton:hover{{
                    background-color: {SiteOpsDarkStyles.COLOR6};
                }}
            """,
            'ask_button' : f"""
                QPushButton {{
                    background-color: {SiteOpsDarkStyles.COLOR1};
                    color: {SiteOpsDarkStyles.COLOR2};
                    border-radius: 12px;
                }}
            QPushButton:hover{{
                background-color: {SiteOpsDarkStyles.COLOR7};
            }}
            """,
            'button' : f"""
                QPushButton {{
                    background-color: {SiteOpsDarkStyles.COLOR1};
                    color: {SiteOpsDarkStyles.COLOR5};
                    border-radius: 10px;
                }}
                QPushButton:hover{{
                    background-color: {SiteOpsDarkStyles.COLOR7};
                }}
            """,
            'combo_box' : f"""
                QComboBox{{
                    background-color: transparent;
                    color: {SiteOpsDarkStyles.COLOR4};

                }}
                QComboBox QAbstractItemView {{
                    background-color: transparent;        
                    color: {SiteOpsDarkStyles.COLOR4};                   
                    selection-background-color: {SiteOpsDarkStyles.COLOR8};
                }}
            """
        }
        return card
    
    @staticmethod
    def menu_item():
        menu_item = {
            'default' : f"""
                background-color: {SiteOpsDarkStyles.COLOR2};
                color: {SiteOpsDarkStyles.COLOR4};
            """,
            'selected' : f"""
                QFrame[project="SiteOps"] {{
                    background-color: {SiteOpsDarkStyles.COLOR9};
                    border-right: 2px solid {SiteOpsDarkStyles.COLOR1};
                }} 
            """,
            'hover': f"""
                background-color: {SiteOpsDarkStyles.COLOR8};
            """
        }
        return menu_item

    @staticmethod
    def card_area():
        return f"""
        background-color: {SiteOpsDarkStyles.COLOR1}
        """

    @staticmethod
    def project_menu_area():
        return f"""
        QWidget[project_menu="SiteOps"]{{
            background-color: {SiteOpsDarkStyles.COLOR2};
            QComboBox{{
                background-color: transparent;
                color: {SiteOpsDarkStyles.COLOR4};
            }}
        }}
        QComboBox QAbstractItemView {{
            background-color: transparent;        
            color: {SiteOpsDarkStyles.COLOR4};                   
            selection-background-color: {SiteOpsDarkStyles.COLOR8};
        }}
        """
    
    @staticmethod
    def default_menu_area():
        return f"""
            background-color: {SiteOpsDarkStyles.COLOR2};
            QComboBox{{
                background-color: transparent;
                color: {SiteOpsDarkStyles.COLOR4};
            }}
            QComboBox QAbstractItemView {{
            j    background-color: transparent;        
                color: {SiteOpsDarkStyles.COLOR4};                   
                selection-background-color: {SiteOpsDarkStyles.COLOR8};
            }}
            """