from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from api.payment_processor import PaymentProcessor


# Create your views here.
class PaymentView(APIView):

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super(PaymentView, self).dispatch(request, *args, **kwargs)

    def post(self, *args, **kwargs):
        mandatory_check_status, message = self.check_mandatory_fields()
        if not mandatory_check_status:
            return Response(data=message, status=400)
        input_data = self.request.data
        card_number = input_data.get('CreditCardNumber')
        card_holder = input_data.get('CardHolder')
        expiry_date = input_data.get('ExpirationDate')
        security_code = input_data.get('SecurityCode')
        amount = input_data.get('Amount')
        try:
            processor_obj = PaymentProcessor(card_number, card_holder, expiry_date, amount, security_code)
            validation_status, validation_message = processor_obj.validate_input()
            if not validation_status:
                return Response(data=validation_message, status=400)
            process_status, process_message = processor_obj.process_payment()
            if not process_status:
                return Response(data=process_message, status=400)

            return Response(data="Paymeny done.", status=200)
        except Exception as error:
            print(error)
            return Response(data="Internal Server Error", status=500)

    def check_mandatory_fields(self):
        data = self.request.data
        if not data.get('CreditCardNumber'):
            return False, "missing Credit card number"
        if not data.get('CardHolder'):
            return False, "missing Card Holder"
        if not data.get('ExpirationDate'):
            return False, "missing expiration date"
        if not data.get('Amount'):
            return False, "missing amount input"
        return True, "All Mandatory fields are present"
