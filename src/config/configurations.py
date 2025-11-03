from ..gui.views.cards.base_card import *
from ..gui.views.cards.combo_box_card import *
from ..gui.views.cards.extra_button_card import *
from ..resources.styles.light import *
from ..resources.styles.dark import *
from ..gui.controllers.sections.campus_controller import *
from ..gui.controllers.sections.cruzeiro_controller import *
from ..gui.controllers.sections.unversities_controller import *
from ..gui.controllers.sections.utilities_controller import *
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
        },
        "Unifatecie": {
            "button_texts": ["Selecione Ofertas IES"],
            "generate_action": lambda data: UniversitiesController().process_unifatecie(data),
            "generate_type": "normal",
            "requires_input" : True,
            "inputs": ["OSC","Data End"],
            "save_type": "save_file",
            "section": "universities"
        },
        "Kroton Lote": {
            "button_texts": ["Selecione Ofertas IES"],
            "generate_action": lambda data: UniversitiesController().process_kroton_lote(data),
            "generate_type": "normal",
            "requires_input" : False,
            "inputs": None,
            "save_type": "save_file",
            "section": "universities"
        },
        "Cruzeiro Técnico": {
            "button_texts": ["Selecione MSP de Ofertas","Selecione EXP de Campus"],
            "generate_action": lambda data: CruzeiroController().process_tec(data),
            "generate_type": "normal",
            "requires_input" : False,
            "inputs": None,
            "save_type": "save_file",
            "section": "cruzeiro"
        },
        "Cruzeiro Pós Graduação": {
            "button_texts": ["Selecione MSP de Ofertas","Selecione EXP de Campus","Selecione Relação"],
            "generate_action": lambda data: CruzeiroController().process_tec(data),
            "generate_type": "normal",
            "requires_input" : True,
            "inputs": ["Semestre de Ingresso","Data End", "OSC"],
            "user_inputs": [],
            "save_type": "save_file",
            "section": "cruzeiro"
        },
        "Cruzeiro Graduação EaD": {
            "button_texts": ["Selecione Ofertas","Selecione Rel. Cursos","Selecione EXP de Campus"],
            "generate_action": lambda data: CruzeiroController().process_tec(data),
            "generate_type": "normal",
            "requires_input" : True,
            "inputs": ["Data End","OSC", "Semestre de Ingresso"],
            "save_type": "save_file",
            "section": "cruzeiro"
        },
        "Dividir Tabela": {
            "button_texts": ["Selecione Planilha"],
            "generate_action": lambda data: UtilitiesController().create_division(data),
            "generate_type": "normal",
            "requires_input" : False,
            "inputs": None,
            "save_type": "save_file",
            "section": "utilities"
        },
        "Exp para MSP": {
            "button_texts": ["Selecione Exp De Ofertas"],
            "generate_action": lambda data: UtilitiesController().process_exp_msp(data),
            "generate_type": "normal",
            "requires_input" : False,
            "inputs": None,
            "save_type": "directory",
            "section": "utilities"
        },
        "Csv para Excel": {
            "button_texts": ["Selecione Planilha CSV"],
            "generate_action": lambda data: UtilitiesController().process_csv_converter(data),
            "generate_type": "normal",
            "requires_input" : False,
            "inputs": None,
            "save_type": "directory",
            "section": "utilities"
        }
    },
    "Comercial": {
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
        },
        "Dividir Tabela": {
            "button_texts": ["Selecione Planilha"],
            "generate_action": lambda data: UtilitiesController().create_division(data),
            "generate_type": "normal",
            "requires_input" : False,
            "inputs": None,
            "save_type": "save_file",
            "section": "utilities"
        },
        "Exp para MSP": {
            "button_texts": ["Selecione Exp De Ofertas"],
            "generate_action": lambda data: UtilitiesController().process_exp_msp(data),
            "generate_type": "normal",
            "requires_input" : False,
            "inputs": None,
            "save_type": "directory",
            "section": "utilities"
        },
        "Csv para Excel": {
            "button_texts": ["Selecione Planilha CSV"],
            "generate_action": lambda data: UtilitiesController().process_csv_converter(data),
            "generate_type": "normal",
            "requires_input" : False,
            "inputs": None,
            "save_type": "directory",
            "section": "utilities"
        }
    }
}

