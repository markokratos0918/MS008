# Single Payment Process using Singleton and Factory Design Patterns

from abc import ABC, abstractmethod
from enum import Enum
import time
from datetime import datetime

# ========== FACTORY PATTERN ==========

# Payment method types
class PaymentType(Enum):
    CREDIT_CARD = "credit_card"
    PAYPAL = "paypal"
    BANK_TRANSFER = "bank_transfer"

# Abstract Payment Method
class PaymentMethod(ABC):
    def __init__(self, amount: float):
        self.amount = amount
    
    @abstractmethod
    def process_payment(self) -> dict:
        pass

# Concrete Payment Methods
class CreditCardPayment(PaymentMethod):
    def __init__(self, amount: float, card_number: str):
        super().__init__(amount)
        self.card_number = card_number[-4:]  # Store only last 4 digits
    
    def process_payment(self) -> dict:
        print("💳 Processing Credit Card payment...")
        time.sleep(1)  # Simulate processing
        return {
            "method": "Credit Card",
            "amount": self.amount,
            "card_ending": self.card_number,
            "status": "Success",
            "transaction_id": f"CC_{int(time.time())}"
        }

class PayPalPayment(PaymentMethod):
    def __init__(self, amount: float, email: str):
        super().__init__(amount)
        self.email = email
    
    def process_payment(self) -> dict:
        print("🅿️ Processing PayPal payment...")
        time.sleep(1)
        return {
            "method": "PayPal",
            "amount": self.amount,
            "email": self.email,
            "status": "Success",
            "transaction_id": f"PP_{int(time.time())}"
        }

class BankTransferPayment(PaymentMethod):
    def __init__(self, amount: float, account_number: str):
        super().__init__(amount)
        self.account_number = account_number[-4:]
    
    def process_payment(self) -> dict:
        print("🏦 Processing Bank Transfer...")
        time.sleep(2)  # Bank transfers take longer
        return {
            "method": "Bank Transfer",
            "amount": self.amount,
            "account_ending": self.account_number,
            "status": "Success",
            "transaction_id": f"BT_{int(time.time())}"
        }

# Factory Class
class PaymentFactory:
    """Factory to create payment method objects"""
    
    @staticmethod
    def create_payment(payment_type: PaymentType, amount: float, **kwargs) -> PaymentMethod:
        """Creates appropriate payment method based on type"""
        
        if payment_type == PaymentType.CREDIT_CARD:
            return CreditCardPayment(amount, kwargs['card_number'])
        
        elif payment_type == PaymentType.PAYPAL:
            return PayPalPayment(amount, kwargs['email'])
        
        elif payment_type == PaymentType.BANK_TRANSFER:
            return BankTransferPayment(amount, kwargs['account_number'])
        
        else:
            raise ValueError(f"Unsupported payment type: {payment_type}")

# ========== SINGLETON PATTERN ==========

