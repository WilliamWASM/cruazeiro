from ..views.card_area import *
from .card_factory import *
from ...config.configurations import CARD_ACTIONS
class ProjectFactory:
    @staticmethod
    def build(project_name,project_config):
        project_contents = {}
        card_controllers = []
        action_map = CARD_ACTIONS.get(project_name,{})

        for section_name,cards_config in project_config.items():
            card_area = CardArea()
            section_cards = []

            for card in cards_config:
                action_config = action_map.get(section_name,{})
                card, card_controller = CardFactory.build(card,action_config)
                
                if section_name == "Campus" and project_name == "SiteOps":
                    card_controller.set_default_values(action_config["button_texts"])
                card_area.add_card(card)
                card.setFixedSize(250,320)
                section_cards.append(card)
                card_controllers.append(card_controller)                

            project_contents[section_name] = {
                "card_area": card_area,
                "cards": section_cards
            }
        
        return project_contents,card_controllers