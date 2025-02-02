from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

# Create your models here.
from crm.querysets.project_service import ProjectServiceQuerySet

ROLE = {
    ('Manager', 'Manager'),
}


class User(AbstractUser):
    name = models.CharField(max_length=120)
    password = models.CharField(max_length=120)
    role = models.CharField(max_length=120, choices=ROLE)
    objects = UserManager()

    def __str__(self):
        return self.username + ' ' + self.role


FROM = {
    ('Instagram', 'Instagram'),
    ('Facebook', 'Facebook'),
}


class ClientsStatus(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Clients(models.Model):
    creat_date = models.DateTimeField(auto_now_add=True)
    birthday = models.DateField(null=True, blank=True)
    full_name = models.CharField(max_length=120)
    phone = models.IntegerField(null=True)
    address = models.CharField(max_length=120, null=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey(ClientsStatus, null=True, blank=True, on_delete=models.CASCADE)
    form = models.CharField(max_length=120, choices=FROM, null=True)

    def __str__(self):
        return self.full_name


STATUS_PAY = {
    ('Оплачено', 'Оплачено'),
    ('Аванс', 'Аванс'),
    ('Ожидание', 'Ожидание'),
}


class Orders(models.Model):
    order_number = models.IntegerField(null=True)
    title = models.CharField(max_length=120)
    service = models.ManyToManyField('Service', through="ProjectService")
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    status = models.CharField(max_length=120, choices=STATUS_PAY, default="Ожидание")
    is_archive = models.BooleanField(default=False, null=True, blank=True)
    numbers = models.PositiveIntegerField(null=True, blank=True)
    user = models.ManyToManyField('User')

    def __str__(self):
        return f"Clientni ismi: {self.client}, Buyurtma: {self.title}"


class Department(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=120)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey('Service', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ProjectService(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ManyToManyField('User', null=True, blank=True, )
    parcent = models.FloatField(default=0, null=True, blank=True)
    max_parcent = models.IntegerField(default=0, null=True, blank=True)

    objects = ProjectServiceQuerySet.as_manager()

    def total_prince(self):
        return int(self.order.numbers * (self.parcent / 100))


class OrderField(models.Model):
    title = models.CharField(max_length=255)
    field = models.FileField(upload_to='uploads/', blank=False)
    order_filed = models.ForeignKey(Orders, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title
