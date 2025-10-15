class ComercialStyles:

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
                background-color: {ComercialStyles.COLOR2};
                color: {ComercialStyles.COLOR4};
                border-radius: 20px;
            """,
            'generate_btn': f"""
                QPushButton {{
                    background-color: {ComercialStyles.COLOR3};
                    color: {ComercialStyles.COLOR4};
                    border-radius: 10px;
                }}
                QPushButton:hover{{
                    background-color: {ComercialStyles.COLOR6};
                }}
            """,
            'ask_button' : f"""
                QPushButton {{
                    background-color: {ComercialStyles.COLOR1};
                    color: {ComercialStyles.COLOR2};
                    border-radius: 12px;
                }}
            QPushButton:hover{{
                background-color: {ComercialStyles.COLOR7};
            }}
            """,
            'button' : f"""
                QPushButton {{
                    background-color: {ComercialStyles.COLOR1};
                    color: {ComercialStyles.COLOR5};
                    border-radius: 10px;
                }}
                QPushButton:hover{{
                    background-color: {ComercialStyles.COLOR7};
                }}
            """,
            'combo_box' : f"""
                QComboBox{{
                    background-color: transparent;
                    color: {ComercialStyles.COLOR4};

                }}
                QComboBox QAbstractItemView {{
                    background-color: transparent;        
                    color: {ComercialStyles.COLOR4};                   
                    selection-background-color: {ComercialStyles.COLOR8};
                }}
            """
        }

        return card
    
    @staticmethod
    def menu_item():
        menu_item = {
            'default' : f"""
                background-color: {ComercialStyles.COLOR2};
                color: {ComercialStyles.COLOR4};
            """,
            'selected' : f"""
                QFrame[menu="item"] {{
                    background-color: {ComercialStyles.COLOR9};
                    border-right: 2px solid {ComercialStyles.COLOR1};
                }} 
            """,
            'hover': f"""
                background-color: {ComercialStyles.COLOR8};
            """
        }
        return menu_item
        
    

    @staticmethod
    def card_area():
        return f"""
        background-color: {ComercialStyles.COLOR1}
        """

    @staticmethod
    def project_menu_area():
        return f"""
        QWidget[project_menu="Comercial"]{{
            background-color: {ComercialStyles.COLOR2};
            QComboBox{{
                background-color: transparent;
                color: {ComercialStyles.COLOR4};
            }}
        }}
        QComboBox QAbstractItemView {{
            background-color: transparent;        
            color: {ComercialStyles.COLOR4};                   
            selection-background-color: {ComercialStyles.COLOR8};
        }}
        """
    
    @staticmethod
    def default_menu_area():
        return f"""
            background-color: {ComercialStyles.COLOR2};
            QComboBox{{
                background-color: transparent;
                color: {ComercialStyles.COLOR4};
            }}
            QComboBox QAbstractItemView {{
            j    background-color: transparent;        
                color: {ComercialStyles.COLOR4};                   
                selection-background-color: {ComercialStyles.COLOR8};
            }}
            """

class SiteOpsStyles:
    COLOR1 = "#F5F5F5" #default background 
    COLOR2 = "#304FFE" #card background
    COLOR3 = "#333333" #generate bttn background
    COLOR4 = "#000000" # texts color
    COLOR5 = "#F5F5F5" # buttons color
    COLOR6 = "#202020" # hover generate
    COLOR7 = "#BDA8B0" #hover buttons
    COLOR8 = "#273FC5" # hover menu item
    COLOR9 = "#19277A" # pressed menuitem

    @staticmethod
    def card():
        card = {
            'card': f"""
                background-color: {SiteOpsStyles.COLOR2};
                color: {SiteOpsStyles.COLOR4};
                border-radius: 20px;
            """,
            'generate_btn': f"""
                QPushButton {{
                    background-color: {SiteOpsStyles.COLOR3};
                    color: {SiteOpsStyles.COLOR4};
                    border-radius: 10px;
                }}
                QPushButton:hover{{
                    background-color: {SiteOpsStyles.COLOR6};
                }}
            """,
            'ask_button' : f"""
                QPushButton {{
                    background-color: {SiteOpsStyles.COLOR1};
                    color: {SiteOpsStyles.COLOR2};
                    border-radius: 12px;
                }}
            QPushButton:hover{{
                background-color: {SiteOpsStyles.COLOR7};
            }}
            """,
            'button' : f"""
                QPushButton {{
                    background-color: {SiteOpsStyles.COLOR1};
                    color: {SiteOpsStyles.COLOR5};
                    border-radius: 10px;
                }}
                QPushButton:hover{{
                    background-color: {SiteOpsStyles.COLOR7};
                }}
            """,
            'combo_box' : f"""
                QComboBox{{
                    background-color: transparent;
                    color: {SiteOpsStyles.COLOR4};

                }}
                QComboBox QAbstractItemView {{
                    background-color: transparent;        
                    color: {SiteOpsStyles.COLOR4};                   
                    selection-background-color: {SiteOpsStyles.COLOR8};
                }}
            """
        }

        return card
    
    @staticmethod
    def menu_item():
        menu_item = {
            'default' : f"""
                background-color: {SiteOpsStyles.COLOR2};
                color: {SiteOpsStyles.COLOR4};
            """,
            'selected' : f"""
                QFrame[menu="item"] {{
                    background-color: {SiteOpsStyles.COLOR9};
                    border-right: 2px solid {SiteOpsStyles.COLOR1};
                }} 
            """,
            'hover': f"""
                background-color: {SiteOpsStyles.COLOR8};
            """
        }
        return menu_item
        
    

    @staticmethod
    def card_area():
        return f"""
        background-color: {SiteOpsStyles.COLOR1}
        """

    @staticmethod
    def project_menu_area():
        return f"""
        QWidget[project_menu="SiteOps"]{{
            background-color: {SiteOpsStyles.COLOR2};
            QComboBox{{
                background-color: transparent;
                color: {SiteOpsStyles.COLOR4};
            }}
        }}
        QComboBox QAbstractItemView {{
            background-color: transparent;        
            color: {SiteOpsStyles.COLOR4};                   
            selection-background-color: {SiteOpsStyles.COLOR8};
        }}
        """
    
    @staticmethod
    def default_menu_area():
        return f"""
            background-color: {SiteOpsStyles.COLOR2};
            QComboBox{{
                background-color: transparent;
                color: {SiteOpsStyles.COLOR4};
            }}
            QComboBox QAbstractItemView {{
            j    background-color: transparent;        
                color: {SiteOpsStyles.COLOR4};                   
                selection-background-color: {SiteOpsStyles.COLOR8};
            }}
            """