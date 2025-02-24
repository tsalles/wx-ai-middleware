from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
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
    hap: ModerationSettings = Field(default=None, nullable=True)
    pii: ModerationSettings = Field(default=None, nullable=True)
    input_ranges: InputRanges = Field(default=None, nullable=True)
    mask: MaskSettings = Field(default=None, nullable=True)


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
    length_penalty: LengthPenalty = Field(default=None, nullable=True)
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
    return_options: Optional[ReturnOptions] = Field(default=None, nullable=True)


class GenerateRequest(BaseModel):
    model_id: str = Field(default=None, nullable=True)
    input: str
    moderations: Moderations = Field(default=None, nullable=True)
    parameters: Parameters = Field(default=None, nullable=True)
    project_id: str = Field(default=None, nullable=True)


class ModerationEntry(BaseModel):
    score: float
    input: bool
    position: InputRanges
    entity: str


class ModerationsOutput(BaseModel):
    pii: List[ModerationEntry] = Field(default=None, nullable=True)
    hap: List[ModerationEntry] = Field(default=None, nullable=True)


class Result(BaseModel):
    generated_text: str
    generated_token_count: int = Field(default=None, nullable=True)
    input_token_count: int = Field(default=None, nullable=True)
    stop_reason: str = Field(default=None, nullable=True)
    moderations: ModerationsOutput = Field(default=None, nullable=True)


class GenerateResponse(BaseModel):
    model_id: str
    created_at: datetime
    results: List[Result]