class PaymentProcessor:
    """Singleton Payment Processor - handles all payment operations"""
    
    _instance = None
    
    def __new__(cls):
        """Ensure only one instance exists"""
        if cls._instance is None:
            cls._instance = super(PaymentProcessor, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize only once"""
        if not self._initialized:
            self.factory = PaymentFactory()
            self.last_transaction = None
            self._initialized = True
            print("🏭 Payment Processor initialized (Singleton)")
    
    def process_single_payment(self, payment_type: PaymentType, amount: float, **payment_details) -> dict:
        """Process a single payment using factory pattern"""
        
        print(f"\n💰 Processing ${amount:.2f} payment...")
        print("=" * 40)
        
        try:
            # Use factory to create appropriate payment method
            payment_method = self.factory.create_payment(payment_type, amount, **payment_details)
            
            # Process the payment
            result = payment_method.process_payment()
            
            # Add timestamp and store as last transaction
            result["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.last_transaction = result
            
            return result
            
        except Exception as e:
            error_result = {
                "status": "Failed",
                "error": str(e),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.last_transaction = error_result
            return error_result
    
    def get_last_transaction(self) -> dict:
        """Get the last processed transaction"""
        return self.last_transaction

# ========== DEMONSTRATION ==========

def demonstrate_single_payment():
    """Demonstrate single payment processing with both patterns"""
    
    print("=" * 50)
    print("💳 SINGLE PAYMENT PROCESS DEMO")
    print("Factory Pattern + Singleton Pattern")
    print("=" * 50)
    
    # Test Singleton Pattern - get multiple instances
    processor1 = PaymentProcessor()
    processor2 = PaymentProcessor()
    
    print(f"\n🔍 Singleton Test:")
    print(f"Processor1 ID: {id(processor1)}")
    print(f"Processor2 ID: {id(processor2)}")
    print(f"Same instance? {processor1 is processor2}")
    
    print(f"\n🏭 Factory Pattern Test:")
    
    # Example 1: Credit Card Payment
    print("\n1️⃣ Credit Card Payment:")
    result1 = processor1.process_single_payment(
        PaymentType.CREDIT_CARD,
        amount=150.00,
        card_number="1234567890123456"
    )
    display_result(result1)
    
    # Example 2: PayPal Payment (using processor2 to show singleton)
    print("\n2️⃣ PayPal Payment:")
    result2 = processor2.process_single_payment(
        PaymentType.PAYPAL,
        amount=75.50,
        email="user@example.com"
    )
    display_result(result2)
    
    # Example 3: Bank Transfer
    print("\n3️⃣ Bank Transfer:")
    result3 = processor1.process_single_payment(
        PaymentType.BANK_TRANSFER,
        amount=500.00,
        account_number="987654321"
    )
    display_result(result3)
    
    # Show that both processors have the same last transaction (singleton effect)
    print(f"\n🔄 Singleton Effect:")
    print(f"Last transaction from processor1: {processor1.get_last_transaction()['transaction_id']}")
    print(f"Last transaction from processor2: {processor2.get_last_transaction()['transaction_id']}")
    print(f"Same transaction? {processor1.get_last_transaction() == processor2.get_last_transaction()}")

def display_result(result: dict):
    """Display payment result in a formatted way"""
    
    if result["status"] == "Success":
        print("✅ PAYMENT SUCCESSFUL!")
        print(f"   💳 Method: {result['method']}")
        print(f"   💰 Amount: ${result['amount']:.2f}")
        print(f"   🆔 Transaction ID: {result['transaction_id']}")
        print(f"   🕒 Time: {result['timestamp']}")
        
        # Display method-specific details
        if 'card_ending' in result:
            print(f"   💳 Card ending: ****{result['card_ending']}")
        elif 'email' in result:
            print(f"   📧 PayPal: {result['email']}")
        elif 'account_ending' in result:
            print(f"   🏦 Account ending: ****{result['account_ending']}")
    else:
        print("❌ PAYMENT FAILED!")
        print(f"   🚫 Error: {result['error']}")
        print(f"   🕒 Time: {result['timestamp']}")

# ========== SIMPLE USAGE EXAMPLE ==========

def simple_usage():
    """Simple example showing how to use the system"""
    
    print("\n" + "=" * 50)
    print("🚀 SIMPLE USAGE EXAMPLE")
    print("=" * 50)
    
    # Step 1: Get the payment processor (Singleton)
    processor = PaymentProcessor()
    
    # Step 2: Process a payment using Factory
    result = processor.process_single_payment(
        PaymentType.CREDIT_CARD,
        amount=99.99,
        card_number="4567890123456789"
    )
    
    # Step 3: Display result
    print("\n📋 Payment Result:")
    display_result(result)

# ========== KEY BENEFITS DEMO ==========

def show_pattern_benefits():
    """Demonstrate the benefits of using both patterns"""
    
    print("\n" + "=" * 50)
    print("🎯 PATTERN BENEFITS DEMONSTRATION")
    print("=" * 50)
    
    print("\n🏭 Factory Pattern Benefits:")
    print("   ✅ Easy to add new payment methods")
    print("   ✅ Centralized object creation")
    print("   ✅ Client doesn't need to know specific classes")
    
    # Show factory creating different objects
    factory = PaymentFactory()
    
    cc_payment = factory.create_payment(PaymentType.CREDIT_CARD, 100, card_number="1234567890123456")
    pp_payment = factory.create_payment(PaymentType.PAYPAL, 100, email="test@example.com")
    bt_payment = factory.create_payment(PaymentType.BANK_TRANSFER, 100, account_number="987654321")
    
    print(f"   🏭 Factory created: {cc_payment.__class__.__name__}")
    print(f"   🏭 Factory created: {pp_payment.__class__.__name__}")
    print(f"   🏭 Factory created: {bt_payment.__class__.__name__}")
    
    print("\n🔒 Singleton Pattern Benefits:")
    print("   ✅ Single point of control")
    print("   ✅ Shared state across application")
    print("   ✅ Consistent transaction tracking")
    
    # Show singleton behavior
    p1 = PaymentProcessor()
    p2 = PaymentProcessor()
    p3 = PaymentProcessor()
    
    print(f"   🔒 All processors are same instance: {p1 is p2 is p3}")

# Run demonstrations
if __name__ == "__main__":
    demonstrate_single_payment()
    simple_usage()
    show_pattern_benefits()