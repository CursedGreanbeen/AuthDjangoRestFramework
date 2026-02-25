from .models import Permission


def check_permission(user, resource_name, action, obj=None):
    if not user or not user.role:
        return False

    try:
        perm = Permission.objects.get(role=user.role, resource__name=resource_name)
    except Permission.DoesNotExist:
        return False

    action_field = {
        'create': 'can_create',
        'read': 'can_read',
        'update': 'can_update',
        'delete': 'can_delete',
    }
    all_field = {
        'read': 'can_read_all',
        'update': 'can_update_all',
        'delete': 'can_delete_all',
    }

    if action in all_field and getattr(perm, all_field[action], False):
        return True

    if not getattr(perm, action_field[action], False):
        return False

    if obj is None:
        return True

    owner_id = getattr(obj, 'owner_id', None) or getattr(obj, 'user_id', None)
    return owner_id == user.id
