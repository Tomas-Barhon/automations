from enum import Enum


class PromptType(Enum):
    SYSTEM = "system"
    HUMAN = "human"


class PromptLoader:
    def __init__(
        self,
        prompt_file_path: str,
        prompt_type: PromptType = PromptType.SYSTEM,
    ) -> None:
        self.prompt_file_path = prompt_file_path
        assert isinstance(prompt_file_path, str), (
            "Prompt file path must be a string."
        )
        assert prompt_file_path.endswith(".txt"), (
            "Prompt file must be a .txt file."
        )
        assert isinstance(prompt_type, PromptType), (
            "Prompt type must be an instance of PromptType."
        )
        self.prompt_type = prompt_type

    def load_prompt(self):
        with open(self.prompt_file_path, "r") as file:
            prompt = file.read()
        return prompt
