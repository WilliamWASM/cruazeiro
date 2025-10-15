from gui.views.cards.base_card import *
from gui.views.cards.combo_box_card import *
from gui.views.cards.extra_button_card import *
from resources.styles.light import *
PROJECT_CONFIGS = {
            "SiteOps":{
                "Universities":[
                    {"type": "base","title":"Unifatecie","description":"Utilizado para gerar planilha da Unifatecie"},
                    {"type": "base","title":"Kroton Lote","description":"Utilizado para gerar planilha da Unifatecie"}
                ],
                "Campus":[
                    {"type": "base","title":"Campus","description":"Utilizado para gerar planilha da Unifatecie"},
                    {"type": "base","title":"Uniasselv EaD","description":"Utilizado para gerar planilha da Unifatecie"},
                    {"type": "base","title":"Uniasselvi Presencial","description":"Utilizado para gerar planilha da Unifatecie"}
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
            "Comercial" : ComercialStyles,
            "SiteOps" : SiteOpsStyles
        }