from django.contrib.auth.models import User

from lunch_room.models import LunchSession, LunchSessionMembership


class Permissions:
    def __init__(self, user):
        self.user = user

    def main_permissions(self):
        result = self.user.groups.filter(name__in=['admin', 'manager', 'customer']).exists()
        return result

    def manage_restaurant(self):
        return self.user.groups.filter(name__in=['admin', 'manager']).exists()

    def can_view_restaurant(self):
        return self.manage_restaurant()

    def is_admin(self):
        return self.user.groups.filter(name='admin').exists()

    def manage_lunch_session_list(self):
        return self.main_permissions()

    def manage_lunch_session(self, permission_context):
        try:
            lunch_session = LunchSession.objects.get( pk=permission_context.get('lunch_session_id'))
        except (LunchSession.DoesNotExist, ValueError):
            return False
        user = self.user
        return lunch_session.participants.filter(id=user.id).exists()

    def manage_lunch_session_edit(self, permission_context):
        try:
            lunch_session = LunchSession.objects.get( pk=permission_context.get('lunch_session_id'))
        except (LunchSession.DoesNotExist, ValueError):
            return False
        user = self.user
        is_manager = LunchSessionMembership.objects.filter(lunch_session_id=lunch_session.id, user=user, role=LunchSessionMembership.MANAGER).exists()
        return is_manager

    def manage_lunch_session_order(self, permission_context):
        try:
            lunch_session = LunchSession.objects.get( pk=permission_context.get('lunch_session_id'))
        except (LunchSession.DoesNotExist, ValueError):
            return False

        try:
            user = User.objects.get(pk=permission_context.get('user_id'))
        except (User.DoesNotExist, ValueError):
            return False

        is_manager = LunchSessionMembership.objects.filter(lunch_session_id=lunch_session.id, user=self.user,
                                                         role=LunchSessionMembership.MANAGER).exists()

        return (user == self.user and lunch_session.is_active()) or is_manager


    def base_permissions(self):
        """Return base permissions for context"""
        return {
            'access_user': self.user,
            'can_view_restaurant': self.can_view_restaurant(),
            'is_admin': self.is_admin(),
        }

    def check_view_permissions(self, view_name, permission_context=None):
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
            'MealDeleteView': self.manage_restaurant,
            'LunchSessionCreateView': self.manage_lunch_session_list,
            'LunchSessionView': lambda context: self.manage_lunch_session(permission_context),
            'LunchSessionEditView': lambda context: self.manage_lunch_session_edit(permission_context),
            'LunchSessionOrderView': lambda context: self.manage_lunch_session_order(permission_context),
            'LunchSessionSummaryView': lambda context: self.manage_lunch_session_edit(permission_context)
        }

        check_method = permission_map.get(view_name)
        if check_method is None:
            raise ValueError(f'No permission check defined for view: {view_name}')

        return check_method(permission_context) if permission_context else check_method()

