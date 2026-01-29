import uuid
from datetime import datetime, timedelta
import random

def generate_sample_users(db, count=10):
    """Generate sample users"""
    first_names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry", "Ivy", "Jack"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]
    
    for i in range(count):
        user_id = f"user_{i+1:03d}"
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        email = f"{name.lower().replace(' ', '.')}@example.com"
        db.add_user(user_id, name, email)
        print(f"Created user: {user_id} - {name}")

def generate_sample_transactions(db, days=30):
    """Generate sample transactions (mix of normal and suspicious)"""
    user_ids = [f"user_{i:03d}" for i in range(1, 11)]
    
    # Normal transactions
    for _ in range(100):
        user_id = random.choice(user_ids)
        amount = random.uniform(10, 5000)
        recipient = random.choice([u for u in user_ids if u != user_id])
        
        transaction_id = str(uuid.uuid4())[:8]
        db.add_transaction(transaction_id, user_id, amount, recipient)
    
    # Suspicious: New user large transfer (Rule 1)
    db.add_transaction("SUSP001", "user_001", 15000, "user_002")  # Should trigger Rule 1
    
    # Suspicious: Rapid transactions (Rule 2)
    for i in range(6):
        db.add_transaction(f"RAPID{i}", "user_003", 50, f"user_{random.randint(4,10):03d}")
    
    # Suspicious: Test pattern (Rule 4)
    db.add_transaction("TEST1", "user_004", 0.99, "user_005")
    db.add_transaction("TEST2", "user_004", 1.50, "user_005")
    db.add_transaction("TEST3", "user_004", 0.75, "user_005")
    db.add_transaction("TEST4", "user_004", 8000, "user_005")  # Large after small
    
    print("Generated sample transactions")

def get_sample_context(user_id):
    """Generate sample context data for a user"""
    # In real system, this would come from database
    return {
        "user_id": user_id,
        "account_age_days": random.choice([1, 5, 30, 100]),  # Mix of new and old accounts
        "transactions_last_hour": random.randint(0, 10),
        "avg_amount": random.uniform(50, 2000),
        "country_changes_last_24h": random.randint(1, 5),
        "small_transactions_last_hour": random.randint(0, 5),
        "hour_of_day": random.randint(0, 23)  # Current hour
    }