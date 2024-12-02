
class Permissions:
    def __init__(self, user):
        self.user = user

    def main_permissions(self):
        result = self.user.groups.filter(name__in=['manager', 'customer']).exists()
        return result

    def manage_restaurant(self):
        return self.user.groups.filter(name__in=['admin', 'manager']).exists()

    def can_view_restaurant(self):
        return self.manage_restaurant()

    def is_admin(self):
        return self.user.groups.filter(name='admin').exists()

    def manage_lunch_session_list(self):
        return self.main_permissions()

    def base_permissions(self):
        """Return base permissions for context"""
        return {
            'can_view_restaurant': self.can_view_restaurant(),
            'is_admin': self.is_admin(),
        }

    def check_view_permissions(self, view_name):
        permission_map = {
            'IndexView': self.main_permissions,
            'LunchSessionListView': self.manage_lunch_session_list,
            'UserProfileView': self.main_permissions,
            'RestaurantListView': self.manage_restaurant,
            'RestaurantEditView': self.manage_restaurant,
            'RestaurantDeleteView': self.manage_restaurant,
            'RestaurantCreateView': self.manage_restaurant,
            'MealCreateView': self.manage_restaurant,
            'MealEditView': self.manage_restaurant,
            'MealDeleteView': self.manage_restaurant
        }

        check_method = permission_map.get(view_name)
        if check_method is None:
            raise ValueError(f'No permission check defined for view: {view_name}')

        return check_method()

