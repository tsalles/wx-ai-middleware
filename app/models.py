import os

from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional, Union, Literal
from datetime import datetime


class ModerationSettings(BaseModel):
    enabled: bool
    threshold: float = Field(default=None, nullable=True)


class MaskSettings(BaseModel):
    remove_entity_value: bool


class InputRanges(BaseModel):
    start: int
    end: int


class Moderations(BaseModel):
    hap: ModerationSettings = None  # Field(default=None, nullable=True)
    pii: ModerationSettings = None  # Field(default=None, nullable=True)
    input_ranges: InputRanges = None  # Field(default=None, nullable=True)
    mask: MaskSettings = None  # Field(default=None, nullable=True)


class LengthPenalty(BaseModel):
    decay_factor: float
    start_index: int


class ReturnOptions(BaseModel):
    input_text: bool = Field(default=False, nullable=True)
    generated_tokens: bool = Field(default=False, nullable=True)
    input_tokens: bool = Field(default=False, nullable=True)
    token_logprobs: bool = Field(default=False, nullable=True)
    token_ranks: bool = Field(default=False, nullable=True)
    top_n_tokens: int = Field(default=0, nullable=True)


class Parameters(BaseModel):
    decoding_method: str = Field(default="greedy", nullable=True)
    length_penalty: LengthPenalty = None  # Field(default=None, nullable=True)
    time_limit: int = Field(default=None, nullable=True)
    temperature: float = Field(default=None, nullable=True)
    top_p: float = Field(default=None, nullable=True)
    top_k: int = Field(default=None, nullable=True)
    random_seed: int = Field(default=None, nullable=True)
    repetition_penalty: float = Field(default=None, nullable=True)
    min_new_tokens: int = Field(default=None, nullable=True)
    max_new_tokens: int = Field(default=None, nullable=True)
    stop_sequences: List[str] = Field(default=None, nullable=True)
    truncate_input_tokens: int = Field(default=None, nullable=True)
    include_stop_sequence: bool = Field(default=None, nullable=True)
    return_options: ReturnOptions = None  # Field(default=None, nullable=True)


class GenerateRequest(BaseModel):
    model_id: str = Field(default=None, nullable=True)
    input: str
    moderations: Moderations = None
    parameters: Parameters = None
    project_id: str = Field(default=None, nullable=True)


class ModerationEntry(BaseModel):
    score: float
    input: bool
    position: InputRanges
    entity: str


class ModerationsOutput(BaseModel):
    pii: List[ModerationEntry] = None  # Field(default=None, nullable=True)
    hap: List[ModerationEntry] = None  # Field(default=None, nullable=True)


class Result(BaseModel):
    generated_text: str
    generated_token_count: int = Field(default=None, nullable=True)
    input_token_count: int = Field(default=None, nullable=True)
    stop_reason: str = Field(default=None, nullable=True)
    moderations: ModerationsOutput = None


class GenerateResponse(BaseModel):
    model_id: str
    created_at: datetime
    results: List[Result]


class GenerateRequestSimple(BaseModel):
    model_id: str = Field(default=os.getenv('WATSONX_MODEL'), nullable=True)
    input: str
    decoding_method: Optional[Literal["greedy", "sample"]] = "greedy"
    temperature: float = Field(default=None, nullable=True)
    top_p: float = Field(default=1.0, nullable=True)
    top_k: int = Field(default=50, nullable=True)
    stop_sequences: List[str] = Field(default=None, nullable=True)
    project_id: str = Field(default=os.getenv('WATSONX_PROJECT_ID'), nullable=True)


class GenerateResponseSimple(BaseModel):
    generated_text: str
