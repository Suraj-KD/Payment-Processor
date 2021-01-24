class PaymentGateway:
    """
    Class for handling different type of gateway endpoint.
    Each method can used as separate gateway
    """

    def __init__(self, card_number, holder, expiry_date, amount, security_code=None):
        self.card_number = card_number
        self.holder = holder
        self.expiry_date = expiry_date
        self.security_code = security_code
        self.amount = amount

    @staticmethod
    def cheap():
        return True, "Success"

    @staticmethod
    def expensive():
        return True, "Success"

    @staticmethod
    def premium():
        return True, "Success"
