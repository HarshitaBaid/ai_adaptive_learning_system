from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

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
        from_attributes = True


class SubjectWithTopics(BaseModel):
    id: int
    name: str
    topics: List[TopicNested] = []

    class Config:
        from_attributes = True
        
        
class TopicCreate(BaseModel):
    name: str
    subject_id: int
    
    
class QuestionCreate(BaseModel):
    topic_id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_option: str
    difficulty_level: str
    

class QuestionResponse(BaseModel):
    id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    difficulty_level: str

    class Config:
        from_attributes = True
        

class QuizStart(BaseModel):
    student_id: int
    topic_id: int

class QuizAttemptResponse(BaseModel):
    id: int
    student_id: int
    topic_id: int
    score: Optional[int]
    total_questions: Optional[int]
    attempt_date: datetime

    class Config:
        from_attributes = True
        
    
class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=72)   
    

class StudentResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True
        
        
class StudentLogIn(BaseModel):
    email: EmailStr
    password: str  
    
    
class QuizSubmit(BaseModel):
    attempt_id: int
    time_taken: float
    answers: dict[int, str]
    

class ResponseCreate(BaseModel):
    question_id: int
    selected_option: str
    
    
class ResponseResponse(BaseModel):
    question_id: int
    selected_option: str
    correct_option: str
    is_correct: bool

    class Config:
        from_attributes = True
        
        
class ResultResponse(BaseModel):
    score: int
    total: int
    percentage: float
    responses: List[ResponseResponse] 

    class Config:
        from_attributes = True
        
        
class AttemptHistoryResponse(BaseModel):
    id: int
    topic_id: int
    score: int
    total_questions: int
    percentage: float
    attempt_date: datetime
    time_taken: float
    
    class Config:
        from_attributes = True
        
        
class WeakTopicResponse(BaseModel):
    topic_id: int
    average_percentage: float
    status: str

    class Config:
        from_attributes = True
        
        
class QuestionResponse(BaseModel):
    id: int
    topic_id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    difficulty_level: str

    class Config:
        from_attributes = True