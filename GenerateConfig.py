from typing_extensions import Required, NotRequired, TypedDict

class GenerateConfig(TypedDict):
    model: Required[str]
    temperature: NotRequired[float]
    top_p: NotRequired[float]
    max_tokens: Required[int]
    n: NotRequired[int]
    stop: Required[str]