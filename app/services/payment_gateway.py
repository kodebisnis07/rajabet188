class ManualPaymentGateway:
    def create_invoice(self, amount, method='Manual'):
        return {'status': 'pending', 'amount': amount, 'method': method, 'message': 'Invoice manual dibuat'}

    def verify_callback(self, payload):
        return {'valid': True, 'payload': payload}
