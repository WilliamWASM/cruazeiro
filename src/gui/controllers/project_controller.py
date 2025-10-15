from ..factories.project_factory import *
class ProjectController():
    def __init__(self,project_name,project_config):

        self.project_config = project_config 
        self.project_name = project_name
        self.project_contents,self.card_controllers = ProjectFactory.build(self.project_name,self.project_config)

    def get_card_areas(self):
        return {menu_item: card_area["card_area"] for menu_item,card_area in self.project_contents.items()}
    
    def get_cards(self,section_name):
        return self.project_contents[section_name]["cards"]