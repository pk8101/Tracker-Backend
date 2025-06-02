from pydantic import BaseModel, ConfigDict


class IncomeData(BaseModel):
    icon:str
    source:str
    amount:int
    date:str
    model_config= model_config=ConfigDict(
        json_schema_extra={
            "example": {
                "icon": "url-emoji",
                "source": "income source",
                "amount" : "enter amount",
                "date":"dd-mm-yy"
            }
        },
    )
    