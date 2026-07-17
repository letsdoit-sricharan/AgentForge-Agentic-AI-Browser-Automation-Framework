from enum import Enum

class NavigationDecision(Enum):
    ABORT = "ABORT"
    RETRY = "RETRY"
    CONTINUE = "CONTINUE"

class NavigationStrategy:
    def on_failure(self, retry_available: bool, checkpoint_available: bool) -> NavigationDecision:
        if retry_available:
            return NavigationDecision.RETRY
        return NavigationDecision.ABORT
