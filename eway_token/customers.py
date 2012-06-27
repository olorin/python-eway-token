from payments import EwayPayment

class EwayCustomer(object):
    member_names = {
        'Title' : 'title',
        'FirstName' : 'first_name',
        'LastName' : 'last_name', 
        'Address' : 'address', 
        'Suburb' : 'suburb', 
        'State' : 'state',
        'Company' : 'company',
        'PostCode' : 'post_code',
        'Country' : 'country',
        'Email' : 'email',
        'Fax' : 'fax',
        'Phone' : 'phone',
        'Mobile' : 'mobile',
        'CustomerRef' : 'customer_ref',
        'JobDesc' : 'job_description',
        'Comments' : 'comments',
        'URL' : 'url',
        'CCNumber' : 'cc_number', 
        'CCNameOnCard' : 'cc_name_on_card',
        'CCExpiryMonth' : 'cc_expiry_month',
        'CCExpiryYear' : 'cc_expiry_year',
        }
    field_names = dict(map(lambda p: (p[1],p[0]), member_names.items()))
    query_member_names = {
        'CustomerTitle' : 'title',
        'CustomerFirstName' : 'first_name',
        'CustomerLastName' : 'last_name', 
        'CustomerAddress' : 'address', 
        'CustomerSuburb' : 'suburb', 
        'CustomerState' : 'state',
        'CustomerCompany' : 'company',
        'CustomerPostCode' : 'post_code',
        'CustomerCountry' : 'country',
        'CustomerEmail' : 'email',
        'CustomerFax' : 'fax',
        'CustomerPhone1' : 'phone',
        'CustomerPhone2' : 'mobile',
        'CustomerRef' : 'customer_ref',
        'CustomerJobDesc' : 'job_description',
        'CustomerComments' : 'comments',
        'CustomerURL' : 'url',
        'CCNumber' : 'cc_number', 
        'CCName' : 'cc_name_on_card',
        'CCExpiryMonth' : 'cc_expiry_month',
        'CCExpiryYear' : 'cc_expiry_year',
        }

    @classmethod
    def get(cls, client, customer_id):
        '''Retrieves an existing customer from Eway by its customer_id
        and instantiates and returns an EwayCustomer.'''
        instance = cls()
        instance.client = client
        instance.customer_id = customer_id
        instance._load()
        return instance

    @classmethod
    def create(cls, 
               client, 
               title,
               first_name, 
               last_name, 
               country, 
               cc_number, 
               cc_expiry_month, 
               cc_expiry_year, 
               cc_name_on_card, 
               address=None, 
               suburb=None, 
               state=None, 
               company=None, 
               post_code=None, 
               email=None, 
               fax=None, 
               phone=None, 
               mobile=None, 
               customer_ref=None, 
               job_description=None, 
               comments=None, 
               url=None):
        '''Creates a new customer from data supplied, registers it 
        with Eway and returns an EwayCustomer instance.

        country is a two-letter lowercase country code (e.g. 'au');
        title is one of the following: 
        
        'Mr.','Ms.','Mrs.','Miss','Dr.','Sir.','Prof.' '''
        args = locals()
        instance = cls()
        for k in args:
            setattr(instance, k, args[k] or '')
        instance._save_initial()
        return instance

    def save_changes(self):
        '''Syncs local changes in customer data to Eway.'''
        params = self._build_param_dict()
        self.client.customers.update(self.customer_id, params)

    def process_payment(self, amount, invoice_ref, invoice_description, cvn=None):
        '''Processes a payment from the customer of amount IN DOLLARS 
        (either an integral number of dollars or a Decimal object).
        cvn is optional (but strongly recommended).'''
        cents = int(amount*100)
        res = self.client.payments.process(self.customer_id, 
                                           cents,
                                           invoice_ref,
                                           invoice_description,
                                           cvn)
        payment = EwayPayment(dict(res))
        return payment

    def get_payments(self):
        '''Returns the customer's transaction history (as a list of 
        EwayPayment objects).'''
        records = dict(self.client.payments.query(self.customer_id))
        payments = map(lambda p: EwayPayment(dict(p), from_record=True), records['ManagedTransaction'])
        return payments

    def _load(self):
        '''Updates the current instance with data from Eway (by
        customer_id).'''
        customer = self.client.customers.query(self.customer_id)
        if not customer:
            raise InvalidCustomerID
        vals = dict(customer)
        del vals['ManagedCustomerID']
        for k in vals:
            setattr(self, self.query_member_names[k], vals[k])

    def _save_initial(self):
        params = self._build_param_dict()
        self.customer_id = self.client.customers.create(params) 

    def _build_param_dict(self):
        return dict(zip(self.member_names.keys(), map(lambda k: self.__dict__[k], self.member_names.values())))
        
    
        
