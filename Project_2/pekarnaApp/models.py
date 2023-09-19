import datetime
import decimal

from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    """
    Create profile for a new user and give him role "user".
    :param sender: Class User - signal is generated on save of instance of class User.
    :param instance: Instance of class User that was saved.
    :param created: says if user was created.
    :param kwargs:
    :return:
    """
    if created:
        instance.groups.add(Group.objects.get_or_create(name='Uživatel')[0])


# Create your models here.
class Allergen(models.Model):
    title = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return '{}'.format(self.title)


class Resource(models.Model):
    title = models.CharField(verbose_name='název', max_length=64)
    price = models.DecimalField(verbose_name='cena/kg', max_digits=8, decimal_places=2, default=0)
    stock = models.DecimalField(verbose_name='na skladě', max_digits=8, decimal_places=2, default=0)
    allergens = models.ManyToManyField(Allergen, verbose_name='alergeny', blank=True)

    def __str__(self):
        return '{}'.format(self.title)


class ProductCategory(models.Model):
    title = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        verbose_name_plural = 'Product Categories'


class Product(models.Model):
    title = models.CharField(max_length=64)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    weight = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.title)


class ProductResource(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='resources')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return '{} - {} - {}g'.format(self.product, self.resource, self.weight)


class State(models.Model):
    """
    Possible states of orders.
    """
    title = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return '{}'.format(self.title)


class Car(models.Model):
    driver = models.ForeignKey(User, verbose_name='řidič', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='název', max_length=64, unique=True)
    spz = models.CharField(max_length=8, unique=True)
    capacity = models.IntegerField(verbose_name='kapacita', default=5)

    def __str__(self):
        return '{} ({}) - {}'.format(self.title, self.spz, self.capacity)

    def driver_name(self):
        return self.driver.get_full_name() + self.driver.username


class Route(models.Model):
    date = models.DateTimeField(null=True, blank=True)
    driver = models.ForeignKey(User, on_delete=models.CASCADE)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    address = models.TextField(verbose_name='Doručovací adresa', null=True, blank=True)
    notes = models.TextField(verbose_name='Poznámky', null=True, blank=True)
    state = models.ForeignKey(State, verbose_name='Stav', on_delete=models.SET_NULL, null=True, default=1)
    created = models.DateTimeField(auto_now_add=True)
    deliver_date = models.DateField(verbose_name='Doručit dne', default=datetime.date.today)
    delivered = models.DateTimeField(null=True, blank=True)
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    route_index = models.IntegerField(default=0)

    class Meta:
        permissions = (
            ("view_cookplan", "Can view production plan"),
        )

    def __str__(self):
        return '{} ({}) - {},-'.format(self.user, self.state, self.price)


class ProductOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return '{} - {} - {}'.format(self.order.user, self.product, self.quantity)


class ResourceOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    notes = models.TextField(null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    delivered = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return '{} ({}) - {},-'.format(self.created.date(), self.state, self.price)

    @classmethod
    def create(cls, request):
        resources = [(Resource.objects.filter(id=key).first(), decimal.Decimal(request.data[key]))
                     for key in request.data if float(request.data[key]) > 0]
        resources = [(resource, weight) for resource, weight in resources if resource is not None]
        if len(resources) == 0:
            return False

        order = cls.objects.create(user=request.user, state=State.objects.get_or_create(title='nezpracováno')[0])

        for resource, weight in resources:
            ResourceResOrder(order=order, resource=resource, weight=weight * 1000).save()
            order.price += resource.price * weight

        order.save()
        return order

    def deliver(self):
        self.state = State.objects.get_or_create(title='přijato')[0]
        for res_id, weight in self.resourceresorder_set.values_list('resource', 'weight'):
            res = Resource.objects.get(id=res_id)
            res.stock += weight
            res.save()
        self.save()


class ResourceResOrder(models.Model):
    """
    One item of specific resource order
    """
    order = models.ForeignKey(ResourceOrder, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.SET_NULL, null=True)
    weight = models.DecimalField(max_digits=8, decimal_places=2, default=1)

    def __str__(self):
        return '{} - {} - {}kg'.format(self.order.created.date(), self.resource, self.weight / 1000)
