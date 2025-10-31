from ....models.campus.CampusVerifications import CampusVerifications
from ....models.campus.UniasselviCampus import UniasselviCampus

class CampusController:
    def process_campus(self, process_data:dict):
        paths = list(process_data["paths"].values())
        save_path = process_data["save_path"]
        
        msp = paths[0]
        exp = paths[1]
        
        campus = CampusVerifications(exp, msp)
        campus.load(save_path)

    def process_uniasselvi_ead(self, process_data):
        paths = list(process_data["paths"].values())
        save_path = process_data["save_path"]
        
        msp = paths[0]
        exp = paths[1]
        
        campus = UniasselviCampus(exp, msp, 'EAD')
        campus.load(save_path)

    def process_uniasselvi_presencial(self, process_data):
        paths = list(process_data["paths"].values())
        save_path = process_data["save_path"]
        
        msp = paths[0]
        exp = paths[1]
        
        campus = UniasselviCampus(exp, msp, 'PRESENCIAL')
        campus.load(save_path)
