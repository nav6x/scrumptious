from flask import Blueprint, request, jsonify, g
from config import supabase
from auth_utils import login_required

notifications_bp = Blueprint("notifications", __name__, url_prefix="/api/notifications")

# Expects a `notifications` table — see supabase/schema.sql.
"""
Notification management routes for the Scrumptious API.

Allows authenticated users to retrieve their notifications, obtain
their unread notification count, mark individual notifications as read,
and mark all unread notifications as read.

Notification queries and updates are scoped to the authenticated
user to prevent access to other users' notification records.
"""

@notifications_bp.route("", methods=["GET"])
@login_required
def list_notifications():
    """The caller's newest notifications plus their total unread count
    (the number shown on the bell)."""
    try:
        limit = max(1, min(int(request.args.get("limit", 30)), 100))
    except ValueError:
        limit = 30

    result = (
        supabase.table("notifications")
        .select("id, type, message, is_read, created_at, project_id, task_id, actor_id, projects(name)")
        .eq("user_id", g.user.id)
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    unread = (
        supabase.table("notifications")
        .select("id", count="exact")
        .eq("user_id", g.user.id)
        .eq("is_read", False)
        .execute()
    )
    return jsonify({
        "notifications": result.data or [],
        "unread_count": unread.count or 0,
    }), 200


@notifications_bp.route("/<notification_id>/read", methods=["POST"])
@login_required
def mark_read(notification_id):
    """Mark one of the current user's notifications as read.

    The update is restricted by both notification ID and authenticated
    user ID.

    Args:
        notification_id: ID of the notification to mark as read.

    Returns:
        A JSON confirmation message and HTTP 200.
    """
    # Scoped to user_id so nobody can mark someone else's notifications.
    (
        supabase.table("notifications")
        .update({"is_read": True})
        .eq("id", notification_id)
        .eq("user_id", g.user.id)
        .execute()
    )
    return jsonify({"message": "Marked as read"}), 200


@notifications_bp.route("/read-all", methods=["POST"])
@login_required
def mark_all_read():
    """Mark all unread notifications belonging to the current user as read.

    Returns:
        A JSON confirmation message and HTTP 200.
    """ 
    (
        supabase.table("notifications")
        .update({"is_read": True})
        .eq("user_id", g.user.id)
        .eq("is_read", False)
        .execute()
    )
    return jsonify({"message": "All notifications marked as read"}), 200
