CREATE A MODEL

main name = Pizza

type = Italian, Spanic, French, African

attribute = toppings, extra crust, cheese


MOdel Logistics Mapping

UserProfile
    User
    stripe/mpesa_customer_id




Item
    title
    price
    dicount_price
    category
    label
    slug
    description
    image




orderItem
    user
    ordered
    quantity


Orderd/order
    user #Asssociate user with the order
    referal_code
    items
    start_date
    ordered_date
    ordered
    shiping/delivery_address
    billing_adress(not important)
    Payment
    Coupon
    being_delivered
    refund_requested
    received
    refund_granted

    user | referal_code | items | start_date | ordered_ date | ordered | shipping_adress | billing_adress | Payment | 

Address
    user
    street_address
    appartment_address
    country
    zip
    address_type
    default


Payment
    Mpesa/stripe_charge_id
    amount
    timestamp



Coupon
    referal_code
    amount

Refund
    order
    reason
    accepted
    email

#shortcut
Userprofile_receiver
def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)





