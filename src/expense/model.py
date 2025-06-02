from pydantic import BaseModel, ConfigDict


class ExpenseData(BaseModel):
    icon:str
    category:str
    amount:int
    date:str
    model_config= model_config=ConfigDict(
        json_schema_extra={
            "example": {
                "icon": "url-emoji",
                "category": "expense category",
                "amount" : "enter amount",
                "date":"dd-mm-yy"
            }
        },
    )
    