from ..gui.views.cards.base_card import *
from ..gui.views.cards.combo_box_card import *
from ..gui.views.cards.extra_button_card import *
from ..resources.styles.light import *
from ..resources.styles.dark import *
from ..gui.controllers.sections.campus_controller import *
from ..gui.controllers.sections.cruzeiro_controller import *
from ..gui.controllers.sections.universities_controller import *
from ..gui.controllers.sections.utilities_controller import *
from ..gui.managers.file_manager import *
from ..gui.views.cards.triple_button_card import *
PROJECT_CONFIGS = {
            "SiteOps":{
                "Universities":[
                    {
                        "type": "base",
                        "title":"Unifatecie",
                        "description":"- Selecione a planilha de ofertas da IES.\n- Clique em Gerar."
                        "\n- Preencha Data End e OSC(s).\n- Nomeie o arquivo que será gerado."
                    },
                    {
                        "type": "base",
                        "title":"Kroton Lote",
                        "description":"- Selecione a planilha de ofertas da IES."
                        "\n- Clique em Gerar.\n- Selecione o diretório onde deseja salvar."
                    }
                ],
                "Campus":[
                    {
                        "type": "extra",
                        "title":"Campus",
                        "description":"- Selecione a MSP de Campus.\n- Selecione o Exp de Campus."
                        "\n- Clique em Gerar.\nn- Selecione o diretório e nome para o arquivo queserá gerado."
                    },
                    {
                        "type": "extra",
                     "title":"Uniasselvi EaD",
                     "description":"- Selecione a Planilha da IES.\n- Selecione o Exp de Campus."
                     "\n- Clique em Gerar.\n- Selecione o diretório e nome para o arquivo queserá gerado."
                    },
                    {
                        "type": "extra",
                        "title":"Uniasselvi Presencial",
                        "description":"- Selecione a Planilha da IES.\n- Selecione o Exp de Campus."
                        "\n- Clique em Gerar.\n- Selecione o diretório e nome para o arquivo queserá gerado."
                    }
                ],
                "Cruzeiro":[
                    {
                        "type": "extra",
                        "title":"Cruzeiro Técnico",
                        "description":"- Selecione a MSP de Ofertas.\n- Selecione o Exp de Campus."
                        "\n- Clique em Gerar.\n- Selecione o diretório e nome para arquivo gerado."
                    },
                    {
                        "type": "triple",
                        "title":"Cruzeiro Pós Graduação",
                        "description":"- Selecione a MSP de Ofertas.\n- Selecione o Exp de Campus."
                        "\n- Selecione a Relação com os polos que devem ser separados.\n- Clique em Gerar.\n- Preencha os valores solicitados."
                        "\n- Selecione o diretório e nome para arquivo gerado."
                    },
                    {
                        "type": "triple",
                        "title":"Cruzeiro Graduação EaD",
                        "description":"- Selecione a Planilha de Ofertas.\n- Selecione a Relação de Cursos."
                        "\n- Selecione o Exp de Campus.\n- Clique em Gerar.\n- Preencha os valores solicitados.\n- Selecione o diretório e nome para arquivo gerado."
                    },
                ],
                "Utilities": [
                    {
                        "type": "combo",
                        "title":"Dividir tabela",
                        "description":"- Selecione a quantidade de divisões que deseja.\n- Selecione a planilha."
                        "\n- Clique em Gerar.\n- Escolha o diretório onde deseja salvar o arquivo."
                        "\n\nIMPORTANTE: O arquivo será gerado no diretório selecionado, com nome pré-configurado.",
                        "items": ["2","3","4","5","6","7","8","9","10"]
                     },
                    {
                            "type": "base",
                        "title":"Exp para Msp",
                        "description":"- Selecione a planilha modelo Exp.\n- Clique em Gerar.\n- Selecione o diretório onde deseja salvar o arquivo."
                        "\n\nIMPORTANTE: O arquivo será gerado no diretório selecionado, com nome pré-configurado."
                    },
                    {
                        "type": "base",
                        "title":"Csv para Excel",
                        "description":"- Selecione a planilha CSV.\n- Clique em Gerar.\n- Selecione o diretório onde deseja salvar o arquivo."
                        "\n\nIMPORTANTE: O arquivo será gerado no diretório selecionado, com nome pré-configurado."
                    },
                ]
            },
            "Comercial":{
                "Campus":[
                    {
                        "type": "base",
                        "title":"Campus",
                        "description":"- Selecione a MSP de Campus.\n- Selecione o Exp de Campus."
                        "\n- Clique em Gerar.\nn- Selecione o diretório e nome para o arquivo queserá gerado."
                    },
                    {
                        "type": "base",
                        "title":"Uniasselvi EaD",
                        "description":"- Selecione a Planilha da IES.\n- Selecione o Exp de Campus."
                     "\n- Clique em Gerar.\n- Selecione o diretório e nome para o arquivo queserá gerado."
                    },
                    {
                        "type": "base",
                        "title":"Uniasselvi Presencial",
                        "description":"- Selecione a Planilha da IES.\n- Selecione o Exp de Campus."
                        "\n- Clique em Gerar.\n- Selecione o diretório e nome para o arquivo queserá gerado."
                    }
                ],
                "Utilities": [
                    {
                        "type": "combo",
                        "title":"Dividir tabela",
                        "description":"- Selecione a quantidade de divisões que deseja.\n- Selecione a planilha."
                        "\n- Clique em Gerar.\n- Escolha o diretório onde deseja salvar o arquivo."
                        "\n\nIMPORTANTE: O arquivo será gerado no diretório selecionado, com nome pré-configurado.",
                        "items": ["2","3","4","5","6","7","8","9","10"]
                    },
                    {
                        "type": "base",
                        "title":"Exp para Msp",
                        "description":"- Selecione a planilha modelo Exp.\n- Clique em Gerar.\n- Selecione o diretório onde deseja salvar o arquivo."
                        "\n\nIMPORTANTE: O arquivo será gerado no diretório selecionado, com nome pré-configurado."
                    },
                    {
                        "type": "base",
                        "title":"Csv para Excel",
                        "description":"- Selecione a planilha CSV.\n- Clique em Gerar.\n- Selecione o diretório onde deseja salvar o arquivo."
                        "\n\nIMPORTANTE: O arquivo será gerado no diretório selecionado, com nome pré-configurado."
                    },
                ]
            }
        }

