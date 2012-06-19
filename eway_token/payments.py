import datetime

class EwayPayment(object):
    member_names = {
        'ewayTrxnError': 'error_code',
        'ewayTrxnStatus' : 'succeeded',
        'ewayTrxnNumber' : 'transaction_number',
        'ewayReturnAmount' : 'amount',
        'ewayAuthCode' : 'auth_code',
        }
    query_member_names = {
        'TotalAmount' : 'amount',
        'Result' : 'result',
        'ResponseText' : 'response_text',
        'ewayTrxnNumber' : 'transaction_number',
        'TransactionDate' : 'timestamp',
        }

    def __init__(self, data, from_record=False):
        # if this object is being created from the result of a 
        # transaction
        if not from_record:
            for k in data:
                setattr(self, self.member_names[k], data[k])
            self.timestamp = datetime.datetime.now()
        # if it's being created from a list of transactions belonging 
        # to a customer
        else:
            for k in data:
                setattr(self, self.query_member_names[k], data[k])


        
        
