"""
Base tool class for MCP tools
"""
from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseTool(ABC):
    """
    Abstract base class for all MCP tools
    """
    name: str = ""
    description: str = ""

    @abstractmethod
    async def execute(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Execute the tool with the given parameters

        Args:
            *args: Positional arguments for the tool
            **kwargs: Keyword arguments for the tool

        Returns:
            Dictionary containing the result of the tool execution
        """
        pass

    def get_spec(self) -> Dict[str, Any]:
        """
        Get the specification for this tool.

        Returns:
            Dictionary containing the tool specification
        """
        return {
            "name": self.name,
            "description": self.description,
            "execute": self.execute
        }