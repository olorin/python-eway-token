from suds.client import Client
from suds.sax.element import Element
from config import *
from exceptions import *

class DataManager(object):
    def __init__(self, client):
        self.client = client
        
class CustomerManager(DataManager):
    fields = [
        'Title',
        'FirstName',
        'LastName', 
        'Address',
        'Suburb', 
        'State',
        'Company',
        'PostCode',
        'Country',
        'Email',
        'Fax',
        'Phone',
        'Mobile',
        'CustomerRef',
        'JobDesc',
        'Comments',
        'URL',
        'CCNumber', 
        'CCNameOnCard',
        'CCExpiryMonth',
        'CCExpiryYear',
        ]
    required_fields = [
        'Title',
        'FirstName',
        'LastName',
        'Country',
        'CCNumber',
        'CCExpiryMonth',
        'CCExpiryYear',
        ]

    def create(self, params):
        for f in self.required_fields:
            if f not in params:
                raise RequiredFieldMissing(f)
        for f in self.fields:
            if f not in params:
                params[f] = ''
        return self.client.service.CreateCustomer(**params)

    def update(self, customer_id, params):
        customer = dict(self.query(customer_id))
        params['managedCustomerID'] = customer_id
        params['CCExpiryMonth'] = customer['CCExpiryMonth']
        params['CCExpiryYear'] = customer['CCExpiryYear']
        return self.client.service.UpdateCustomer(**params)

    def query(self, customer_id):
        return self.client.service.QueryCustomer(managedCustomerID=customer_id)

class PaymentManager(DataManager):
    def process(self, customer_id, cents, invoice_ref, invoice_description, cvn=None):
        if int(cents) != cents:
            raise InvalidPaymentAmount(cents)
        if cvn is None:
            return self.client.service.ProcessPayment(managedCustomerID=customer_id, amount=cents, invoiceReference=invoice_ref, invoiceDescription=invoice_description)
        return self.client.service.ProcessPayment(managedCustomerID=customer_id, amount=cents, invoiceReference=invoice_ref, invoiceDescription=invoice_description, cvn=cvn)

    def query(self, customer_id):
        return self.client.service.QueryPayment(managedCustomerID=customer_id)

class EwayTokenClient(object):
    def __init__(self, eway_customer_id=None, username=None, password=None, live=False, url=None):
        if url is None:
            url = (TOKEN_URL_LIVE if live else TOKEN_URL_TEST)
        if not live:
            eway_customer_id = TEST_CUSTOMER_ID
            username = TEST_USERNAME
            password = TEST_PASSWORD
        self.client = Client(url)
        
        eway_header = self.client.factory.create("eWAYHeader")
        eway_header.eWAYCustomerID = eway_customer_id
        eway_header.Username = username
        eway_header.Password = password

        self.client.set_options(soapheaders=eway_header)
        
        self.customers = CustomerManager(self.client)
        self.payments = PaymentManager(self.client)
