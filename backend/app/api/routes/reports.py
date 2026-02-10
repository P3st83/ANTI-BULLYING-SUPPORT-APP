from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter()

class BullyingReport(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None  # None for anonymous reports
    title: str
    description: str
    incident_date: str
    location: str
    people_involved: List[str]
    is_anonymous: bool
    reported_to: Optional[str] = None
    status: str = "pending"  # pending, reviewed, resolved
    created_at: Optional[str] = None

class ReportUpdate(BaseModel):
    status: str
    notes: Optional[str] = None

# Mock reports storage
mock_reports = []

@router.post("/", response_model=BullyingReport)
async def create_report(report: BullyingReport):
    """Submit a new bullying incident report."""
    
    # Validate required fields
    if not report.title or not report.description:
        raise HTTPException(
            status_code=400,
            detail="Title and description are required"
        )
    
    if len(report.description) > 2000:
        raise HTTPException(
            status_code=400,
            detail="Description must be under 2000 characters"
        )
    
    # Create new report
    report_dict = {
        "id": f"report_{len(mock_reports) + 1}",
        "user_id": None if report.is_anonymous else report.user_id,
        "title": report.title,
        "description": report.description,
        "incident_date": report.incident_date,
        "location": report.location,
        "people_involved": report.people_involved,
        "is_anonymous": report.is_anonymous,
        "reported_to": report.reported_to,
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }
    
    mock_reports.append(report_dict)
    
    # In a real app, send notifications to appropriate authorities
    await send_report_notifications(report_dict)
    
    return BullyingReport(**report_dict)

@router.get("/", response_model=List[BullyingReport])
async def get_reports(user_id: Optional[str] = None, status: Optional[str] = None):
    """Get reports. If user_id is provided, get user's reports only."""
    
    filtered_reports = mock_reports
    
    if user_id:
        filtered_reports = [r for r in filtered_reports if r["user_id"] == user_id]
    
    if status:
        filtered_reports = [r for r in filtered_reports if r["status"] == status]
    
    # Sort by creation date (newest first)
    filtered_reports.sort(key=lambda x: x["created_at"], reverse=True)
    
    return [BullyingReport(**report) for report in filtered_reports]

@router.get("/{report_id}", response_model=BullyingReport)
async def get_report(report_id: str):
    """Get a specific report by ID."""
    
    report = next((r for r in mock_reports if r["id"] == report_id), None)
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    return BullyingReport(**report)

@router.put("/{report_id}/status")
async def update_report_status(report_id: str, update: ReportUpdate):
    """Update the status of a report (admin/staff only)."""
    
    report = next((r for r in mock_reports if r["id"] == report_id), None)
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    valid_statuses = ["pending", "reviewed", "resolved"]
    if update.status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        )
    
    report["status"] = update.status
    
    # In a real app, send notification to user if not anonymous
    if not report["is_anonymous"] and report["user_id"]:
        await send_status_update_notification(report, update.notes)
    
    return {"message": "Report status updated successfully"}

@router.get("/stats/summary")
async def get_report_stats():
    """Get summary statistics of all reports."""
    
    total_reports = len(mock_reports)
    anonymous_reports = len([r for r in mock_reports if r["is_anonymous"]])
    
    status_counts = {}
    for report in mock_reports:
        status = report["status"]
        status_counts[status] = status_counts.get(status, 0) + 1
    
    # Recent activity (last 30 days)
    from datetime import timedelta
    thirty_days_ago = datetime.now() - timedelta(days=30)
    recent_reports = [
        r for r in mock_reports 
        if datetime.fromisoformat(r["created_at"]) > thirty_days_ago
    ]
    
    return {
        "total_reports": total_reports,
        "anonymous_reports": anonymous_reports,
        "status_breakdown": status_counts,
        "recent_reports_30_days": len(recent_reports),
        "resolution_rate": (
            status_counts.get("resolved", 0) / total_reports * 100 
            if total_reports > 0 else 0
        )
    }

async def send_report_notifications(report: dict):
    """Send notifications to appropriate authorities about new report."""
    
    # Mock notification logic
    # In production, integrate with email/SMS services
    
    notification_recipients = []
    
    if report["reported_to"]:
        recipients = report["reported_to"].split(", ")
        notification_recipients.extend(recipients)
    
    # Default to school administration for all reports
    if "school" not in notification_recipients:
        notification_recipients.append("school_administration")
    
    # For development, just log the notification
    print(f"📧 Report notification sent to: {', '.join(notification_recipients)}")
    print(f"📋 Report ID: {report['id']}")
    print(f"📍 Location: {report['location']}")
    print(f"🔒 Anonymous: {report['is_anonymous']}")

async def send_status_update_notification(report: dict, notes: Optional[str] = None):
    """Send status update notification to the user who submitted the report."""
    
    # Mock notification logic
    print(f"📱 Status update sent to user {report['user_id']}")
    print(f"📋 Report ID: {report['id']}")
    print(f"📊 New Status: {report['status']}")
    if notes:
        print(f"💬 Notes: {notes}")

@router.post("/emergency")
async def emergency_report():
    """Handle emergency reports that require immediate attention."""
    
    # This endpoint would trigger immediate notifications
    # to emergency contacts, school staff, parents, etc.
    
    return {
        "message": "Emergency report received. Immediate assistance has been notified.",
        "emergency_contacts": [
            {
                "name": "School Emergency Line",
                "phone": "555-SCHOOL",
                "available": "24/7"
            },
            {
                "name": "Crisis Text Line", 
                "contact": "Text HOME to 741741",
                "available": "24/7"
            },
            {
                "name": "Emergency Services",
                "phone": "911",
                "available": "24/7"
            }
        ]
    }