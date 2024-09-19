# from typing import Any

# from pydantic import BaseModel, model_validator
# from pydantic_core.core_schema import ValidationInfo


# class ContextCheckingBaseModel(BaseModel):
#     @model_validator(mode="before")
#     @classmethod
#     def check_context(cls, data: Any, info: ValidationInfo) -> Any:
#         context = info.context        
#         return dict(zip([key[0] for key in context.description], data)) if context else data
