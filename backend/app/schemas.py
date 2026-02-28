from pydantic import BaseModel
from typing import List

class SubjectResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
        

class TopicResponse(BaseModel):
    id: int
    name: str
    subject_id: int

    class Config:
        from_attributes = True
        
        
class TopicNested(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class SubjectWithTopics(BaseModel):
    id: int
    name: str
    topics: List[TopicNested] = []

    class Config:
        orm_mode = True
        
        
class TopicCreate(BaseModel):
    name: str
    subject_id: int