from datetime import date,datetime
from api.payment_gateway import PaymentGateway


class PaymentProcessor:
    """
    This class is used for payment processing.
    We can validate input data and call payment gateway based on amount
    1. Use Cheapest gateway for amount less than 20
    2. Use Expensive gateway for 20 <= amount <= 500
    3. Use Premium gateway for amount > 500
    """
    def __init__(self, card_number, card_holder, expiry_date, amount, security_code=None):
        self.card_number = card_number
        self.card_holder = card_holder
        self.expiry_date = expiry_date
        self.security_code = security_code
        self.amount = amount

    def validate_input(self):
        if not luhn(self.card_number) or not isinstance(self.card_number, str):
            return False, "Invalid Credit Card Number"
        if not isinstance(self.card_holder, str):
            return False, "Invalid Card Holder"
        if datetime.strptime(self.expiry_date, '%d/%m/%Y').date() < date.today():
            return False, "Card has already expired"
        if not isinstance(self.amount, float) or self.amount < 0:
            return False, "Invalid Amount entered, It must be positive decimal value"
        if self.security_code:
            if not isinstance(self.security_code, str) or len(self.security_code) != 3:
                return False, "Invalid Security Code, It must be 3 digit long character"
        return True, "All inputs are valid"

    def process_payment(self):
        gateway_obj = PaymentGateway(self.card_number, self.card_holder, self.expiry_date,
                                     self.amount, self.security_code)
        if self.amount < 20:
            validation_status, message = gateway_obj.cheap()
            payment_status = validation_status
        elif 20 <= self.amount <= 500:
            validation_status, message = gateway_obj.expensive()
            if not validation_status:
                validation_status, message = gateway_obj.cheap()
            payment_status = validation_status
        else:
            validation_status, message = gateway_obj.premium()
            if not validation_status:
                for _ in range(3):
                    validation_status, message = gateway_obj.premium()
            payment_status = validation_status

        return payment_status, message


def luhn(card_number):
    """
    function to validate Credit Card Number based on Luhn Algorithm
    :param card_number:
    :return: True/False
    """
    digits = [int(c) for c in card_number if c.isdigit()]
    checksum = digits.pop()
    digits.reverse()
    doubled = [2*d for d in digits[0::2]]
    total = sum(d-9 if d > 9 else d for d in doubled) + sum(digits[1::2])
    return (total * 9) % 10 == checksum
