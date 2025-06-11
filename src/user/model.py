from pydantic import ConfigDict, Field, BaseModel


class UserDetails(BaseModel):
    username: str=Field(min_length=10)
    email: str 
    password: str
    profileImageUrl:str
    model_config=ConfigDict(
    json_schema_extra={
    "example": {
        "email": "pradeep@gmail.com",
        "password": "Pradeep@123",
        "username" : "pradeepkanda",
        "profileImageUrl":"https://img-url.com"
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
            "password": "Pradeep@123",
            "username": "pradeepk20"
        }
        } 
    )   


class UserLogin(BaseModel):
    email:str 
    password:str
    model_config=ConfigDict(
        json_schema_extra={
            "example": {
            "password": "Pradeep@123",
            "email": "pradeep@gmail.com"
        }
        } 
    ) 
    
class VerifyOTP(BaseModel):
    email:str 
    otp:str
    model_config=ConfigDict(
        json_schema_extra={
            "example": {
            "otp": "123456"
        }
        } 
    )
    