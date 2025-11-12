class ComercialLightStyles:
    COLOR1 = "#FFE5F0" #default background 
    COLOR2 = "#F22786" #card background
    COLOR3 = "#FF5BB5" #generate bttn background
    COLOR4 = "#F1F1F5" # texts color
    COLOR5 = "#001219" # buttons color
    COLOR6 = "#CF4A93" # hover generate
    COLOR7 = "#D3BBC5" #hover buttons
    COLOR8 = "#B91F67" # hover menu item
    COLOR9 = "#EB0C74" # pressed menuitem

    @staticmethod
    def card():
        card = {
            'card': f"""
                background-color: {ComercialLightStyles.COLOR2};
                color: {ComercialLightStyles.COLOR4};
                border-radius: 20px;
            """,
            'generate_btn': f"""
                QPushButton {{
                    background-color: {ComercialLightStyles.COLOR3};
                    color: {ComercialLightStyles.COLOR4};
                    border-radius: 10px;
                }}
                QPushButton:hover{{
                    background-color: {ComercialLightStyles.COLOR6};
                }}
            """,
            'ask_button' : f"""
                QPushButton {{
                    background-color: {ComercialLightStyles.COLOR1};
                    color: {ComercialLightStyles.COLOR2};
                    border-radius: 12px;
                }}
            QPushButton:hover{{
                background-color: {ComercialLightStyles.COLOR7};
            }}
            """,
            'button' : f"""
                QPushButton {{
                    background-color: {ComercialLightStyles.COLOR1};
                    color: {ComercialLightStyles.COLOR5};
                    border-radius: 10px;
                }}
                QPushButton:hover{{
                    background-color: {ComercialLightStyles.COLOR7};
                }}
            """,
            'combo_box' : f"""
                QComboBox{{
                    background-color: transparent;
                    color: {ComercialLightStyles.COLOR4};

                }}
                QComboBox QAbstractItemView {{
                    background-color: transparent;        
                    color: {ComercialLightStyles.COLOR4};                   
                    selection-background-color: {ComercialLightStyles.COLOR8};
                }}
            """
        }
        return card
    
    @staticmethod
    def card_title():
        return f"""
                QLabel[label="title_card"] {{
                    font-size: 18px;
                    font-weight: bold;
                }}
            """
    
    @staticmethod
    def menu_item():
        menu_item = {
            'default' : f"""
                background-color: {ComercialLightStyles.COLOR2};
                color: {ComercialLightStyles.COLOR4};
            """,
            'selected' : f"""
                QFrame[project="Comercial"] {{
                    background-color: {ComercialLightStyles.COLOR9};
                    border-right: 2px solid {ComercialLightStyles.COLOR1};
                }} 
            """,
            'hover': f"""
                background-color: {ComercialLightStyles.COLOR8};
            """
        }
        return menu_item
        
    @staticmethod
    def card_area():
        return f"""
        background-color: {ComercialLightStyles.COLOR1}
        """

    @staticmethod
    def project_menu_area():
        return f"""
        QWidget[project_menu="Comercial"]{{
            background-color: {ComercialLightStyles.COLOR2};
            QComboBox{{
                background-color: transparent;
                color: {ComercialLightStyles.COLOR4};
            }}
        }}
        QComboBox QAbstractItemView {{
            background-color: transparent;        
            color: {ComercialLightStyles.COLOR4};                   
            selection-background-color: {ComercialLightStyles.COLOR8};
        }}
        """
    
    @staticmethod
    def default_menu_area():
        return f"""
            background-color: {ComercialLightStyles.COLOR2};
            QComboBox{{
                background-color: transparent;
                color: {ComercialLightStyles.COLOR4};
            }}
            QComboBox QAbstractItemView {{
                background-color: transparent;        
                color: {ComercialLightStyles.COLOR4};                   
                selection-background-color: {ComercialLightStyles.COLOR8};
            }}

            """

