

class PayPalPayment:
    def process_payment(self, amount):
        return f"Processed ${amount} payment with PayPal."

class StripePayment:
    def process_payment(self, amount):
        return f"Processed ${amount} payment with Stripe."

class CreditCardPayment:
    def process_payment(self, amount):
        return f"Processed ${amount} payment with Credit Card."



class PaymentProcessorFactory:
	_processor = {
		"paypal": PayPalPayment,
		"stripe": StripePayment,
		"credit_card": CreditCardPayment
	}

	@classmethod
	def create_processor(cls, payment_method):
		processor_class = cls._processor.get(payment_method.lower())
		if not processor_class:
			raise ValueError(f"Unknown payment method: {payment_method}")
		return processor_class()
		



def checkout(payment_method, amount):
	processor = PaymentProcessorFactory.create_processor(payment_method)
	return processor.process_payment(amount)	
#This function simulates a checkout process.
# It uses the factory to get the correct payment processor and processes the payment.																											

print("Checkout with PayPal:", checkout("paypal", 100))
print("Checkout with Stripe:", checkout("stripe", 150))
print("Checkout with Credit Card:", checkout("credit_card", 200))       


# These are three separate classes, each representing a different payment method.
# Each class has a process_payment method that takes an amount and returns a string describing the processed payment.
# PaymentProcessorFactory is a factory class that creates payment processor objects.
# _processor is a dictionary mapping payment method names to their respective classes.
# create_processor is a class method that:
# Looks up the class for the given payment_method.
# Raises an error if the method is unknown.
# Returns an instance of the appropriate payment processor class