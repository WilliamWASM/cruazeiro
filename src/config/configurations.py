from ..gui.views.cards.base_card import *
from ..gui.views.cards.combo_box_card import *
from ..gui.views.cards.extra_button_card import *
from ..resources.styles.light import *
from ..resources.styles.dark import *
from ..gui.controllers.sections.campus_controller import *
from ..gui.managers.file_manager import *
PROJECT_CONFIGS = {
            "SiteOps":{
                "Universities":[
                    {"type": "base","title":"Unifatecie","description":"Utilizado para gerar planilha da Unifatecie"},
                    {"type": "base","title":"Kroton Lote","description":"Utilizado para gerar planilha da Unifatecie"}
                ],
                "Campus":[
                    {"type": "extra","title":"Campus","description":"Utilizado para gerar planilha da Unifatecie"},
                    {"type": "extra","title":"Uniasselv EaD","description":"Utilizado para gerar planilha da Unifatecie"},
                    {"type": "extra","title":"Uniasselvi Presencial","description":"Utilizado para gerar planilha da Unifatecie"}
                ],
                "Cruzeiro":[
                    {"type": "base","title":"Cruzeiro Técnico","description":"Utilizado para gerar planilha da Unifatecie"},
                    {"type": "base","title":"Cruzeiro Pós Graduação","description":"Utilizado para gerar planilha da Unifatecie"},
                    {"type": "base","title":"Cruzeiro Graduação EaD","description":"Utilizado para gerar planilha da Unifatecie"},
                ],
                "Utilities": [
                    {"type": "combo","title":"Dividir tabela","description":"Utilizado para gerar planilha da Unifatecie","items": [1,2,3,4,5,6,7,8,9]},
                    {"type": "base","title":"Exp para Msp","description":"Utilizado para gerar planilha da Unifatecie"},
                    {"type": "base","title":"Csv para Excel","description":"Utilizado para gerar planilha da Unifatecie"},
                ]
            },
            "Comercial":{
                "Universities":[
                    {"type": "base","title":"Unifatecie","description":"Utilizado para gerar planilha da Unifatecie"},
                    {"type": "base","title":"Kroton Lote","description":"Utilizado para gerar planilha da Unifatecie"}
                ],
                "Campus":[
                    {"type": "base","title":"Campus","description":"Utilizado para gerar planilha da Unifatecie"},
                    {"type": "base","title":"Uniasselv EaD","description":"Utilizado para gerar planilha da Unifatecie"},
                    {"type": "base","title":"Uniasselvi Presencial","description":"Utilizado para gerar planilha da Unifatecie"}
                ],
                "Utilities": [
                    {"type": "combo","title":"Dividir tabela","description":"Utilizado para gerar planilha da Unifatecie","items": [1,2,3,4,5,6,7,8,9]},
                    {"type": "base","title":"Exp para Msp","description":"Utilizado para gerar planilha da Unifatecie"},
                    {"type": "base","title":"Csv para Excel","description":"Utilizado para gerar planilha da Unifatecie"},
                ]
            }
        }

CARD_TYPES = {
        "base": BaseCard,
        "combo": ComboBoxCard,
        "extra": ExtraButtonCard,
    }

PROJECT_STYLES = {
    'Comercial': {
        'light': ComercialLightStyles,
        'dark': ComercialDarkStyles
    },
    'SiteOps': {
        'light': SiteOpsLightStyles, 
        'dark': SiteOpsDarkStyles
    }
}

CARD_ACTIONS = {
    "SiteOps": {
        "Campus": {
            "button_texts": ["Selecione MSP Polos", "Selecione EXP campus"],
            "generate_action": lambda data: CampusController().process_campus(data),
            "generate_type": "normal",
            "requires_input" : False,
            "inputs": None,
            "save_type": "save_file",
            "section": "campus"
        },
        "Uniasselvi EaD": {
            "button_texts": ["Selecione Planilha Campus", "Selecione EXP campus"],
            "generate_action": lambda data: CampusController().process_uniasselvi_ead(data),
            "generate_type": "normal",
            "requires_input" : False,
            "inputs": None,
            "save_type": "save_file",
            "section": "campus"
        },
        "Uniasselvi Presencial": {
            "button_texts": ["Selecione Planilha Campus", "Selecione EXP campus"],
            "generate_action": lambda data: CampusController().process_uniasselvi_presencial(data),
            "generate_type": "normal",
            "requires_input" : False,
            "inputs": None,
            "save_type": "save_file", 
            "section": "campus"
        }
    }
}

