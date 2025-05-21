from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class FunctionCall(BaseModel):
    name: str = Field(..., description="Name of the function to call")
    parameters: Dict[str, Any] = Field(..., description="Parameters of the function to call")

class LLMResponse(BaseModel):
    content: str = Field(..., description="Response to the user's query")
    function_call: Optional[FunctionCall] = Field(None, description="Function call object")
    reasoning: str = Field(..., description="Reason of choosing the response and function")
