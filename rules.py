from dataclasses import dataclass
from typing import List, Dict, Any, Callable
import json
from lib.rule_schema import *
Rule_list=[
    Rule(
        rule_id="R001",
        name="New User Large Transfer",
        description="Account less than 7 days old sending over $10,000",
        conditions=[
            Condition("account_age_days", "<", 7),
            Condition("amount", ">", 10000)
        ],
        actions=["hold_transaction", "require_mfa", "alert_admin"],
        severity="high",
        score=40
    ),
    Rule(
        rule_id="R002",
        name="Rapid Transaction Spam",
        description="More than 5 transactions in last hour",
        conditions=[
            Condition("transactions_last_hour", ">", 5),
            Condition("avg_amount", "<", 100)
        ],
        actions=["limit_velocity", "alert_user"],
        severity="medium",
        score=30
    ),
    Rule(
        rule_id="R003",
        name="Geographic Hopping",
        description="Transactions from multiple countries in short time",
        conditions=[
            Condition("country_changes_last_24h", ">=", 3),
            Condition("account_age_days", ">", 30)  # Not new users
        ],
        actions=["require_mfa", "flag_account"],
        severity="high",
        score=50
    ),
    Rule(
        rule_id="R004",
        name="Test Transaction Pattern",
        description="Multiple small transactions before large one",
        conditions=[
            Condition("small_transactions_last_hour", ">=", 3),
            Condition("amount", ">", 5000)
        ],
        actions=["hold_transaction", "investigate"],
        severity="medium",
        score=35
    ),
    Rule(
        rule_id="R005",
        name="Unusual Transaction Time",
        description="Large transaction at unusual hour (2AM-5AM)",
        conditions=[
            Condition("hour_of_day", ">=", 2),
            Condition("hour_of_day", "<=", 5),
            Condition("amount", ">", 2000)
        ],
        actions=["alert_user", "monitor"],
        severity="low",
        score=20
    )
]

class RuleManager:
    """Manages all fraud detection rules"""
    
    def __init__(self):
        self.rules: List[Rule] = []
    
    def add_rule(self, rule: Rule):
        """Add a rule to the manager"""
        self.rules.append(rule)
    
    def load_sample_rules(self):
        """Load some example rules"""
        # Rule 1: New user making large transfer
        for rule in Rule_list:
            self.add_rule(rule)
    
    def evaluate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate all rules against data"""
        results = []
        total_score = 0
        all_actions = []
        
        for rule in self.rules:
            result = rule.check(data)
            results.append(result)
            
            if result["triggered"]:
                total_score += result["score"]
                all_actions.extend(result["actions"])
        
        # Cap score at 100
        total_score = min(total_score, 100)
        
        # Determine risk level
        if total_score >= 70:
            risk_level = "HIGH"
        elif total_score >= 40:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        return {
            "fraud_score": total_score,
            "risk_level": risk_level,
            "triggered_rules": [r for r in results if r["triggered"]],
            "recommended_actions": list(set(all_actions)),  # Remove duplicates
            "all_rules_checked": len(results)
        }