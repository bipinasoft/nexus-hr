from fastapi import APIRouter, Depends, HTTPException, Query, WebSocket, WebSocketDisconnect, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.contracts import NotificationAck, NotificationItem
from ..db.session import get_db_session
from ..platform import (
    Permission,
    Principal,
    get_current_principal,
    require_permissions,
    resolve_principal_from_token,
)
from ..services.notifications import list_notifications, mark_as_read
from ..services.websocket_hub import notification_hub

router = APIRouter(prefix="/v1/notifications", tags=["notifications"])


@router.get("/me", response_model=list[NotificationItem])
async def read_my_notifications(
    principal: Principal = Depends(require_permissions(Permission.NOTIFICATION_READ)),
    session: AsyncSession | None = Depends(get_db_session),
) -> list[NotificationItem]:
    return await list_notifications(
        org_id=principal.org_id,
        recipient_id=principal.user_id,
        session=session,
    )


@router.post("/{notification_id}/read", response_model=NotificationAck)
async def acknowledge_notification(
    notification_id: str,
    principal: Principal = Depends(require_permissions(Permission.NOTIFICATION_READ)),
    session: AsyncSession | None = Depends(get_db_session),
) -> NotificationAck:
    updated = await mark_as_read(
        org_id=principal.org_id,
        recipient_id=principal.user_id,
        notification_id=notification_id,
        session=session,
    )
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found.",
        )
    return NotificationAck(notification_id=notification_id, status="read")


@router.websocket("/ws/notifications")
async def notifications_socket(
    websocket: WebSocket,
    token: str = Query(...),
) -> None:
    principal = await resolve_principal_from_token(token)
    await notification_hub.connect(principal.user_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        notification_hub.disconnect(principal.user_id, websocket)
