from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class ReportType(str, Enum):
    PHYSICAL = "physical"
    VERBAL = "verbal"
    SOCIAL = "social"
    CYBERBULLYING = "cyberbullying"
    OTHER = "other"

class ReportStatus(str, Enum):
    PENDING = "pending"
    UNDER_REVIEW = "under_review"
    RESOLVED = "resolved"
    ESCALATED = "escalated"

class BullyingReportBase(BaseModel):
    report_type: ReportType
    title: str = Field(..., min_length=5, max_length=255)
    description: str = Field(..., min_length=10, max_length=5000)
    location: Optional[str] = Field(None, max_length=255)
    incident_date: Optional[datetime] = None
    
    bully_name: Optional[str] = Field(None, max_length=255)
    bully_details: Optional[str] = Field(None, max_length=1000)
    
    witnesses: Optional[List[str]] = None
    evidence_urls: Optional[List[str]] = None
    
    severity_level: int = Field(default=1, ge=1, le=5)
    requires_immediate_attention: bool = False

class BullyingReportCreate(BullyingReportBase):
    is_anonymous: bool = False

class BullyingReportUpdate(BaseModel):
    status: ReportStatus
    admin_notes: Optional[str] = Field(None, max_length=2000)
    resolution_notes: Optional[str] = Field(None, max_length=2000)

class BullyingReportResponse(BullyingReportBase):
    id: int
    user_id: Optional[int]
    is_anonymous: bool
    status: ReportStatus
    created_at: datetime
    resolved_at: Optional[datetime]
    admin_notes: Optional[str]
    resolution_notes: Optional[str]
    
    class Config:
        from_attributes = True

class BullyingReport(BullyingReportResponse):
    pass