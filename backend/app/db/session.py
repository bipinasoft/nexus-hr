from __future__ import annotations

import logging
from collections.abc import AsyncGenerator
from datetime import UTC, datetime, time

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from nexus_shared.config import get_settings

from ..core.demo_data import (
    DEMO_DEPARTMENTS,
    DEMO_DOMAIN,
    DEMO_EMPLOYEES,
    DEMO_LEAVE_BALANCES,
    DEMO_ORG_ID,
    DEMO_POLICY_DOCUMENTS,
    DEMO_POSITIONS,
    DEMO_TENANT_SLUG,
    demo_attendance_records,
    demo_holidays,
    demo_leave_requests,
    initial_notifications,
)
from ..core.passwords import hash_password
from .models import (
    AttendanceRecord,
    Base,
    Department,
    Employee,
    Holiday,
    KnowledgeDocument,
    LeaveBalance,
    LeaveRequest,
    Notification,
    Organization,
    Position,
)

logger = logging.getLogger("nexushr.database")


class DatabaseManager:
    def __init__(self) -> None:
        self.engine: AsyncEngine | None = None
        self.session_factory: async_sessionmaker[AsyncSession] | None = None
        self.available = False
        self.startup_error: str | None = None

    async def initialize(self) -> None:
        settings = get_settings()
        if not settings.bootstrap_database:
            self.available = False
            self.startup_error = "Database bootstrap disabled by configuration."
            return

        try:
            self.engine = create_async_engine(
                settings.database_url,
                echo=settings.database_echo,
                pool_pre_ping=True,
            )
            self.session_factory = async_sessionmaker(
                self.engine,
                expire_on_commit=False,
            )

            async with self.engine.begin() as connection:
                if settings.database_url.startswith("postgresql"):
                    await connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
                await connection.run_sync(Base.metadata.create_all)

            if settings.seed_demo_data and self.session_factory is not None:
                async with self.session_factory() as session:
                    await seed_demo_dataset(session)

            self.available = True
            self.startup_error = None
        except Exception as exc:
            logger.warning("Database bootstrap unavailable: %s", exc)
            self.available = False
            self.startup_error = str(exc)
            if self.engine is not None:
                await self.engine.dispose()
            self.engine = None
            self.session_factory = None

    async def dispose(self) -> None:
        if self.engine is not None:
            await self.engine.dispose()
        self.engine = None
        self.session_factory = None
        self.available = False

    async def get_session(self) -> AsyncGenerator[AsyncSession | None, None]:
        if self.session_factory is None:
            yield None
            return

        async with self.session_factory() as session:
            yield session


database_manager = DatabaseManager()


async def get_db_session() -> AsyncGenerator[AsyncSession | None, None]:
    async for session in database_manager.get_session():
        yield session


async def seed_demo_dataset(session: AsyncSession) -> None:
    existing_org = await session.scalar(
        select(Organization).where(Organization.id == DEMO_ORG_ID)
    )
    if existing_org is not None:
        return

    organization = Organization(
        id=DEMO_ORG_ID,
        name="NexusHR Demo Workspace",
        slug=DEMO_TENANT_SLUG,
        primary_domain=DEMO_DOMAIN,
        region_code="IN",
        status="active",
    )
    session.add(organization)

    for department in DEMO_DEPARTMENTS:
        session.add(
            Department(
                id=department["id"],
                org_id=DEMO_ORG_ID,
                name=department["name"],
                code=department["code"],
            )
        )

    for position in DEMO_POSITIONS:
        session.add(
            Position(
                id=position["id"],
                org_id=DEMO_ORG_ID,
                title=position["title"],
                level=position["level"],
                description=position.get("description"),
            )
        )

    for employee in DEMO_EMPLOYEES:
        session.add(
            Employee(
                id=employee.employee_id,
                user_id=employee.user_id,
                org_id=DEMO_ORG_ID,
                employee_code=employee.employee_code,
                first_name=employee.first_name,
                last_name=employee.last_name,
                work_email=employee.work_email,
                role=employee.role.value,
                employment_status=employee.employment_status,
                password_hash=hash_password(get_settings().demo_password),
                department_id=employee.department_id,
                position_id=employee.position_id,
                team_id=employee.team_id,
                manager_id=employee.manager_id,
                hire_date=datetime.combine(employee.hire_date, time(9, 0), tzinfo=UTC),
                timezone="Asia/Calcutta",
            )
        )

    month_start = datetime.now(UTC).date().replace(day=1)

    for holiday in demo_holidays(month_start):
        session.add(
            Holiday(
                id=holiday["id"],
                org_id=DEMO_ORG_ID,
                holiday_date=holiday["holiday_date"],
                name=holiday["name"],
                kind=holiday["kind"],
            )
        )

    for item in DEMO_LEAVE_BALANCES:
        session.add(
            LeaveBalance(
                id=f"lb-{item['employee_id']}-{item['leave_type'].lower().replace(' ', '-')}",
                org_id=DEMO_ORG_ID,
                employee_id=item["employee_id"],
                leave_type=item["leave_type"],
                allocated_days=item["allocated_days"],
                used_days=item["used_days"],
                pending_days=item["pending_days"],
            )
        )

    for leave_request in demo_leave_requests("emp-maya-rao", month_start):
        session.add(
            LeaveRequest(
                id=leave_request["id"],
                org_id=DEMO_ORG_ID,
                employee_id=leave_request["employee_id"],
                approver_id=leave_request["approver_id"],
                leave_type=leave_request["leave_type"],
                start_date=leave_request["start_date"],
                end_date=leave_request["end_date"],
                status=leave_request["status"],
                reason=leave_request["reason"],
            )
        )

    for attendance in demo_attendance_records("emp-maya-rao", month_start):
        session.add(
            AttendanceRecord(
                id=attendance["id"],
                org_id=DEMO_ORG_ID,
                employee_id=attendance["employee_id"],
                work_date=attendance["work_date"],
                status=attendance["status"],
                check_in_at=attendance["check_in_at"],
                check_out_at=attendance["check_out_at"],
                total_hours=attendance["total_hours"],
                geofence_passed=attendance["geofence_passed"],
                location_label=attendance["location_label"],
                notes=attendance["notes"],
            )
        )

    for notification in initial_notifications():
        session.add(
            Notification(
                id=notification["notification_id"],
                org_id=DEMO_ORG_ID,
                recipient_id=notification["recipient_id"],
                title=notification["title"],
                message=notification["message"],
                severity=notification["severity"],
                tags=notification["tags"],
                action_url=notification["action_url"],
                is_read=notification["is_read"],
                created_at=notification["created_at"],
            )
        )

    for document in DEMO_POLICY_DOCUMENTS:
        session.add(
            KnowledgeDocument(
                id=f"doc-{document['source'].split('/')[-1].replace(':', '-')}",
                org_id=DEMO_ORG_ID,
                title=document["title"],
                source=document["source"],
                tags=document["tags"],
                status="seeded",
            )
        )

    await session.commit()
