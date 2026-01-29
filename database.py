import sqlite3
from datetime import datetime
import json

class SimpleDatabase:
    def __init__(self, db_name="fraud.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            name TEXT,
            email TEXT,
            created_at TIMESTAMP,
            account_age_days INTEGER DEFAULT 0,
            risk_score INTEGER DEFAULT 0
        )
        ''')
        
        # Transactions table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id TEXT PRIMARY KEY,
            user_id TEXT,
            amount REAL,
            recipient_id TEXT,
            timestamp TIMESTAMP,
            fraud_score INTEGER DEFAULT 0,
            status TEXT DEFAULT 'pending'
        )
        ''')
        
        # Sessions table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            user_id TEXT,
            login_time TIMESTAMP,
            ip_address TEXT,
            device_id TEXT
        )
        ''')
        
        # Rules table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS rules (
            rule_id TEXT PRIMARY KEY,
            name TEXT,
            description TEXT,
            conditions TEXT,  -- Store as JSON
            actions TEXT,     -- Store as JSON
            severity TEXT,
            is_active INTEGER DEFAULT 1
        )
        ''')
        
        self.conn.commit()
    
    def add_user(self, user_id, name, email):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO users (user_id, name, email, created_at) 
        VALUES (?, ?, ?, ?)
        ''', (user_id, name, email, datetime.now()))
        self.conn.commit()
    
    def add_transaction(self, transaction_id, user_id, amount, recipient_id):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO transactions (transaction_id, user_id, amount, recipient_id, timestamp)
        VALUES (?, ?, ?, ?, ?)
        ''', (transaction_id, user_id, amount, recipient_id, datetime.now()))
        self.conn.commit()
    
    def update_fraud_score(self, transaction_id, score):
        cursor = self.conn.cursor()
        cursor.execute('''
        UPDATE transactions SET fraud_score = ? WHERE transaction_id = ?
        ''', (score, transaction_id))
        self.conn.commit()
    
    def get_user_info(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        return cursor.fetchone()
    
    def get_user_transactions(self, user_id, hours=24):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT COUNT(*), SUM(amount) 
        FROM transactions 
        WHERE user_id = ? AND timestamp > datetime('now', ?)
        ''', (user_id, f'-{hours} hours'))
        return cursor.fetchone()
    def get_all_transactions(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM transactions')
        return cursor.fetchall()
    
    def close(self):
        self.conn.close()

# Initialize database
db = SimpleDatabase()