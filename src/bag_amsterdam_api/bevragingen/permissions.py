import logging

from rest_framework.permissions import BasePermission

logger = logging.getLogger(__name__)


class IsUserScope(BasePermission):
    """Permission check, wrapped in a DRF permissions adapter"""

    message = "Required scopes not given in token."
    code = "permissionDenied"

    def __init__(self, needed_scopes):
        self.needed_scopes = frozenset(needed_scopes)

    def has_permission(self, request, view):
        """Check whether the user has all required scopes"""
        # Allow preflight requests
        if request.method == "OPTIONS":
            return True

        # When the access is granted, this skips going into the authorization middleware.
        # This is solely done to avoid incorrect log messages of "access granted",
        # because additional checks may still deny access.
        user_scopes = set(request.get_token_scopes)
        if user_scopes.issuperset(self.needed_scopes):
            return True

        # This calls into 'authorization_django middleware'
        return request.is_authorized_for(*self.needed_scopes)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class HasRequiredHeaders(BasePermission):
    """Permission check to check whether expected headers are present."""

    required_headers = ("X-User", "X-Correlation-ID", "X-Task-Description")
    message = f"The following headers are required: {', '.join(required_headers)}."
    code = "missingHeaders"  # this helps both clients and unittest to see the difference.

    def has_permission(self, request, view):
        if request.method == "OPTIONS":
            return True
        return all(request.headers.get(header) for header in self.required_headers)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
