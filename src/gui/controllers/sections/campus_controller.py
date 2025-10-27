from ....models.campus.CampusVerifications import CampusVerifications
from ....models.campus.UniasselviCampus import UniasselviCampus

class CampusController:
    def process_campus(self, process_data:dict):
        paths = process_data["paths"]
        save_path = process_data["save_path"]
        
        msp = paths.get("Msp Polos")
        exp = paths.get("EXP campus")
        
        campus = CampusVerifications(exp, msp)
        campus.load(save_path)

    def process_uniasselvi_ead(self, process_data):
        paths = process_data["paths"]
        save_path = process_data["save_path"]
        
        msp = paths.get("Planilha Campus")
        exp = paths.get("EXP campus")
        
        campus = UniasselviCampus(exp, msp, 'EAD')
        campus.load(save_path)

    def process_uniasselvi_presencial(self, process_data):
        paths = process_data["paths"]
        save_path = process_data["save_path"]
        
        msp = paths.get("Planilha Campus")
        exp = paths.get("EXP campus")
        
        campus = UniasselviCampus(exp, msp, 'PRESENCIAL')
        campus.load(save_path)
