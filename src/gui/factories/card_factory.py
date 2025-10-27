from ..views.cards.base_card import *
from ..views.cards.combo_box_card import *
from ..views.cards.extra_button_card import *
from ..controllers.card_controller import *
from ...config.configurations import CARD_TYPES, CARD_ACTIONS

class CardFactory:
    CARD_TYPES = {
        "base": BaseCard,
        "combo": ComboBoxCard,
        "extra": ExtraButtonCard,
    }
    card_actions = CARD_ACTIONS 


    @staticmethod
    def build(card_config: dict):
        card_type = card_config["type"]
        card_class = CardFactory.CARD_TYPES.get(card_type, BaseCard)

        if card_type == "combo":
            card = card_class(card_config["title"], card_config.get("items", []), card_config.get("description", ""))
        else:
            card = card_class(card_config["title"], card_config.get("description", ""))

        card_controller = CardController(card)
        return card, card_controller