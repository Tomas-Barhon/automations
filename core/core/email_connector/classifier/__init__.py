"""Email classifier implementations."""

from email_connector.classifier.rule_based import (
    RuleBasedClassifier,
    sender_contains_rule,
)

__all__ = [
    "RuleBasedClassifier",
    "sender_contains_rule",
]
