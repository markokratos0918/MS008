
class PayPalPayment:
	def process_payment(self, amount):
		return f"Processing ${amount} via PayPal"


class StripePayment:
	def process_payment(self, amount):
		return f"Processing ${amount} via Stripe"


class CreditCardPayment:
	def process_payment(self, amount):
		return f"Processing ${amount} via Credit Card"


# Factory class
class PaymentFactory:    
	@staticmethod
	def get_payment_processor(payment_method):
		if payment_method == "paypal":
			return PayPalPayment()
		elif payment_method == "stripe":
			return StripePayment()
		elif payment_method == "credit_card":
			return CreditCardPayment()
		else:
			raise ValueError("Unknown payment method")

# Client code using the factory
def checkout(payment_method, amount):
	processor = PaymentFactory.get_payment_processor(payment_method)
	return processor.process_payment(amount)

print("Checkout with PayPal:", checkout("paypal", 100))
print("Checkout with Stripe:", checkout("stripe", 150))
print("Checkout with Credit Card:", checkout("credit_card", 200))       


#class PaymentFactory - Defines a class called PaymentFactory
#  that will be responsible for creating payment processor objects.

#@staticmethod - Declares the following method as a static method, so it can be called
#  on the class itself without creating an instance.

#def get_payment_processor(payment_method) - Defines a method that takes payment_method as a
# an argument and returns the appropriate payment processor object.

#if payment_method == "paypal":            return PayPalPayment()
  #If the payment method is "paypal", it creates and returns an instance of PayPalPayment.

#elif payment_method == "stripe":          return StripePayment()
  #If the payment method is "stripe", it creates and returns an instance of StripePayment.

#elif payment_method == "credit_card":     return CreditCardPayment()
    #If the payment method is "credit_card", it creates and returns an instance of CreditCardPayment.
#else:                                    raise ValueError("Unknown payment method")
    #If the payment method is none of the above, it raises a ValueError indicating an
    # unknown payment method.   
	
#def checkout(payment_method, amount) - Defines a function that simulates a checkout process.
# It takes the payment method and amount as arguments.
#processor = PaymentFactory.get_payment_processor(payment_method)
# It uses the PaymentFactory to get the appropriate payment processor based on the
# provided payment method.
#return processor.process_payment(amount)
# It calls the process_payment method on the obtained processor to process the payment  and returns the result.
