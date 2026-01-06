from ....models.offer.msp_offer import CheckAnyErrorFromOfferSheet as MspCheck
from ....models.offer.exp_offer import CheckAnyErrorFromOfferSheet as ExpCheck

class OfferController:
    def process_offer_msp(self, process_data):
        paths = list(process_data['paths'].values())

        msp = paths[0]

        offer = MspCheck(msp)
        offer.execute()

    def process_offer_exp(self, process_data):
        paths = list(process_data['paths'].values())

        exp = paths[0]

        offer = ExpCheck(exp)
        offer.execute()