from django.contrib.auth.models import User
from django.db import models


class Restaurant(models.Model):
    name = models.CharField(verbose_name='Nazwa', max_length=255)
    address = models.CharField(verbose_name='Adres', max_length=255)
    phone = models.CharField(verbose_name='Telefon kontaktowy', max_length=255)


class Meal(models.Model):
    name = models.CharField(verbose_name='Nazwa', max_length=255)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='meals')


class OrderGroup(models.Model):
    name = models.CharField(verbose_name='Nazwa', max_length=150, unique=True)
    users = models.ManyToManyField(User, verbose_name='users', blank=True, related_name='order_groups')


class LunchSessionMembership(models.Model):
    MEMBER = 'member'
    MANAGER = 'manager'

    ROLE_CHOICES = (
        (MEMBER, 'Uczestnik'),
        (MANAGER, 'Manager'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lunch_session = models.ForeignKey('LunchSession', on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=MEMBER)

    class Meta:
        unique_together = ['user', 'lunch_session']


class LunchSession(models.Model):
    ACTIVE = 'active'
    CLOSED = 'closed'

    STATUSES = (
        (ACTIVE, 'Aktywna'),
        (CLOSED, 'Zamknięta'),
    )
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_lunch_sessions')
    name = models.CharField(verbose_name='Nazwa', max_length=255)
    participants = models.ManyToManyField(
        User,
        through='LunchSessionMembership',
        related_name='participated_lunch_sessions'
    )
    status = models.CharField(max_length=255, choices=STATUSES, default=ACTIVE)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, related_name='lunch_sessions')
    delivery_time = models.DateTimeField(null=True)
    session_end_time = models.DateTimeField(null=True)

    def get_members(self):
        return self.participants.filter(
            lunchsessionmembership__role=LunchSessionMembership.MEMBER
        )

    def get_managers(self):
        return self.participants.filter(
            lunchsessionmembership__role=LunchSessionMembership.MANAGER
        )

    def add_member(self, user):
        LunchSessionMembership.objects.get_or_create(
            user=user,
            lunch_session=self,
            defaults={'role': LunchSessionMembership.MEMBER}
        )

    def add_manager(self, user):
        LunchSessionMembership.objects.get_or_create(
            user=user,
            lunch_session=self,
            defaults={'role': LunchSessionMembership.MANAGER}
        )

    def all_participants(self):
        return self.participants.all()

    def all_participants_initials(self):
        initials = []
        for user in self.all_participants():
            name = user.get_full_name() or user.username
            initials.append(''.join(word[0].upper() for word in name.split()))
        return initials

    def get_user_order(self, user):
        return self.session_orders.filter(user=user)

    def get_user_order_total(self, user):
        return self.session_orders.filter(user=user).aggregate(total=models.Sum('total_price'))['total'] or 0

    def get_session_total(self):
        return self.session_orders.aggregate(total=models.Sum('total_price'))['total'] or 0

    def get_all_orders_grouped_by_user(self):
        return self.session_orders.values('user__username').annotate(total=models.Sum('total_price')).order_by('user__username')


    def is_active(self):
        return self.status == self.ACTIVE


class LunchSessionOrderItem(models.Model):
    lunch_session = models.ForeignKey(LunchSession, on_delete=models.CASCADE, related_name='session_orders')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lunch_orders')
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=20, decimal_places=2, null=True)

    def save(self, *args, **kwargs):
        self.total_price = self.meal.price * self.quantity
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ['lunch_session', 'user', 'meal']