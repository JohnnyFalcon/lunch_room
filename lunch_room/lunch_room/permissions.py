
class Permissions:
    def __init__(self, user):
        self.user = user

    def manage_restaurant(self):
        return self.user.groups.filter(name__in=['admin', 'manager']).exists()

    def can_view_restaurant(self):
        return self.manage_restaurant()

    def is_admin(self):
        return self.user.groups.filter(name='admin').exists()

    def manage_lunch_session_list(self):
        result = self.user.groups.filter(name__in=['admin', 'manager', 'customer']).exists()
        return result

    def base_permissions(self):
        """Return base permissions for context"""
        return {
            'can_view_restaurant': self.can_view_restaurant(),
            'is_admin': self.is_admin(),
        }

    def check_view_permissions(self, view_name):
        permission_map = {
            'IndexView': self.manage_lunch_session_list,
            'LunchSessionListView': self.manage_lunch_session_list,
        }

        check_method = permission_map.get(view_name)
        if check_method is None:
            raise ValueError(f'No permission check defined for view: {view_name}')

        return check_method()

