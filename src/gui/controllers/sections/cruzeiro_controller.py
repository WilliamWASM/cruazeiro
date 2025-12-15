from ....models.Cruzeiro_do_Sul.Graduacao_EaD.ModifyHandler import *
from ....models.Cruzeiro_do_Sul.PosGradEad import *
from ....models.Cruzeiro_do_Sul.tecnico import *

class CruzeiroController:
    def process_tec(self,process_data:dict):
            paths = list(process_data["paths"].values())
            save_path = process_data["save_path"]

            msp = paths[0]
            exp = paths[1]

            tecnico = tecnicoCruzeiro(msp,exp)
            tecnico.load(save_path)
            
    def process_pos(self,process_data:dict):
            paths = list(process_data["paths"].values())
            save_path = process_data["save_path"]

            msp = paths[0]
            exp = paths[1]
            relation = paths[2]

            pos = PosGradEadCruzeiro(msp,exp,relation)
            inputs = process_data["user_inputs"]
            pos.load()
            pos.set_values_missing_in_msp(inputs[0],inputs[1],inputs[2])
            pos.save(save_path)
   
    def process_grad(self,process_data:dict):
            paths = list(process_data["paths"].values())
            save_path = process_data["save_path"]

            offers = paths[0]
            relation = paths[1]
            exp = paths[2]

            grad = ModifyHandler(offers,relation,exp)
            inputs = process_data["user_inputs"]
            grad.set_values(inputs[0],inputs[1],inputs[2])
            grad.load(save_path)