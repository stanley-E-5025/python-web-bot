import sys
from pathlib import Path

tenant_directory, root_dir = (
    Path(__file__).resolve().parent.parent,
    Path(__file__).resolve().parent.parent.parent,
)
sys.path.insert(0, str(root_dir))
sys.path.append(str(tenant_directory))

from config import openai


class OpenAIClient:
    def generate_text(
        self,
        input_prompt,
        max_response_length=10,
        num_responses=1,
        stopping_phrases=None,
        creativity_temperature=1.0,
        engine="text-davinci-002",
    ):
        response = openai.Completion.create(
            engine=engine,
            prompt=input_prompt,
            max_tokens=max_response_length,
            n=num_responses,
            stop=stopping_phrases,
            temperature=creativity_temperature,
        )
        return response.choices[0].text.strip()
