from typing import Any

from rich.console   import Console
from rich.prompt    import Prompt

get_pm = lambda self, *a, **b: self.get_pm()

class SlazheCliModule:
    """
    Base class for Slazhe CLI modules.
    """

    def __init__(self, parent, **opts: dict[str, Any]) -> None:
        """
        Initialize the SlazheCliModule with a reference to the parent CLI.

        Args:
            parent (SlazheCli): The parent CLI instance.
        """
        self.parent: Any        = parent
        self.console: Console   = parent.console
        self.prompt: Prompt     = parent.prompt

        self.opts: dict[str, Any] = opts

    def get_pm(self) -> Any:
        if hasattr(self, 'pm'):
            return self.pm
        
        return None

# Version Globale: v00.00.00.pi
# Version du fichier: v00.00.00.02
