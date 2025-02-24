from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime


class ModerationSettings(BaseModel):
    enabled: bool
    threshold: Optional[float] = None

class MaskSettings(BaseModel):
    remove_entity_value: bool

class InputRanges(BaseModel):
    start: int
    end: int

class Moderations(BaseModel):
    hap: Optional[ModerationSettings] = None
    pii: Optional[ModerationSettings] = None
    input_ranges: Optional[InputRanges] = None
    mask: Optional[MaskSettings] = None

class LengthPenalty(BaseModel):
    decay_factor: float
    start_index: int

class ReturnOptions(BaseModel):
    input_text: Optional[bool] = False
    generated_tokens: Optional[bool] = False
    input_tokens: Optional[bool] = False
    token_logprobs: Optional[bool] = False
    token_ranks: Optional[bool] = False
    top_n_tokens: Optional[int] = 0

class Parameters(BaseModel):
    decoding_method: Optional[str] = 'greedy'
    length_penalty: Optional[LengthPenalty] = None
    time_limit: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    top_k: Optional[int] = None
    random_seed: Optional[int] = None
    repetition_penalty: Optional[float] = None
    min_new_tokens: Optional[int] = None
    max_new_tokens: Optional[int] = None
    stop_sequences: Optional[List[str]] = []
    truncate_input_tokens: Optional[int] = None
    include_stop_sequence: Optional[bool] = None
    return_options: Optional[ReturnOptions] = None

class GenerateRequest(BaseModel):
    model_id: str
    input: str
    moderations: Optional[Moderations] = None
    parameters: Optional[Parameters] = None
    project_id: str

class ModerationEntry(BaseModel):
    score: float
    input: bool
    position: InputRanges
    entity: str

class ModerationsOutput(BaseModel):
    pii: Optional[List[ModerationEntry]] = None
    hap: Optional[List[ModerationEntry]] = None

class Result(BaseModel):
    generated_text: str
    generated_token_count: Optional[int] = None
    input_token_count: Optional[int] = None
    stop_reason: Optional[str] = None
    moderations: Optional[ModerationsOutput] = None

class GenerateResponse(BaseModel):
    model_id: str
    created_at: datetime
    results: List[Result]

