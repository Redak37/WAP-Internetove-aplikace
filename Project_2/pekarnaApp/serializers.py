from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from django.contrib.auth.models import User, Group

from pekarnaApp.models import Product, ProductCategory, Resource, Allergen, Car, Order, ProductOrder, State, \
    ResourceOrder, ProductResource, Route, ResourceResOrder


class ProductCategorySerializer(ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ResourceSerializer(ModelSerializer):
    allergens = PrimaryKeyRelatedField(many=True, queryset=Allergen.objects.all())

    class Meta:
        model = Resource
        fields = '__all__'
        depth = 1


class ProductResourceSerializer(ModelSerializer):
    resource = ResourceSerializer()

    class Meta:
        model = ProductResource
        fields = ('resource', 'weight',)


class ProductSerializer(ModelSerializer):
    resources = ProductResourceSerializer(many=True)
    category = ProductCategorySerializer()

    class Meta:
        model = Product
        fields = ('id', 'title', 'category', 'price', 'weight', 'description', 'resources',)


class AllergenSerializer(ModelSerializer):
    class Meta:
        model = Allergen
        fields = '__all__'
        depth = 1


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups', 'first_name', 'last_name', 'last_login', 'date_joined',
                  'is_superuser', 'is_staff', 'is_active', 'user_permissions',)
        depth = 1


class UserCreateSerializer(ModelSerializer):
    groups = PrimaryKeyRelatedField(
        many=True,
        queryset=Group.objects.all()
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups', 'first_name', 'last_name', 'last_login', 'is_active',)
        depth = 1


class GroupSerialized(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
        depth = 1


class CarSerializer(ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'
        depth = 1


class OrderSerializer(ModelSerializer):
    user = PrimaryKeyRelatedField(
        many=False,
        queryset=User.objects.all(),
    )
    state = PrimaryKeyRelatedField(
        many=False,
        queryset=State.objects.all(),
    )

    class Meta:
        model = Order
        fields = '__all__'
        depth = 1


class MyOrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        depth = 1


class ProductOrderGetSerializer(ModelSerializer):
    class Meta:
        model = ProductOrder
        fields = ('quantity', 'product',)
        depth = 1


class ProductOrderSerializer(ModelSerializer):
    product = PrimaryKeyRelatedField(
        many=False,
        queryset=Product.objects.all()
    )
    order = PrimaryKeyRelatedField(
        many=False,
        queryset=Order.objects.all()
    )

    class Meta:
        model = ProductOrder
        fields = '__all__'
        depth = 1


class OrderGetSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        depth = 1


class StateSerializer(ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'
        depth = 1


class ResourceOrderSerializer(ModelSerializer):
    class Meta:
        model = ResourceOrder
        fields = ('id', 'user', 'created', 'price', 'state',)
        depth = 1


class ResourceResOrderSerializer(ModelSerializer):
    class Meta:
        model = ResourceResOrder
        fields = ('resource', 'weight',)
        depth = 1


class RouteOrderSerializer(ModelSerializer):
    class StateSerializer(ModelSerializer):
        class Meta:
            model = State
            fields = ('title',)

    user = UserCreateSerializer()
    state = StateSerializer()

    class Meta:
        model = Order
        fields = '__all__'
        depth = 1


class RouteSerializer(ModelSerializer):
    orders = RouteOrderSerializer(many=True)
    driver = UserCreateSerializer()

    class Meta:
        model = Route
        fields = ('id', 'date', 'driver', 'orders',)
