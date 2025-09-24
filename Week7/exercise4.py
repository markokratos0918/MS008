from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Any
import threading
import time
from datetime import datetime

# Enum for Payment Types
class PaymentType(Enum):
    CREDIT_CARD = "credit_card"
    PAYPAL = "paypal"
    BANK_TRANSFER = "bank_transfer"
    CRYPTO = "crypto"
    GOOGLE_PAY = "google_pay"

# Abstract Payment Method Base Class
class PaymentMethod(ABC):
    def __init__(self, amount: float):
        self.amount = amount
        self.transaction_id = None
        self.status = "pending"
    
    @abstractmethod
    def validate(self) -> bool:
        """Validate payment method specific details"""
        pass
    
    @abstractmethod
    def process_payment(self) -> Dict[str, Any]:
        """Process the payment and return transaction details"""
        pass
    
    @abstractmethod
    def get_payment_type(self) -> str:
        """Return the payment method type"""
        pass

# Concrete Payment Method Implementations
class CreditCardPayment(PaymentMethod):
    def __init__(self, amount: float, card_number: str, cvv: str, expiry_date: str, cardholder_name: str):
        super().__init__(amount)
        self.card_number = card_number[-4:]  # Store only last 4 digits for security
        self.cvv = cvv
        self.expiry_date = expiry_date
        self.cardholder_name = cardholder_name
    
    def validate(self) -> bool:
        # Simple validation logic
        return len(self.cvv) == 3 and len(self.expiry_date) == 5 and len(self.cardholder_name) > 0
    
    def process_payment(self) -> Dict[str, Any]:
        if not self.validate():
            return {"status": "failed", "message": "Invalid credit card details"}
        
        print("🔄 Processing Credit Card payment...")
        time.sleep(2)  # Simulate payment processing
        self.transaction_id = f"CC_{int(time.time())}"
        self.status = "completed"
        
        return {
            "status": "success",
            "transaction_id": self.transaction_id,
            "amount": self.amount,
            "payment_method": "Credit Card",
            "cardholder_name": self.cardholder_name,
            "card_last_four": f"****-****-****-{self.card_number}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def get_payment_type(self) -> str:
        return "Credit Card"

class PayPalPayment(PaymentMethod):
    def __init__(self, amount: float, email: str):
        super().__init__(amount)
        self.email = email
    
    def validate(self) -> bool:
        return "@" in self.email and "." in self.email
    
    def process_payment(self) -> Dict[str, Any]:
        if not self.validate():
            return {"status": "failed", "message": "Invalid PayPal email address"}
        
        print("🔄 Processing PayPal payment...")
        time.sleep(1.5)
        self.transaction_id = f"PP_{int(time.time())}"
        self.status = "completed"
        
        return {
            "status": "success",
            "transaction_id": self.transaction_id,
            "amount": self.amount,
            "payment_method": "PayPal",
            "email": self.email,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def get_payment_type(self) -> str:
        return "PayPal"

class BankTransferPayment(PaymentMethod):
    def __init__(self, amount: float, account_number: str, routing_number: str, bank_name: str):
        super().__init__(amount)
        self.account_number = account_number[-4:]  # Store only last 4 digits
        self.routing_number = routing_number
        self.bank_name = bank_name
    
    def validate(self) -> bool:
        return len(self.routing_number) == 9 and len(self.bank_name) > 0
    
    def process_payment(self) -> Dict[str, Any]:
        if not self.validate():
            return {"status": "failed", "message": "Invalid bank details"}
        
        print("🔄 Processing Bank Transfer payment...")
        time.sleep(3)  # Bank transfers take longer
        self.transaction_id = f"BT_{int(time.time())}"
        self.status = "completed"
        
        return {
            "status": "success",
            "transaction_id": self.transaction_id,
            "amount": self.amount,
            "payment_method": "Bank Transfer",
            "bank_name": self.bank_name,
            "account_last_four": f"****{self.account_number}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def get_payment_type(self) -> str:
        return "Bank Transfer"

class CryptoPayment(PaymentMethod):
    def __init__(self, amount: float, wallet_address: str, crypto_type: str = "Bitcoin"):
        super().__init__(amount)
        self.wallet_address = wallet_address
        self.crypto_type = crypto_type
    
    def validate(self) -> bool:
        return len(self.wallet_address) >= 26  # Basic Bitcoin address length check
    
    def process_payment(self) -> Dict[str, Any]:
        if not self.validate():
            return {"status": "failed", "message": "Invalid wallet address"}
        
        print("🔄 Processing Cryptocurrency payment...")
        time.sleep(2.5)
        self.transaction_id = f"CR_{int(time.time())}"
        self.status = "completed"
        
        return {
            "status": "success",
            "transaction_id": self.transaction_id,
            "amount": self.amount,
            "payment_method": f"Cryptocurrency ({self.crypto_type})",
            "wallet_address": self.wallet_address[:8] + "...",
            "crypto_type": self.crypto_type,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def get_payment_type(self) -> str:
        return f"Cryptocurrency ({self.crypto_type})"

class GooglePayPayment(PaymentMethod):
    def __init__(self, amount: float, google_account: str, phone_number: str):
        super().__init__(amount)
        self.google_account = google_account
        self.phone_number = phone_number
    
    def validate(self) -> bool:
        return "@gmail.com" in self.google_account and len(self.phone_number) >= 10
    
    def process_payment(self) -> Dict[str, Any]:
        if not self.validate():
            return {"status": "failed", "message": "Invalid Google Pay details"}
        
        print("🔄 Processing Google Pay payment...")
        time.sleep(1)
        self.transaction_id = f"GP_{int(time.time())}"
        self.status = "completed"
        
        return {
            "status": "success",
            "transaction_id": self.transaction_id,
            "amount": self.amount,
            "payment_method": "Google Pay",
            "account": self.google_account,
            "phone_number": f"***-***-{self.phone_number[-4:]}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def get_payment_type(self) -> str:
        return "Google Pay"

# Factory Pattern Implementation
class PaymentMethodFactory:
    """Factory class to create payment method objects dynamically"""
    
    @staticmethod
    def create_payment_method(payment_type: PaymentType, amount: float, **kwargs) -> PaymentMethod:
        """Factory method to create appropriate payment method objects"""
        
        if payment_type == PaymentType.CREDIT_CARD:
            return CreditCardPayment(
                amount=amount,
                card_number=kwargs['card_number'],
                cvv=kwargs['cvv'],
                expiry_date=kwargs['expiry_date'],
                cardholder_name=kwargs['cardholder_name']
            )
        
        elif payment_type == PaymentType.PAYPAL:
            return PayPalPayment(
                amount=amount,
                email=kwargs['email']
            )
        
        elif payment_type == PaymentType.BANK_TRANSFER:
            return BankTransferPayment(
                amount=amount,
                account_number=kwargs['account_number'],
                routing_number=kwargs['routing_number'],
                bank_name=kwargs['bank_name']
            )
        
        elif payment_type == PaymentType.CRYPTO:
            return CryptoPayment(
                amount=amount,
                wallet_address=kwargs['wallet_address'],
                crypto_type=kwargs.get('crypto_type', 'Bitcoin')
            )
        
        elif payment_type == PaymentType.GOOGLE_PAY:
            return GooglePayPayment(
                amount=amount,
                google_account=kwargs['google_account'],
                phone_number=kwargs['phone_number']
            )
        
        else:
            raise ValueError(f"Unsupported payment type: {payment_type}")

# Singleton Pattern Implementation
class PaymentGateway:
    """Singleton Payment Gateway - ensures only one instance exists"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """Ensure only one instance is created (thread-safe)"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(PaymentGateway, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the gateway only once"""
        if not self._initialized:
            self.transaction_history = []
            self.supported_methods = list(PaymentType)
            self.factory = PaymentMethodFactory()
            self._initialized = True
    
    def process_payment(self, payment_type: PaymentType, amount: float, **kwargs) -> Dict[str, Any]:
        """Main method to process payments using the factory pattern"""
        try:
            # Use factory to create appropriate payment method
            payment_method = self.factory.create_payment_method(payment_type, amount, **kwargs)
            
            # Process the payment
            result = payment_method.process_payment()
            
            # Store transaction in history
            self.transaction_history.append(result)
            
            return result
            
        except Exception as e:
            error_result = {
                "status": "error",
                "message": f"Payment processing failed: {str(e)}",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.transaction_history.append(error_result)
            return error_result
    
    def get_transaction_history(self) -> list:
        """Return transaction history"""
        return self.transaction_history.copy()

# Interactive User Interface Functions
class PaymentUI:
    def __init__(self):
        self.gateway = PaymentGateway()
    
    def display_welcome(self):
        """Display welcome message"""
        print("=" * 60)
        print("🏦 WELCOME TO SECURE PAYMENT PROCESSING SYSTEM 🏦")
        print("=" * 60)
        print("Powered by Factory & Singleton Design Patterns")
        print("=" * 60)
    
    def display_payment_methods(self):
        """Display available payment methods"""
        print("\n💳 Available Payment Methods:")
        print("1. Credit Card")
        print("2. PayPal")
        print("3. Bank Transfer")
        print("4. Cryptocurrency")
        print("5. Google Pay")
        print("6. View Transaction History")
        print("7. Exit")
    
    def get_payment_amount(self):
        """Get payment amount from user"""
        while True:
            try:
                amount = float(input("\n💰 Enter payment amount: $"))
                if amount > 0:
                    return amount
                else:
                    print("❌ Please enter a positive amount.")
            except ValueError:
                print("❌ Please enter a valid number.")
    
    def get_credit_card_details(self, amount):
        """Get credit card details from user"""
        print(f"\n💳 Processing Credit Card Payment for ${amount:.2f}")
        print("-" * 50)
        
        cardholder_name = input("👤 Cardholder Name: ")
        card_number = input("💳 Card Number (16 digits): ")
        cvv = input("🔐 CVV (3 digits): ")
        expiry_date = input("📅 Expiry Date (MM/YY): ")
        
        return {
            'cardholder_name': cardholder_name,
            'card_number': card_number,
            'cvv': cvv,
            'expiry_date': expiry_date
        }
    
    def get_paypal_details(self, amount):
        """Get PayPal details from user"""
        print(f"\n🅿️ Processing PayPal Payment for ${amount:.2f}")
        print("-" * 50)
        
        email = input("📧 PayPal Email: ")
        
        return {'email': email}
    
    def get_bank_transfer_details(self, amount):
        """Get bank transfer details from user"""
        print(f"\n🏦 Processing Bank Transfer for ${amount:.2f}")
        print("-" * 50)
        
        bank_name = input("🏛️ Bank Name: ")
        account_number = input("🔢 Account Number: ")
        routing_number = input("🔀 Routing Number (9 digits): ")
        
        return {
            'bank_name': bank_name,
            'account_number': account_number,
            'routing_number': routing_number
        }
    
    def get_crypto_details(self, amount):
        """Get cryptocurrency details from user"""
        print(f"\n₿ Processing Cryptocurrency Payment for ${amount:.2f}")
        print("-" * 50)
        
        crypto_types = ["Bitcoin", "Ethereum", "Litecoin", "Dogecoin"]
        print("Available cryptocurrencies:")
        for i, crypto in enumerate(crypto_types, 1):
            print(f"{i}. {crypto}")
        
        while True:
            try:
                choice = int(input("Select cryptocurrency (1-4): "))
                if 1 <= choice <= 4:
                    crypto_type = crypto_types[choice-1]
                    break
                else:
                    print("❌ Please select a valid option (1-4).")
            except ValueError:
                print("❌ Please enter a valid number.")
        
        wallet_address = input(f"🔐 {crypto_type} Wallet Address: ")
        
        return {
            'crypto_type': crypto_type,
            'wallet_address': wallet_address
        }
    
    def get_google_pay_details(self, amount):
        """Get Google Pay details from user"""
        print(f"\n📱 Processing Google Pay Payment for ${amount:.2f}")
        print("-" * 50)
        
        google_account = input("📧 Google Account (Gmail): ")
        phone_number = input("📱 Phone Number: ")
        
        return {
            'google_account': google_account,
            'phone_number': phone_number
        }
    
    def display_payment_result(self, result):
        """Display payment processing result"""
        print("\n" + "=" * 60)
        
        if result['status'] == 'success':
            print("✅ PAYMENT SUCCESSFUL!")
            print("=" * 60)
            print(f"🆔 Transaction ID: {result['transaction_id']}")
            print(f"💳 Payment Method: {result['payment_method']}")
            print(f"💰 Amount: ${result['amount']:.2f}")
            print(f"🕒 Timestamp: {result['timestamp']}")
            
            # Display method-specific details
            if 'cardholder_name' in result:
                print(f"👤 Cardholder: {result['cardholder_name']}")
                print(f"💳 Card: {result['card_last_four']}")
            elif 'email' in result:
                print(f"📧 Email: {result['email']}")
            elif 'bank_name' in result:
                print(f"🏛️ Bank: {result['bank_name']}")
                print(f"🔢 Account: {result['account_last_four']}")
            elif 'crypto_type' in result:
                print(f"₿ Cryptocurrency: {result['crypto_type']}")
                print(f"🔐 Wallet: {result['wallet_address']}")
            elif 'phone_number' in result:
                print(f"📧 Account: {result['account']}")
                print(f"📱 Phone: {result['phone_number']}")
            
        else:
            print("❌ PAYMENT FAILED!")
            print("=" * 60)
            print(f"🚫 Error: {result['message']}")
            print(f"🕒 Timestamp: {result['timestamp']}")
        
        print("=" * 60)
    
    def display_transaction_history(self):
        """Display transaction history"""
        history = self.gateway.get_transaction_history()
        
        print("\n" + "=" * 60)
        print("📋 TRANSACTION HISTORY")
        print("=" * 60)
        
        if not history:
            print("No transactions found.")
        else:
            successful = sum(1 for txn in history if txn.get('status') == 'success')
            total_amount = sum(txn.get('amount', 0) for txn in history if txn.get('status') == 'success')
            
            print(f"Total Transactions: {len(history)}")
            print(f"Successful: {successful}")
            print(f"Failed: {len(history) - successful}")
            print(f"Total Amount Processed: ${total_amount:.2f}")
            print("-" * 60)
            
            for i, txn in enumerate(history, 1):
                status_icon = "✅" if txn.get('status') == 'success' else "❌"
                print(f"{i}. {status_icon} {txn.get('payment_method', 'Unknown')} - "
                      f"${txn.get('amount', 0):.2f} - {txn.get('timestamp', 'Unknown')}")
        
        print("=" * 60)
    
    def run(self):
        """Main application loop"""
        self.display_welcome()
        
        while True:
            self.display_payment_methods()
            
            try:
                choice = input("\n🔢 Select payment method (1-7): ")
                
                if choice == '1':  # Credit Card
                    amount = self.get_payment_amount()
                    details = self.get_credit_card_details(amount)
                    result = self.gateway.process_payment(PaymentType.CREDIT_CARD, amount, **details)
                    self.display_payment_result(result)
                
                elif choice == '2':  # PayPal
                    amount = self.get_payment_amount()
                    details = self.get_paypal_details(amount)
                    result = self.gateway.process_payment(PaymentType.PAYPAL, amount, **details)
                    self.display_payment_result(result)
                
                elif choice == '3':  # Bank Transfer
                    amount = self.get_payment_amount()
                    details = self.get_bank_transfer_details(amount)
                    result = self.gateway.process_payment(PaymentType.BANK_TRANSFER, amount, **details)
                    self.display_payment_result(result)
                
                elif choice == '4':  # Cryptocurrency
                    amount = self.get_payment_amount()
                    details = self.get_crypto_details(amount)
                    result = self.gateway.process_payment(PaymentType.CRYPTO, amount, **details)
                    self.display_payment_result(result)
                
                elif choice == '5':  # Google Pay
                    amount = self.get_payment_amount()
                    details = self.get_google_pay_details(amount)
                    result = self.gateway.process_payment(PaymentType.GOOGLE_PAY, amount, **details)
                    self.display_payment_result(result)
                
                elif choice == '6':  # Transaction History
                    self.display_transaction_history()
                
                elif choice == '7':  # Exit
                    print("\n👋 Thank you for using our Payment Processing System!")
                    print("💼 Goodbye!")
                    break
                
                else:
                    print("❌ Invalid choice. Please select 1-7.")
                
                # Ask if user wants to continue
                if choice in ['1', '2', '3', '4', '5']:
                    input("\n⏎ Press Enter to continue...")
            
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ An error occurred: {str(e)}")
                input("⏎ Press Enter to continue...")

# Main execution
if __name__ == "__main__":
    app = PaymentUI()
    app.run()