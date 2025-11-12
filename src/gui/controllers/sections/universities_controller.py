from ....models.unifatecie import *
from ....models.Utilities.lote_kroton import *
class UniversitiesController:
    def process_unifatecie(self,process_data:dict):
        paths = list(process_data["paths"].values())
        save_path = process_data["save_path"]

        offers = paths[0]

        unifatecie = Unifatecie(offers)
        inputs = process_data["user_inputs"]
        unifatecie.set_values(inputs[0],inputs[1])
        unifatecie.load(save_path)

    def process_kroton_lote(self,process_data:dict):
        paths = list(process_data["paths"].values())
        save_path = process_data["save_path"]

        offers = paths[0]
        kroton = KrotonLote(offers, save_path)
        kroton.load()
