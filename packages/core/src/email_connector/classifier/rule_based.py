"""Rule-based email classifier.

This module implements a simple rule-based email classifier
that uses pattern matching on email attributes.
"""

import logging
import re
from dataclasses import dataclass
from typing import Callable

from email_connector.interfaces.classifier import EmailClassifier
from email_connector.interfaces.models import (
    ClassificationResult,
    EmailMessage,
)

logger = logging.getLogger(__name__)


@dataclass
class ClassificationRule:
    """
    A single classification rule.

    Attributes
    ----------
    name : str
        Human-readable rule name for debugging.
    category : str
        Category to assign when rule matches.
    condition : Callable[[EmailMessage], bool]
        Function that returns True if rule matches.
    confidence : float
        Confidence score when this rule matches.
    suggested_action : str | None
        Suggested action when rule matches.
    priority : int
        Rule priority (higher = checked first).
    """

    name: str
    category: str
    condition: Callable[[EmailMessage], bool]
    confidence: float = 0.8
    suggested_action: str | None = None
    priority: int = 0


class RuleBasedClassifier(EmailClassifier):
    """
    Rule-based email classifier using pattern matching.

    This classifier applies a set of rules in priority order and
    returns the first matching rule's category.

    Parameters
    ----------
    rules : list[ClassificationRule] | None, optional
        Initial rules to use, by default None (empty).
    default_category : str, optional
        Category for emails that match no rules, by default "uncategorized".

    Examples
    --------
    >>> classifier = RuleBasedClassifier()
    >>> classifier.add_rule(ClassificationRule(
    ...     name="newsletter",
    ...     category="newsletter",
    ...     condition=lambda m: "unsubscribe" in m.body.lower(),
    ...     confidence=0.9,
    ...     suggested_action="archive",
    ... ))
    >>> result = classifier.classify(message)
    """

    def __init__(
        self,
        rules: list[ClassificationRule] | None = None,
        default_category: str = "uncategorized",
    ) -> None:
        self._rules: list[ClassificationRule] = rules or []
        self._default_category = default_category
        self._sort_rules()

    def _sort_rules(self) -> None:
        """Sort rules by priority (descending)."""
        self._rules.sort(key=lambda r: r.priority, reverse=True)

    def add_rule(self, rule: ClassificationRule) -> None:
        """
        Add a classification rule.

        Parameters
        ----------
        rule : ClassificationRule
            Rule to add.
        """
        self._rules.append(rule)
        self._sort_rules()
        logger.debug(f"Added rule: {rule.name}")

    def remove_rule(self, rule_name: str) -> bool:
        """
        Remove a rule by name.

        Parameters
        ----------
        rule_name : str
            Name of rule to remove.

        Returns
        -------
        bool
            True if rule was found and removed.
        """
        original_count = len(self._rules)
        self._rules = [r for r in self._rules if r.name != rule_name]
        removed = len(self._rules) < original_count

        if removed:
            logger.debug(f"Removed rule: {rule_name}")

        return removed

    def classify(self, message: EmailMessage) -> ClassificationResult:
        """
        Classify a single email message.

        Parameters
        ----------
        message : EmailMessage
            Message to classify.

        Returns
        -------
        ClassificationResult
            Classification result with category and confidence.
        """
        for rule in self._rules:
            try:
                if rule.condition(message):
                    logger.debug(
                        f"Message {message.id} matched rule: {rule.name}"
                    )
                    return ClassificationResult(
                        message_id=message.id,
                        category=rule.category,
                        confidence=rule.confidence,
                        suggested_action=rule.suggested_action,
                        reasoning=f"Matched rule: {rule.name}",
                    )
            except Exception as e:
                logger.warning(f"Rule '{rule.name}' raised exception: {e}")
                continue

        logger.debug(f"Message {message.id} matched no rules")
        return ClassificationResult(
            message_id=message.id,
            category=self._default_category,
            confidence=0.5,
            reasoning="No rules matched",
        )

    @property
    def categories(self) -> list[str]:
        """
        List of possible categories.

        Returns
        -------
        list[str]
            Unique categories from all rules plus default.
        """
        cats = {rule.category for rule in self._rules}
        cats.add(self._default_category)
        return sorted(cats)

    def train(self, messages: list[EmailMessage], labels: list[str]) -> None:
        """
        Training is not supported for rule-based classifier.

        This method is a no-op for rule-based classification.
        Use add_rule() to add new classification rules.

        Parameters
        ----------
        messages : list[EmailMessage]
            Ignored.
        labels : list[str]
            Ignored.
        """
        logger.warning(
            "Rule-based classifier does not support training. Use add_rule() "
            "instead."
        )


# Pre-built rule factories for common patterns
def sender_contains_rule(
    pattern: str,
    category: str,
    confidence: float = 0.85,
    suggested_action: str | None = None,
) -> ClassificationRule:
    """
    Create a rule that matches sender address pattern.

    Parameters
    ----------
    pattern : str
        Regex pattern to match in sender address.
    category : str
        Category to assign.
    confidence : float, optional
        Confidence score, by default 0.85.
    suggested_action : str | None, optional
        Suggested action, by default None.

    Returns
    -------
    ClassificationRule
        Configured rule.
    """
    compiled = re.compile(pattern, re.IGNORECASE)
    return ClassificationRule(
        name=f"sender_contains:{pattern}",
        category=category,
        condition=lambda m: bool(compiled.search(m.sender)),
        confidence=confidence,
        suggested_action=suggested_action,
    )


def subject_contains_rule(
    pattern: str,
    category: str,
    confidence: float = 0.8,
    suggested_action: str | None = None,
) -> ClassificationRule:
    """
    Create a rule that matches subject pattern.

    Parameters
    ----------
    pattern : str
        Regex pattern to match in subject.
    category : str
        Category to assign.
    confidence : float, optional
        Confidence score, by default 0.8.
    suggested_action : str | None, optional
        Suggested action, by default None.

    Returns
    -------
    ClassificationRule
        Configured rule.
    """
    compiled = re.compile(pattern, re.IGNORECASE)
    return ClassificationRule(
        name=f"subject_contains:{pattern}",
        category=category,
        condition=lambda m: bool(compiled.search(m.subject)),
        confidence=confidence,
        suggested_action=suggested_action,
    )


def body_contains_rule(
    pattern: str,
    category: str,
    confidence: float = 0.75,
    suggested_action: str | None = None,
) -> ClassificationRule:
    """
    Create a rule that matches body pattern.

    Parameters
    ----------
    pattern : str
        Regex pattern to match in body.
    category : str
        Category to assign.
    confidence : float, optional
        Confidence score, by default 0.75.
    suggested_action : str | None, optional
        Suggested action, by default None.

    Returns
    -------
    ClassificationRule
        Configured rule.
    """
    compiled = re.compile(pattern, re.IGNORECASE)
    return ClassificationRule(
        name=f"body_contains:{pattern}",
        category=category,
        condition=lambda m: bool(compiled.search(m.body)),
        confidence=confidence,
        suggested_action=suggested_action,
    )
