python-eway-token
=================

A simple Python implementation of Eway's token-based/managed payment system.

Installation
============

    sudo python2 setup.py install

Example usage
=============

    from eway_token import EwayTokenClient, EwayCustomer

    client = EwayTokenClient(eway_customer_id=87654321, 
        username='username', 
        password='password', 
        live=True)

    customer = EwayCustomer.create(client, 
        first_name='Foo', 
        last_name='Bar', 
        country='au', 
        cc_number='4444333322221111', 
        cc_expiry_month=11, 
        cc_expiry_year=14, 
        cc_name_on_card='Foo Baz Bar')

    # after creation the Eway customer ID is stored in 
    # customer.customer_id

    customer.title = 'Prof.'
    customer.save_changes()
    payment = customer.process_payment(Decimal('3.14'), 'ref00', 'invoice description', cvn=271)

    another_customer = EwayCustomer.get(client, customer_id=654321)
    past_payments = another_customer.get_payments()

