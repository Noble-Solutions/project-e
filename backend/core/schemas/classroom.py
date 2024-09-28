from pydantic import BaseModel, ConfigDict


class ClassroomCreate(BaseModel):
    name: str
    subject: str


class ClassroomRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    subject: str
    amount_of_students: int
