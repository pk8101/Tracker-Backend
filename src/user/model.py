from pydantic import ConfigDict, Field, BaseModel


class UserDetails(BaseModel):
    username: str=Field(min_length=10)
    email: str 
    password: str
    model_config=ConfigDict(
    json_schema_extra={
    "example": {
        "email": "pradeep@gmail.com",
        "password": "Pradeep@123",
        "username" : "pradeepkanda"
    }
    },
    from_attributes=True
    )
    
    
class UserDetailsUpdate(BaseModel):
    username: str=Field(min_length=10)
    password:str
    model_config=ConfigDict(
        json_schema_extra={
            "example": {
            "password": "Pradeep®123",
            "username": "pradeep."
        }
        } 
    )   


class UserLogin(BaseModel):
    email:str 
    password:str
    