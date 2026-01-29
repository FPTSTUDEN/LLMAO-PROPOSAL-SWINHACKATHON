from dataclasses import dataclass
from typing import List, Dict, Any, Callable
import json

@dataclass
class Condition:
    """A single condition to check"""
    field: str          # e.g., "amount", "account_age_days"
    operator: str       # e.g., ">", "<", "==", "!=", "in"
    value: Any          # e.g., 10000, 7, ["US", "UK"]
    
    def check(self, data: Dict[str, Any]) -> bool:
        """Check if condition is true for given data"""
        actual_value = data.get(self.field)
        
        if self.operator == ">":
            return actual_value > self.value
        elif self.operator == "<":
            return actual_value < self.value
        elif self.operator == ">=":
            return actual_value >= self.value
        elif self.operator == "<=":
            return actual_value <= self.value
        elif self.operator == "==":
            return actual_value == self.value
        elif self.operator == "!=":
            return actual_value != self.value
        elif self.operator == "in":
            return actual_value in self.value
        elif self.operator == "not in":
            return actual_value not in self.value
        elif self.operator == "contains":
            return str(self.value) in str(actual_value)
        return False

@dataclass
class Rule:
    """A fraud detection rule"""
    rule_id: str
    name: str
    description: str
    conditions: List[Condition]
    actions: List[str]      # What to do if rule triggers
    severity: str          # "low", "medium", "high", "critical"
    score: int            # Points to add to fraud score (0-100)
    
    def check(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Check all conditions and return result"""
        triggered = all(condition.check(data) for condition in self.conditions)
        
        return {
            "rule_id": self.rule_id,
            "name": self.name,
            "triggered": triggered,
            "severity": self.severity,
            "score": self.score if triggered else 0,
            "actions": self.actions if triggered else []
        }
