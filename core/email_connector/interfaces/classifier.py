"""Email classifier interface.

This module defines the abstract base class for email classifiers.
Different classification strategies (rule-based, ML, LLM) implement this
interface.
"""

from abc import ABC, abstractmethod

from email_connector.interfaces.models import (
    ClassificationResult,
    EmailMessage,
)


class EmailClassifier(ABC):
    """
    Abstract email classifier for categorizing messages.

    This interface defines the contract for email classification strategies.
    Implementations can use rule-based logic, machine learning models,
    or LLM-based classification.

    Examples
    --------
    >>> classifier = RuleBasedClassifier(rules=my_rules)
    >>> result = classifier.classify(message)
    >>> print(f"Category: {result.category}, Confidence: {result.confidence}")
    """

    @abstractmethod
    def classify(self, message: EmailMessage) -> ClassificationResult:
        """
        Classify a single email message.

        Parameters
        ----------
        message : EmailMessage
            The email message to classify.

        Returns
        -------
        ClassificationResult
            Classification result with category and confidence.
        """
        pass

    def classify_batch(
        self,
        messages: list[EmailMessage],
    ) -> list[ClassificationResult]:
        """
        Classify multiple email messages.

        Default implementation calls classify() for each message.
        Subclasses may override for batch optimization.

        Parameters
        ----------
        messages : list[EmailMessage]
            List of email messages to classify.

        Returns
        -------
        list[ClassificationResult]
            List of classification results in the same order as input.
        """
        return [self.classify(msg) for msg in messages]

    @property
    @abstractmethod
    def categories(self) -> list[str]:
        """
        List of possible classification categories.

        Returns
        -------
        list[str]
            All categories this classifier can assign.
        """
        pass

    @abstractmethod
    def train(self, messages: list[EmailMessage], labels: list[str]) -> None:
        """
        Train or update the classifier with labeled examples.

        For rule-based classifiers, this may be a no-op or update rules.
        For ML classifiers, this trains the underlying model.

        Parameters
        ----------
        messages : list[EmailMessage]
            Training examples.
        labels : list[str]
            Category labels for each message.

        Raises
        ------
        ValueError
            If messages and labels have different lengths.
        """
        pass
