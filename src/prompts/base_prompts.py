from typing import Dict, Any

class BasePrompt:
    """Base class for all prompts"""
    
    @classmethod
    def get_system_prompt(cls) -> str:
        """Returns the system prompt"""
        raise NotImplementedError
    
    @classmethod
    def get_human_prompt(cls, **kwargs) -> str:
        """Returns the human prompt with variables substituted"""
        raise NotImplementedError

class PromptTemplate:
    @staticmethod
    def format_dict(d: Dict[str, Any], indent: int = 2) -> str:
        """Helper method to format dictionary data nicely"""
        if not d:
            return "{}"
        return "\n".join(f"{' ' * indent}- {k}: {v}" for k, v in d.items())