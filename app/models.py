from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime


class ModerationSettings(BaseModel):
    enabled: bool
    threshold: Optional[float] = Field(default=None, nullable=True)


class MaskSettings(BaseModel):
    remove_entity_value: bool


class InputRanges(BaseModel):
    start: int
    end: int


class Moderations(BaseModel):
    hap: Optional[ModerationSettings] = Field(default=None, nullable=True)
    pii: Optional[ModerationSettings] = Field(default=None, nullable=True)
    input_ranges: Optional[InputRanges] = Field(default=None, nullable=True)
    mask: Optional[MaskSettings] = Field(default=None, nullable=True)


class LengthPenalty(BaseModel):
    decay_factor: float
    start_index: int


class ReturnOptions(BaseModel):
    input_text: Optional[bool] = Field(default=False, nullable=True)
    generated_tokens: Optional[bool] = Field(default=False, nullable=True)
    input_tokens: Optional[bool] = Field(default=False, nullable=True)
    token_logprobs: Optional[bool] = Field(default=False, nullable=True)
    token_ranks: Optional[bool] = Field(default=False, nullable=True)
    top_n_tokens: Optional[int] = Field(default=0, nullable=True)


class Parameters(BaseModel):
    decoding_method: Optional[str] = Field(default="greedy", nullable=True)
    length_penalty: Optional[LengthPenalty] = Field(default=None, nullable=True)
    time_limit: Optional[int] = Field(default=None, nullable=True)
    temperature: Optional[float] = Field(default=None, nullable=True)
    top_p: Optional[float] = Field(default=None, nullable=True)
    top_k: Optional[int] = Field(default=None, nullable=True)
    random_seed: Optional[int] = Field(default=None, nullable=True)
    repetition_penalty: Optional[float] = Field(default=None, nullable=True)
    min_new_tokens: Optional[int] = Field(default=None, nullable=True)
    max_new_tokens: Optional[int] = Field(default=None, nullable=True)
    stop_sequences: Optional[List[str]] = []
    truncate_input_tokens: Optional[int] = Field(default=None, nullable=True)
    include_stop_sequence: Optional[bool] = Field(default=None, nullable=True)
    return_options: Optional[ReturnOptions] = Field(default=None, nullable=True)


class GenerateRequest(BaseModel):
    model_id: str = Field(default=None, nullable=True)
    input: str
    moderations: Optional[Moderations] = Field(default=None, nullable=True)
    parameters: Optional[Parameters] = Field(default=None, nullable=True)
    project_id: str = Field(default=None, nullable=True)


class ModerationEntry(BaseModel):
    score: float
    input: bool
    position: InputRanges
    entity: str


class ModerationsOutput(BaseModel):
    pii: Optional[List[ModerationEntry]] = Field(default=None, nullable=True)
    hap: Optional[List[ModerationEntry]] = Field(default=None, nullable=True)


class Result(BaseModel):
    generated_text: str
    generated_token_count: Optional[int] = Field(default=None, nullable=True)
    input_token_count: Optional[int] = Field(default=None, nullable=True)
    stop_reason: Optional[str] = Field(default=None, nullable=True)
    moderations: Optional[ModerationsOutput] = Field(default=None, nullable=True)


class GenerateResponse(BaseModel):
    model_id: str
    created_at: datetime
    results: List[Result]
