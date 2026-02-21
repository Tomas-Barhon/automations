from enum import Enum
from pathlib import Path
from typing import Literal


class PromptType(Enum):
    SYSTEM = "system"
    HUMAN = "human"


class PromptLoader:
    def __init__(self, prompt_dir: Path | str) -> None:
        if isinstance(prompt_dir, str):
            prompt_dir = Path(prompt_dir)
        self.prompt_dir = prompt_dir

    def load_prompt(
        self, prompt_file_name: Path | str, prompt_type: PromptType
    ) -> dict[str, str]:
        assert prompt_type in PromptType, f"Invalid prompt type: {prompt_type}"
        assert isinstance(
            prompt_file_name, (str, Path)
        ), f"""Prompt file name must be a string or Path, got:
            {type(prompt_file_name)}"""

        if isinstance(prompt_file_name, str):
            prompt_file_name = Path(prompt_file_name)
        prompt_file_path = self.prompt_dir / prompt_file_name
        with open(prompt_file_path, "r") as file:
            prompt = file.read()

        # TODO: Check whether the keys are correct in langchain
        return {"type": prompt_type.value, "content": prompt}