class SiteOpsLightStyles:
    COLOR1 = "#F5F5F5" #default background 
    COLOR2 = "#304FFE" #card background
    COLOR3 = "#333333" #generate bttn background
    COLOR4 = "#F5F5F5" # texts color
    COLOR5 = "#001219" # buttons color
    COLOR6 = "#202020" # hover generate
    COLOR7 = "#BDA8B0" #hover buttons
    COLOR8 = "#273FC5" # hover menu item
    COLOR9 = "#263CB6" # pressed menuitem

    @staticmethod
    def card():
        card = {
            'card': f"""
                background-color: {SiteOpsLightStyles.COLOR2};
                color: {SiteOpsLightStyles.COLOR4};
                border-radius: 20px;
            """,
            'generate_btn': f"""
                QPushButton {{
                    background-color: {SiteOpsLightStyles.COLOR3};
                    color: {SiteOpsLightStyles.COLOR4};
                    border-radius: 10px;
                }}
                QPushButton:hover{{
                    background-color: {SiteOpsLightStyles.COLOR6};
                }}
            """,
            'ask_button' : f"""
                QPushButton {{
                    background-color: {SiteOpsLightStyles.COLOR1};
                    color: {SiteOpsLightStyles.COLOR2};
                    border-radius: 12px;
                }}
            QPushButton:hover{{
                background-color: {SiteOpsLightStyles.COLOR7};
            }}
            """,
            'button' : f"""
                QPushButton {{
                    background-color: {SiteOpsLightStyles.COLOR1};
                    color: {SiteOpsLightStyles.COLOR5};
                    border-radius: 10px;
                }}
                QPushButton:hover{{
                    background-color: {SiteOpsLightStyles.COLOR7};
                }}
            """,
            'combo_box' : f"""
                QComboBox{{
                    background-color: transparent;
                    color: {SiteOpsLightStyles.COLOR4};

                }}
                QComboBox QAbstractItemView {{
                    background-color: transparent;        
                    color: {SiteOpsLightStyles.COLOR4};                   
                    selection-background-color: {SiteOpsLightStyles.COLOR8};
                }}
            """
        }
        return card
    
    @staticmethod
    def card_title():
        return f"""
                QLabel[label="title_card"] {{
                    font-size: 18px;
                    font-weight: bold;
                }}
            """
    
    @staticmethod
    def menu_item():
        menu_item = {
            'default' : f"""
                background-color: {SiteOpsLightStyles.COLOR2};
                color: {SiteOpsLightStyles.COLOR4};
            """,
            'selected' : f"""
                QFrame[project="SiteOps"] {{
                    background-color: {SiteOpsLightStyles.COLOR9};
                    border-right: 2px solid {SiteOpsLightStyles.COLOR1};
                }} 
            """,
            'hover': f"""
                background-color: {SiteOpsLightStyles.COLOR8};
            """
        }
        return menu_item

    @staticmethod
    def card_area():
        return f"""
        background-color: {SiteOpsLightStyles.COLOR1}
        """

    @staticmethod
    def project_menu_area():
        return f"""
        QWidget[project_menu="SiteOps"]{{
            background-color: {SiteOpsLightStyles.COLOR2};
            QComboBox{{
                background-color: transparent;
                color: {SiteOpsLightStyles.COLOR4};
            }}
        }}
        QComboBox QAbstractItemView {{
            background-color: transparent;        
            color: {SiteOpsLightStyles.COLOR4};                   
            selection-background-color: {SiteOpsLightStyles.COLOR8};
        }}
        """
    
    @staticmethod
    def default_menu_area():
        return f"""
            background-color: {SiteOpsLightStyles.COLOR2};
            QComboBox{{
                background-color: transparent;
                color: {SiteOpsLightStyles.COLOR4};
            }}
            QComboBox QAbstractItemView {{
                background-color: transparent;        
                color: {SiteOpsLightStyles.COLOR4};                   
                selection-background-color: {SiteOpsLightStyles.COLOR8};
            }}
            """