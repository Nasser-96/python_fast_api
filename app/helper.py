from pydantic import BaseModel
from typing import Any

class ReturnResponseType(BaseModel):
    is_successful:bool
    response:Any
    error_msg: str = ''
    success: str = ''

def ReturnResponse(response: Any, is_successful: bool = False, error_msg: str = '', success: str = ''):

    is_successful = False if error_msg else is_successful

    return ReturnResponseType(is_successful=is_successful,
        response=response,
        error_msg=error_msg,
        success=success
        )