class FeatureFlagError(Exception):
    """Base exception for SDK errors."""

class FeatureFlagTransportError(FeatureFlagError):
    """Raised when the platform cannot be reached or returns an invalid response."""

class FeatureFlagEvaluationError(FeatureFlagError):
    """Raised when evaluation fails for a semantic reason."""
