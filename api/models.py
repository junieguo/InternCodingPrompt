from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(default="", max_length=1000, description="Task description")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Title",
                "description": "This is description"
            }
        }
    )

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")
    completed: Optional[bool] = Field(None, description="Task completion status")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Updated Task Title",
                "description": "Updated description",
                "completed": True
            }
        }
    )

class TaskResponse(BaseModel):
    id: str = Field(..., description="Unique task identifier")
    title: str = Field(..., description="Task title")
    description: str = Field(..., description="Task description")
    completed: bool = Field(..., description="Whether task is completed")
    created_at: str = Field(..., description="Creation timestamp")
    updated_at: Optional[str] = Field(None, description="Last update timestamp")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Sample Task",
                "description": "This is a sample task",
                "completed": False,
                "created_at": "2024-01-01T00:00:00",
                "updated_at": None
            }
        }
    )