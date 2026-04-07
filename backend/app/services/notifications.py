from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.contracts import NotificationItem
from ..core.demo_data import (
    DEMO_ORG_ID,
    append_demo_notification,
    list_demo_notifications,
    mark_demo_notification_read,
)
from ..db.models import Notification
from .cache import build_cache_key, cache_service
from .websocket_hub import notification_hub


async def list_notifications(
    *, org_id: str, recipient_id: str, session: AsyncSession | None
) -> list[NotificationItem]:
    cache_key = build_cache_key("notifications", org_id, recipient_id)
    cached = await cache_service.get_json(cache_key)
    if cached is not None:
        return [NotificationItem.model_validate(item) for item in cached]

    if session is not None:
        result = await session.scalars(
            select(Notification)
            .where(
                Notification.org_id == org_id,
                Notification.recipient_id == recipient_id,
            )
            .order_by(Notification.created_at.desc())
            .limit(20)
        )
        items = [to_contract(item) for item in result.all()]
    else:
        items = [
            NotificationItem.model_validate(item)
            for item in list_demo_notifications(recipient_id)
        ]

    await cache_service.set_json(
        cache_key,
        [item.model_dump(mode="json") for item in items],
    )
    return items


async def mark_as_read(
    *,
    org_id: str,
    recipient_id: str,
    notification_id: str,
    session: AsyncSession | None,
) -> bool:
    if session is not None:
        notification = await session.scalar(
            select(Notification).where(
                Notification.id == notification_id,
                Notification.org_id == org_id,
                Notification.recipient_id == recipient_id,
            )
        )
        if notification is None:
            return False
        notification.is_read = True
        notification.updated_at = datetime.now(UTC)
        await session.commit()
    else:
        if not mark_demo_notification_read(notification_id, recipient_id):
            return False

    await cache_service.delete_prefix(build_cache_key("notifications", org_id, recipient_id))
    return True


async def create_notification(
    *,
    org_id: str,
    recipient_id: str,
    title: str,
    message: str,
    severity: str,
    tags: list[str],
    action_url: str | None,
    session: AsyncSession | None,
) -> NotificationItem:
    if session is not None:
        notification = Notification(
            id=f"notif-{datetime.now(UTC).timestamp()}",
            org_id=org_id,
            recipient_id=recipient_id,
            title=title,
            message=message,
            severity=severity,
            tags=tags,
            action_url=action_url,
            is_read=False,
        )
        session.add(notification)
        await session.commit()
        await session.refresh(notification)
        item = to_contract(notification)
    else:
        item = NotificationItem.model_validate(
            append_demo_notification(
                recipient_id=recipient_id,
                title=title,
                message=message,
                severity=severity,
                tags=tags,
                action_url=action_url,
            )
        )

    target_org = org_id or DEMO_ORG_ID
    await cache_service.delete_prefix(build_cache_key("notifications", target_org, recipient_id))
    await notification_hub.push_to_user(
        recipient_id,
        {
            "type": "notification.created",
            "payload": item.model_dump(mode="json"),
        },
    )
    return item


def to_contract(notification: Notification) -> NotificationItem:
    return NotificationItem(
        notification_id=notification.id,
        title=notification.title,
        message=notification.message,
        severity=notification.severity,
        tags=notification.tags or [],
        action_url=notification.action_url,
        created_at=notification.created_at,
        is_read=notification.is_read,
    )
