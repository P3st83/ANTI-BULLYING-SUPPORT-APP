from sqlalchemy import Column, String, Integer, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class BullyingReport(Base, TimestampMixin):
    __tablename__ = "bullying_reports"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)  # Nullable for anonymous reports
    
    is_anonymous = Column(Boolean, default=False)
    report_type = Column(String(20), nullable=False)
    status = Column(String(20), default="pending")
    
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String(255), nullable=True)
    incident_date = Column(DateTime(timezone=True), nullable=True)
    
    bully_name = Column(String(255), nullable=True)
    bully_details = Column(Text, nullable=True)
    
    witnesses = Column(Text, nullable=True)  # JSON array
    evidence_urls = Column(Text, nullable=True)  # JSON array of file URLs
    
    severity_level = Column(Integer, default=1)  # 1-5 scale
    requires_immediate_attention = Column(Boolean, default=False)
    
    admin_notes = Column(Text, nullable=True)
    resolution_notes = Column(Text, nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    
    user = relationship("User", back_populates="reports")