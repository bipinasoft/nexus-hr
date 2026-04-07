from __future__ import annotations

from datetime import UTC, date, datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import JSON, Boolean, Date, DateTime, Float, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def utcnow() -> datetime:
    return datetime.now(UTC)


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )


class Organization(TimestampMixin, Base):
    __tablename__ = "organizations"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(160))
    slug: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    primary_domain: Mapped[str] = mapped_column(String(160), unique=True)
    region_code: Mapped[str] = mapped_column(String(16), default="IN")
    status: Mapped[str] = mapped_column(String(32), default="active")


class Department(TimestampMixin, Base):
    __tablename__ = "departments"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    org_id: Mapped[str] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), index=True
    )
    name: Mapped[str] = mapped_column(String(120))
    code: Mapped[str] = mapped_column(String(24))

    __table_args__ = (
        UniqueConstraint("org_id", "code", name="uq_departments_org_code"),
    )


class Position(TimestampMixin, Base):
    __tablename__ = "positions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    org_id: Mapped[str] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), index=True
    )
    title: Mapped[str] = mapped_column(String(120))
    level: Mapped[str] = mapped_column(String(32))
    description: Mapped[str | None] = mapped_column(Text(), nullable=True)


class Employee(TimestampMixin, Base):
    __tablename__ = "employees"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    org_id: Mapped[str] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), index=True
    )
    employee_code: Mapped[str] = mapped_column(String(32))
    first_name: Mapped[str] = mapped_column(String(80))
    last_name: Mapped[str] = mapped_column(String(80))
    work_email: Mapped[str] = mapped_column(String(160), index=True)
    role: Mapped[str] = mapped_column(String(32))
    employment_status: Mapped[str] = mapped_column(String(32), default="active")
    password_hash: Mapped[str] = mapped_column(Text())
    department_id: Mapped[str] = mapped_column(
        ForeignKey("departments.id", ondelete="RESTRICT"), index=True
    )
    position_id: Mapped[str] = mapped_column(
        ForeignKey("positions.id", ondelete="RESTRICT"), index=True
    )
    team_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    manager_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    hire_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    timezone: Mapped[str] = mapped_column(String(64), default="Asia/Calcutta")

    __table_args__ = (
        UniqueConstraint("org_id", "employee_code", name="uq_employees_org_code"),
        UniqueConstraint("org_id", "work_email", name="uq_employees_org_email"),
    )


class AttendanceRecord(TimestampMixin, Base):
    __tablename__ = "attendance_records"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    org_id: Mapped[str] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), index=True
    )
    employee_id: Mapped[str] = mapped_column(
        ForeignKey("employees.id", ondelete="CASCADE"), index=True
    )
    work_date: Mapped[date] = mapped_column(Date, index=True)
    status: Mapped[str] = mapped_column(String(24), index=True)
    check_in_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    check_out_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    total_hours: Mapped[float | None] = mapped_column(Float, nullable=True)
    geofence_passed: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    location_label: Mapped[str | None] = mapped_column(String(160), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text(), nullable=True)

    __table_args__ = (
        UniqueConstraint(
            "org_id", "employee_id", "work_date", name="uq_attendance_org_employee_day"
        ),
        Index("ix_attendance_org_employee_date", "org_id", "employee_id", "work_date"),
    )


class LeaveRequest(TimestampMixin, Base):
    __tablename__ = "leave_requests"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    org_id: Mapped[str] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), index=True
    )
    employee_id: Mapped[str] = mapped_column(
        ForeignKey("employees.id", ondelete="CASCADE"), index=True
    )
    approver_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    leave_type: Mapped[str] = mapped_column(String(64))
    start_date: Mapped[date] = mapped_column(Date, index=True)
    end_date: Mapped[date] = mapped_column(Date, index=True)
    status: Mapped[str] = mapped_column(String(24), index=True)
    reason: Mapped[str] = mapped_column(Text())

    __table_args__ = (
        Index("ix_leave_requests_org_employee", "org_id", "employee_id"),
    )


class LeaveBalance(TimestampMixin, Base):
    __tablename__ = "leave_balances"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    org_id: Mapped[str] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), index=True
    )
    employee_id: Mapped[str] = mapped_column(
        ForeignKey("employees.id", ondelete="CASCADE"), index=True
    )
    leave_type: Mapped[str] = mapped_column(String(64))
    allocated_days: Mapped[float] = mapped_column(Float)
    used_days: Mapped[float] = mapped_column(Float, default=0.0)
    pending_days: Mapped[float] = mapped_column(Float, default=0.0)


class Holiday(TimestampMixin, Base):
    __tablename__ = "holidays"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    org_id: Mapped[str] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), index=True
    )
    holiday_date: Mapped[date] = mapped_column(Date, index=True)
    name: Mapped[str] = mapped_column(String(160))
    kind: Mapped[str] = mapped_column(String(32), default="company")

    __table_args__ = (
        UniqueConstraint("org_id", "holiday_date", name="uq_holidays_org_day"),
    )


class Notification(TimestampMixin, Base):
    __tablename__ = "notifications"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    org_id: Mapped[str] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), index=True
    )
    recipient_id: Mapped[str] = mapped_column(
        ForeignKey("employees.id", ondelete="CASCADE"), index=True
    )
    title: Mapped[str] = mapped_column(String(160))
    message: Mapped[str] = mapped_column(Text())
    severity: Mapped[str] = mapped_column(String(24), default="low")
    tags: Mapped[list[str]] = mapped_column(JSON, default=list)
    action_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)

    __table_args__ = (
        Index("ix_notifications_org_recipient", "org_id", "recipient_id"),
    )


class KnowledgeDocument(TimestampMixin, Base):
    __tablename__ = "knowledge_documents"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    org_id: Mapped[str] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), index=True
    )
    title: Mapped[str] = mapped_column(String(160))
    source: Mapped[str] = mapped_column(String(255))
    tags: Mapped[list[str]] = mapped_column(JSON, default=list)
    status: Mapped[str] = mapped_column(String(24), default="indexed")

    __table_args__ = (
        UniqueConstraint("org_id", "source", name="uq_knowledge_documents_org_source"),
    )


class KnowledgeChunk(TimestampMixin, Base):
    __tablename__ = "knowledge_chunks"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    org_id: Mapped[str] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), index=True
    )
    document_id: Mapped[str] = mapped_column(
        ForeignKey("knowledge_documents.id", ondelete="CASCADE"), index=True
    )
    chunk_index: Mapped[int] = mapped_column(index=True)
    content: Mapped[str] = mapped_column(Text())
    metadata_json: Mapped[dict[str, str]] = mapped_column(JSON, default=dict)
    embedding: Mapped[list[float]] = mapped_column(Vector(256))

    __table_args__ = (
        Index("ix_knowledge_chunks_org_document", "org_id", "document_id", "chunk_index"),
    )
