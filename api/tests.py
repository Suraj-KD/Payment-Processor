from django.test import TestCase
import requests
ENDPOINT = 'http://127.0.0.1:8000/api/process_payment'


# Create your tests here.
class APITest(TestCase):

    def test_get_method_call(self):
        data = {}
        resposne = requests.get(ENDPOINT, data=data)
        return self.assertEqual(resposne.status_code, 405)

    def test_put_method_call(self):
        data = {}
        resposne = requests.put(ENDPOINT, data=data)
        return self.assertEqual(resposne.status_code, 405)

    def test_delete_method_call(self):
        data = {}
        resposne = requests.delete(ENDPOINT, data=data)
        return self.assertEqual(resposne.status_code, 405)

    def test_missing_credit_card_number(self):
        data = {
            "CreditCardNumber": "",
            "CardHolder": "Suraj Kumar Dubey",
            "ExpirationDate": "24/01/2021",
            "Amount": 25.00
        }
        response = requests.post(ENDPOINT, data=data)
        self.assertEqual(response.status_code, 400)

    def test_missing_card_holder(self):
        data = {
            "CreditCardNumber": "4111 1111 1111 1111",
            "CardHolder": "",
            "ExpirationDate": "24/01/2021",
            "Amount": 25.00
        }
        response = requests.post(ENDPOINT, data=data)
        self.assertEqual(response.status_code, 400)

    def test_missing_expiry_date(self):
        data = {
            "CreditCardNumber": "4111 1111 1111 1111",
            "CardHolder": "Suraj Kumar Dubey",
            "ExpirationDate": "",
            "Amount": 25.00
        }
        response = requests.post(ENDPOINT, data=data)
        self.assertEqual(response.status_code, 400)

    def test_missing_amount(self):
        data = {
            "CreditCardNumber": "4111 1111 1111 1111",
            "CardHolder": "Suraj Kumar Dubey",
            "ExpirationDate": "24/01/2021",
            "Amount": ""
        }
        response = requests.post(ENDPOINT, data=data)
        self.assertEqual(response.status_code, 400)

    def test_invalid_expiry_date(self):
        data = {
            "CreditCardNumber": "4111 1111 1111 1111",
            "CardHolder": "Suraj Kumar Dubey",
            "ExpirationDate": "20/01/2021",
            "Amount": 25.00
        }
        response = requests.post(ENDPOINT, data=data)
        self.assertEqual(response.status_code, 400)

    def test_invalid_credit_card_number(self):
        data = {
            "CreditCardNumber": "4111 1111 1111 111",
            "CardHolder": "Suraj Kumar Dubey",
            "ExpirationDate": "20/01/2021",
            "Amount": 25.00
        }
        response = requests.post(ENDPOINT, data=data)
        self.assertEqual(response.status_code, 400)

    def test_credit_card_number_having_alphabets(self):
        data = {
            "CreditCardNumber": "4111 1111 1111 111a",
            "CardHolder": "Suraj Kumar Dubey",
            "ExpirationDate": "20/01/2021",
            "Amount": 25.00
        }
        response = requests.post(ENDPOINT, data=data)
        self.assertEqual(response.status_code, 400)

    def test_amount_value_as_string(self):
        data = {
            "CreditCardNumber": "4111 1111 1111 1111",
            "CardHolder": "Suraj Kumar Dubey",
            "ExpirationDate": "24/01/2021",
            "Amount": "20"
        }
        response = requests.post(ENDPOINT, data=data)
        self.assertEqual(response.status_code, 400)

    def test_amount_value_as_intger(self):
        data = {
            "CreditCardNumber": "4111 1111 1111 1111",
            "CardHolder": "Suraj Kumar Dubey",
            "ExpirationDate": "24/01/2021",
            "Amount": 20
        }
        response = requests.post(ENDPOINT, data=data)
        self.assertEqual(response.status_code, 400)

    def test_security_code_having_more_data_length(self):
        data = {
            "CreditCardNumber": "4111 1111 1111 1111",
            "CardHolder": "Suraj Kumar Dubey",
            "ExpirationDate": "24/01/2021",
            "Amount": 25.00,
            "SecurityCode": "3333"
        }
        response = requests.post(ENDPOINT, data=data)
        self.assertEqual(response.status_code, 400)

    def test_security_code_having_less_data_length(self):
        data = {
            "CreditCardNumber": "4111 1111 1111 1111",
            "CardHolder": "Suraj Kumar Dubey",
            "ExpirationDate": "24/01/2021",
            "Amount": 25.00,
            "SecurityCode": "33"
        }
        response = requests.post(ENDPOINT, data=data)
        self.assertEqual(response.status_code, 400)

    def test_security_code_with_wrong_data_type(self):
        data = {
            "CreditCardNumber": "4111 1111 1111 1111",
            "CardHolder": "Suraj Kumar Dubey",
            "ExpirationDate": "24/01/2021",
            "Amount": 25.00,
            "SecurityCode": 333
        }
        response = requests.post(ENDPOINT, data=data)
        self.assertEqual(response.status_code, 400)
