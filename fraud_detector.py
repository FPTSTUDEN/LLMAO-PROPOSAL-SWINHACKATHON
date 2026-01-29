import os
def delete_file(filepath):
    """Delete a file if it exists"""
    try:
        os.remove(filepath)
        print(f"Deleted file: {filepath}")
    except FileNotFoundError:
        pass
delete_file("fraud.db")  # Clean slate for demo
from database import SimpleDatabase
from rules import RuleManager
from sample_data import generate_sample_users, generate_sample_transactions, get_sample_context
import uuid
from datetime import datetime


class SimpleFraudDetector:
    def __init__(self):
        self.db = SimpleDatabase()
        self.rule_manager = RuleManager()
        self.rule_manager.load_sample_rules()
    
    def analyze_transaction(self, user_id, amount, recipient_id=None, context=None):
        """Analyze a single transaction for fraud"""
        
        # Generate transaction ID
        transaction_id = str(uuid.uuid4())[:8]
        
        # Get or create context
        if context is None:
            context = get_sample_context(user_id)
        
        # Add transaction-specific data
        context.update({
            "transaction_id": transaction_id,
            "user_id": user_id,
            "amount": amount,
            "recipient_id": recipient_id,
            "timestamp": datetime.now().isoformat()
        })
        
        # Evaluate rules
        result = self.rule_manager.evaluate(context)
        
        # Store transaction in database
        self.db.add_transaction(transaction_id, user_id, amount, recipient_id)
        self.db.update_fraud_score(transaction_id, result["fraud_score"])
        
        # Add result details
        result["transaction_id"] = transaction_id
        result["user_id"] = user_id
        result["amount"] = amount
        
        return result
    
    def print_result(self, result):
        """Print fraud analysis result nicely"""
        print("\n" + "="*50)
        print("FRAUD DETECTION RESULT")
        print("="*50)
        print(f"Transaction: {result['transaction_id']}")
        print(f"User: {result['user_id']}")
        print(f"Amount: ${result['amount']:,.2f}")
        print(f"Fraud Score: {result['fraud_score']}/100")
        print(f"Risk Level: {result['risk_level']}")
        
        if result["triggered_rules"]:
            print("\n⚠️  TRIGGERED RULES:")
            for rule in result["triggered_rules"]:
                print(f"  • {rule['name']} ({rule['severity'].upper()})")
                print(f"    Score: +{rule['score']}")
        
        if result["recommended_actions"]:
            print("\n🚨 RECOMMENDED ACTIONS:")
            for action in result["recommended_actions"]:
                print(f"  • {action}")
        
        print(f"\nTotal rules checked: {result['all_rules_checked']}")
        print("="*50)
    
    def run_demo(self):
        """Run a demo with sample data"""
        print("Setting up demo...")
        
        # Clear and setup
        self.db = SimpleDatabase()
        
        # Generate sample data
        generate_sample_users(self.db, 5)
        generate_sample_transactions(self.db)
        
        print("\n" + "="*50)
        print("DEMO: Fraud Detection on Sample Transactions")
        print("="*50)
        
        for transaction in self.db.get_all_transactions():
            user_id = transaction[1]
            amount = transaction[2]
            recipient_id = transaction[3]
            
            # Get context for user
            context = get_sample_context(user_id)
            
            # Analyze transaction
            result = self.analyze_transaction(user_id, amount, recipient_id, context)
            if result["fraud_score"] > 0:
                self.print_result(result)

        self.db.close()

# Interactive mode
def interactive_mode():
    """Run an interactive fraud detection session"""
    detector = SimpleFraudDetector()
    
    print("💳 Interactive Fraud Detector")
    print("Enter transaction details (or 'quit' to exit)")
    
    while True:
        print("\n" + "-"*30)
        user_id = input("User ID: ").strip()
        if user_id.lower() == 'quit':
            break
        
        try:
            amount = float(input("Amount: $").strip())
        except:
            print("Invalid amount!")
            continue
        
        recipient = input("Recipient ID (optional): ").strip() or None
        
        # Get some context
        print("\nProvide some context:")
        try:
            age = int(input("Account age in days: ").strip() or "30")
            txn_count = int(input("Transactions in last hour: ").strip() or "1")
            hour = int(input("Current hour (0-23): ").strip() or "12")
        except:
            print("Using default context...")
            age, txn_count, hour = 30, 1, 12
        
        context = {
            "account_age_days": age,
            "transactions_last_hour": txn_count,
            "avg_amount": amount,  # Simplified
            "country_changes_last_24h": 1,
            "small_transactions_last_hour": 1 if amount < 10 else 0,
            "hour_of_day": hour
        }
        
        # Analyze
        result = detector.analyze_transaction(user_id, amount, recipient, context)
        detector.print_result(result)

if __name__ == "__main__":
    # delete_file("fraud.db")  # Clean slate for demo
    # Run the demo
    detector = SimpleFraudDetector()
    detector.run_demo()
    
    # Uncomment to run interactive mode
    interactive_mode()