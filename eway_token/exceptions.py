class EwayException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)

class RequiredFieldMissing(EwayException):
    pass

class InvalidPaymentAmount(EwayException):
    def __str__(self):
        return "Amount must be an integer. (did you forget to convert it to cents?)"

class InvalidCustomerID(EwayException):
    pass
