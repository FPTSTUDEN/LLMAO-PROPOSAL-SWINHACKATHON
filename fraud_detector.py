import os

def delete_file(filepath):
    """Delete a file if it exists"""
    try:
        os.remove(filepath)
        print(f"Deleted file: {filepath}")
    except FileNotFoundError:
        pass
delete_file("fraud.db")  # Clean slate for demo

from lib.fraud_detector_schema import FraudDetector, interactive_mode
from database import SimpleDatabase
from rules import RuleManager
from sample_data import generate_sample_users, generate_sample_transactions, get_sample_context
import uuid
from datetime import datetime


class SimpleFraudDetector(FraudDetector):
    
    def run_demo(self):
        """Run a demo with sample data"""
        print("Setting up demo...")
        
        # Clear and setup
        # self.db = SimpleDatabase()
        
        # Generate sample data
        generate_sample_users(self.db, 5)
        generate_sample_transactions(self.db)
        
        print("\n" + "="*50)
        print("DEMO: Fraud Detection on Sample Transactions")
        print("="*50)
        
        for result in self.analyze_all_transactions():
            if result["fraud_score"] > 0:
                self.print_result(result)

        self.db.close()


if __name__ == "__main__":
    # delete_file("fraud.db")  # Clean slate for demo
    # Run the demo
    detector = SimpleFraudDetector()
    detector.run_demo()
    
    # Uncomment to run interactive mode
    interactive_mode(detector)