CARD_TYPES = {
        "base": BaseCard,
        "combo": ComboBoxCard,
        "extra": ExtraButtonCard,
        "triple": TripleButtonCard
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
            "Campus":{
                "button_texts": ["Selecione MSP Polos", "Selecione EXP campus"],
                "generate_action": lambda data: CampusController().process_campus(data),
                "generate_type": "normal",
                "requires_input" : False,
                "inputs": None,
                "save_type": "save_file",
                "section": "Campus"
            },
            "Uniasselvi EaD": {
                "button_texts": ["Selecione Planilha Campus", "Selecione EXP campus"],
                "generate_action": lambda data: CampusController().process_uniasselvi_ead(data),
                "generate_type": "normal",
                "requires_input" : False,
                "inputs": None,
                "save_type": "save_file",
                "section": "Campus"
            },
            "Uniasselvi Presencial": {
                "button_texts": ["Selecione Planilha Campus", "Selecione EXP campus"],
                "generate_action": lambda data: CampusController().process_uniasselvi_presencial(data),
                "generate_type": "normal",
                "requires_input" : False,
                "inputs": None,
                "save_type": "save_file", 
                "section": "Campus"
            }   
        },
        "Universities": {
            "Unifatecie": {
                "button_texts": ["Selecione Ofertas IES"],
                "generate_action": lambda data: UniversitiesController().process_unifatecie(data),
                "generate_type": "normal",
                "requires_input" : True,
                "inputs": ["Data End","OSC"],
                "save_type": "save_file",
                "section": "Universities"
            },
            "Kroton Lote": {
                "button_texts": ["Selecione Ofertas IES"],
                "generate_action": lambda data: UniversitiesController().process_kroton_lote(data),
                "generate_type": "normal",
                "requires_input" : False,
                "inputs": None,
                "save_type": "save_file",
                "section": "Universities"
            }
        },
        "Cruzeiro": {
            "Cruzeiro Técnico": {
                "button_texts": ["Selecione MSP de Ofertas","Selecione EXP de Campus"],
                "generate_action": lambda data: CruzeiroController().process_tec(data),
                "generate_type": "normal",
                "requires_input" : False,
                "inputs": None,
                "save_type": "save_file",
                "section": "Cruzeiro"
            },
            "Cruzeiro Pós Graduação": {
                "button_texts": ["Selecione MSP de Ofertas","Selecione EXP de Campus","Selecione Relação"],
                "generate_action": lambda data: CruzeiroController().process_pos(data),
                "generate_type": "normal",
                "requires_input" : True,
                "inputs": ["Semestre de Ingresso","Data End", "OSC"],
                "user_inputs": [],
                "save_type": "save_file",
                "section": "Cruzeiro"
            },
            "Cruzeiro Graduação EaD": {
                "button_texts": ["Selecione Ofertas","Selecione Rel. Cursos","Selecione EXP de Campus"],
                "generate_action": lambda data: CruzeiroController().process_grad(data),
                "generate_type": "normal",
                "requires_input" : True,
                "inputs": ["Data End","OSC", "Semestre de Ingresso"],
                "save_type": "save_file",
                "section": "Cruzeiro"
            }
        },
        "Utilities": {
            "Dividir tabela": {
                "button_texts": ["Selecione Planilha"],
                "generate_action": lambda data: UtilitiesController().create_division(data),
                "generate_type": "normal",
                "requires_input" : False,
                "inputs": None,
                "save_type": "directory",
                "section": "Utilities"
            },
            "Exp para Msp": {
                "button_texts": ["Selecione Exp De Ofertas"],
                "generate_action": lambda data: UtilitiesController().process_exp_msp(data),
                "generate_type": "normal",
                "requires_input" : False,
                "inputs": None,
                "save_type": "directory",
                "section": "Utilities"
            },
            "Csv para Excel": {
                "button_texts": ["Selecione Planilha CSV"],
                "generate_action": lambda data: UtilitiesController().process_csv_converter(data),
                "generate_type": "normal",
                "requires_input" : False,
                "inputs": None,
                "save_type": "directory",
                "section": "Utilities"
            }
        }  
    },
    "Comercial": {
        "Campus":{
            "Campus": {
                "button_texts": ["Selecione MSP Polos", "Selecione EXP campus"],
                "generate_action": lambda data: CampusController().process_campus(data),
                "generate_type": "normal",
                "requires_input" : False,
                "inputs": None,
                "save_type": "save_file",
                "section": "Campus"
            },
            "Uniasselvi EaD": {
                "button_texts": ["Selecione Planilha Campus", "Selecione EXP campus"],
                "generate_action": lambda data: CampusController().process_uniasselvi_ead(data),
                "generate_type": "normal",
                "requires_input" : False,
                "inputs": None,
                "save_type": "save_file",
                "section": "Campus"
            },
            "Uniasselvi Presencial": {
                "button_texts": ["Selecione Planilha Campus", "Selecione EXP campus"],
                "generate_action": lambda data: CampusController().process_uniasselvi_presencial(data),
                "generate_type": "normal",
                "requires_input" : False,
                "inputs": None,
                "save_type": "save_file", 
                "section": "Campus"
            }
        },
        "Utilities": {
            "Dividir tabela": {
                "button_texts": ["Selecione Planilha"],
                "generate_action": lambda data: UtilitiesController().create_division(data),
                "generate_type": "normal",
                "requires_input" : False,
                "inputs": None,
                "save_type": "save_file",
                "section": "Utilities"
            },
            "Exp para Msp": {
                "button_texts": ["Selecione Exp De Ofertas"],
                "generate_action": lambda data: UtilitiesController().process_exp_msp(data),
                "generate_type": "normal",
                "requires_input" : False,
                "inputs": None,
                "save_type": "directory",
                "section": "Utilities"
            },
            "Csv para Excel": {
                "button_texts": ["Selecione Planilha CSV"],
                "generate_action": lambda data: UtilitiesController().process_csv_converter(data),
                "generate_type": "normal",
                "requires_input" : False,
                "inputs": None,
                "save_type": "directory",
                "section": "Utilities"
            }
        }
        
    }
}

HOME_INFOS = {
    "app_version": "SiteOps Echo © v1.1.0",
    "features": """
        <ul>
            <li>Novo sistema de notificações</li>
            <li>Melhorias na interface gráfica</li>
            <li>Adição de projetos (SiteOps e Comercial)</li>
            <li>Modo light e dark</li>
            <li>Correção de bugs</li>
            <li>Notificação de carregamento do card</li>
        </ul>
    """,
    "help_text": """
        Envie uma mensagem no canal <b>#parcerias-estoque</b> do Slack,<br>
        ou entre em contato com nossos desenvolvedores:<br>
        <b>@davison.queiroz</b><br>
        <b>@bruno.pelossi</b><br>
        <b>@matheus.antonio</b>
    """
}
