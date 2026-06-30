from enum import StrEnum


class RoleSlug(StrEnum):
    OWNER = "owner"
    ADMIN = "admin"
    MANAGER = "manager"
    DEVELOPER = "developer"
    MEMBER = "member"
    BILLING = "billing"


class Permission(StrEnum):
    ORG_READ = "org:read"
    ORG_WRITE = "org:write"
    ORG_DELETE = "org:delete"
    TEAM_READ = "team:read"
    TEAM_WRITE = "team:write"
    TEAM_DELETE = "team:delete"
    INVITE_CREATE = "invite:create"
    INVITE_MANAGE = "invite:manage"
    MEMBERS_MANAGE = "members:manage"
    BILLING_MANAGE = "billing:manage"
    API_KEYS_MANAGE = "api_keys:manage"
    AUDIT_READ = "audit:read"


ROLE_PERMISSIONS: dict[RoleSlug, set[Permission]] = {
    RoleSlug.OWNER: set(Permission),
    RoleSlug.ADMIN: {
        Permission.ORG_READ,
        Permission.ORG_WRITE,
        Permission.TEAM_READ,
        Permission.TEAM_WRITE,
        Permission.TEAM_DELETE,
        Permission.INVITE_CREATE,
        Permission.INVITE_MANAGE,
        Permission.MEMBERS_MANAGE,
        Permission.API_KEYS_MANAGE,
        Permission.AUDIT_READ,
    },
    RoleSlug.MANAGER: {
        Permission.ORG_READ,
        Permission.TEAM_READ,
        Permission.TEAM_WRITE,
        Permission.INVITE_CREATE,
        Permission.MEMBERS_MANAGE,
    },
    RoleSlug.DEVELOPER: {
        Permission.ORG_READ,
        Permission.TEAM_READ,
        Permission.API_KEYS_MANAGE,
    },
    RoleSlug.MEMBER: {Permission.ORG_READ, Permission.TEAM_READ},
    RoleSlug.BILLING: {Permission.ORG_READ, Permission.BILLING_MANAGE},
}


def role_has_permission(role: str, permission: Permission) -> bool:
    try:
        return permission in ROLE_PERMISSIONS[RoleSlug(role)]
    except ValueError:
        return False