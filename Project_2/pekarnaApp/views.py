from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import Group
from django.views.decorators.csrf import ensure_csrf_cookie
import datetime

from .forms import SignUpForm, CarForm, UserForm, UserCreateForm, ResourceForm, OrderForm
import pekarnaApp.managers as managers
from pekarnaApp.models import Product, Resource, Allergen, Car, User, Order, State, ProductOrder, \
    ResourceOrder, Route, ProductResource, ResourceResOrder
from pekarnaApp.serializers import ProductCategorySerializer, ProductSerializer, ResourceSerializer, UserSerializer, \
    UserCreateSerializer, AllergenSerializer, CarSerializer, GroupSerialized, OrderSerializer, ProductOrderSerializer, \
    OrderGetSerializer, StateSerializer, ProductOrderGetSerializer, ResourceOrderSerializer, MyOrderSerializer, \
    RouteSerializer, ResourceResOrderSerializer

ROUTE_PERMS = ['pekarnaApp.add_route', 'pekarnaApp.delete_route', 'pekarnaApp.change_route', 'pekarnaApp.view_route']


@api_view()
@ensure_csrf_cookie
def csrf_view(request):
    return Response({})


@api_view(['POST'])
def login_view(request):
    data = request.data
    user = authenticate(request, username=data.get('username'), password=data.get('password'))
    try:
        login(request, user)
    except AttributeError:
        return Response({'errorMessage': 'Nesprávné přihlašovací údaje'},
                        status=status.HTTP_401_UNAUTHORIZED)

    return Response(status=status.HTTP_200_OK)


@api_view(['POST', 'GET'])
def registration_view(request):
    user_form = SignUpForm(request.data or None)
    data = {'form': render_to_string('form.html', {'form': user_form})}
    if request.method == 'POST':
        if user_form.is_valid():
            user_form.save()
        else:
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)

    return Response(data, status=status.HTTP_200_OK)


def model_view(request, object_id, model, form, perms):
    model_object = model.objects.filter(id=object_id).first()
    if request.method == 'DELETE':
        if model_object is None or not perms['delete']:
            return Response(status=status.HTTP_404_NOT_FOUND)
        model_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    object_form = form(request.data or None, instance=model_object)
    data = {'form': render_to_string('form.html', {'form': object_form})}
    if request.method == 'GET':
        return Response(data, status=status.HTTP_200_OK)

    # request.method == 'POST
    if object_form.is_valid():
        if (perms['add'] and model_object is None) or (perms['change'] and model_object is not None):
            object_form.save()
            return Response(status=status.HTTP_200_OK)
    return Response(data, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'POST', 'DELETE'])
def cars_view(request, car_id=None):
    perms = {
        'add': request.user.has_perm('pekarnaApp.add_car'),
        'change': request.user.has_perm('pekarnaApp.change_car'),
        'delete': request.user.has_perm('pekarnaApp.delete_car'),
    }
    return model_view(request, car_id, Car, CarForm, perms)


@api_view(['GET', 'POST', 'DELETE'])
def user_view(request, user_id=None):
    perms = {
        'add': False,
        'change': request.user.has_perm('auth.change_user'),
        'delete': request.user.has_perm('auth.delete_user'),
    }
    return model_view(request, user_id, User, UserForm, perms)


@api_view(['GET', 'POST'])
def user_create_view(request):
    perms = {'add': request.user.has_perm('auth.add_user'),
             'change': False,
             'delete': False}
    return model_view(request, None, User, UserCreateForm, perms)


@api_view(['GET', 'POST', 'DELETE'])
def resource_view(request, resource_id=None):
    perms = {
        'add': request.user.has_perm('pekarnaApp.add_resource'),
        'change': request.user.has_perm('pekarnaApp.change_resource'),
        'delete': request.user.has_perm('pekarnaApp.delete_resource'),
    }
    return model_view(request, resource_id, Resource, ResourceForm, perms)


@api_view(['POST'])
@permission_required('pekarnaApp.add_resourceorder')
def resource_order(request):
    if ResourceOrder.create(request):
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_required('pekarnaApp.view_resourceorder')
def resource_order_detail(request, order_id):
    return Response(ResourceResOrderSerializer(ResourceResOrder.objects.filter(order_id=order_id), many=True).data)


@api_view(['PUT'])
@permission_required('pekarnaApp.change_resourceorder')
def resourceOrderChangeState(request, resource_id, state):
    ResourceOrder.objects.filter(id=resource_id).update(state=State.objects.get_or_create(title=state)[0])
    return Response(status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_required('pekarnaApp.change_resourceorder')
def resourceOrderDelivered(request, resource_id):
    ResourceOrder.objects.get(id=resource_id).deliver()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)


@api_view()
@permission_required('pekarnaApp.view_product')
def products(request, category=None):
    resultProducts = Product.objects.order_by('title')
    if category is not None:
        resultProducts = resultProducts.filter(category__title=category)
    return Response(ProductSerializer(resultProducts, many=True).data)


@api_view()
def getUser(request):
    return Response(UserSerializer(request.user).data)


@api_view()
def getPerms(request):
    return Response(request.user.get_user_permissions().union(request.user.get_group_permissions()))


@api_view(['GET'])
@permission_required('pekarnaApp.view_resource')
def resources(request):
    return Response(ResourceSerializer(Resource.objects.order_by('title'), many=True).data)


@api_view(['GET'])
@permission_required('pekarnaApp.view_resourceorder')
def resource_orders(request):
    return Response(ResourceOrderSerializer(
        ResourceOrder.objects.exclude(state__title__in=['zrušeno', 'přijato']), many=True).data)


@api_view(['GET'])
@permission_required('pekarnaApp.view_resourceorder')
def resource_orders_history(request):
    return Response(ResourceOrderSerializer(
        ResourceOrder.objects.filter(state__title__in=['zrušeno', 'přijato']), many=True).data)


@api_view(['GET'])
def product_categories(request):
    pcs = ProductCategorySerializer(managers.get_product_categories(), many=True)
    return Response({'categories': pcs.data})


@api_view(['POST'])
@permission_required('pekarnaApp.add_product')
def add_product(request):
    try:
        product = managers.add_product(request.data)
        return Response({'id': product.id}, status=status.HTTP_201_CREATED)
    except managers.APIError as e:
        return Response({'errorMessage': e.message}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_required('pekarnaApp.change_product')
def edit_product(request, product_id):
    try:
        managers.update_product(product_id, request.data)
        return Response({}, status=status.HTTP_200_OK)
    except managers.APIError as e:
        return Response({'errorMessage': e.message}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_required('pekarnaApp.view_product')
def view_product(request, product_id):
    product = managers.product_from_id(product_id)
    ps = ProductSerializer(product)
    return Response(ps.data)


@api_view(['GET'])
@permission_required('pekarnaApp.view_product')
def allergens(request):
    return Response(AllergenSerializer(Allergen.objects.order_by('title'), many=True).data)


@api_view(['GET'])
@permission_required('pekarnaApp.view_car')
def cars(request):
    return Response(CarSerializer(Car.objects.order_by('driver__last_name'), many=True).data)


@api_view(['GET'])
@permission_required('pekarnaApp.view_user')
def users(request):
    return Response(UserSerializer(User.objects.order_by('last_name'), many=True).data)


@api_view(['GET'])
@permission_required('pekarnaApp.view_user')
def groups(request):
    return Response(GroupSerialized(Group.objects.order_by('name'), many=True).data)


@api_view(['GET'])
#@permission_required('pekarnaApp.view_user')
def drivers(request):
    return Response(UserCreateSerializer(
        User.objects.filter(groups__name="Řidič").filter(is_active=True), many=True).data)


@api_view(['GET', 'POST'])
def orders(request):
    if request.method == 'GET':
        return Response(OrderGetSerializer(Order.objects.order_by('created'), many=True).data)
    # request.method == 'POST':
    request.data['user'] = request.user.id
    request.data['state'] = State.objects.get(title='Vytvořena').id
    request.data['price'] = "{:.2f}".format(float(request.data['price']))
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'GET':
        if not request.user.has_perm('pekarnaApp.view_order'):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(OrderSerializer(order, many=False).data)
    elif request.method == 'PUT':
        if not request.user.has_perm('pekarnaApp.add_order') and not request.user.has_perm('pekarnaApp.change_order') and not request.user.has_perm('pekarnaApp.view_order'):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        request.data['user'] = order.user.id
        if request.data['state'] == State.objects.get(title='Doručena').id and order.delivered is None:
            request.data['delivered'] = datetime.datetime.today().isoformat()
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        if not request.user.has_perm('pekarnaApp.delete_order'):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_required(['pekarnaApp.add_order'])
def product_order(request):
    serializer = ProductOrderSerializer(data=request.data, many=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_required('pekarnaApp.add_order')
def my_orders(request, user_id):
    return Response(MyOrderSerializer(Order.objects.filter(user_id=user_id), many=True).data)


@api_view(['GET', 'POST', 'DELETE'])
def my_orders_view(request, order_id):
    perms = {
        'add': request.user.has_perm('pekarnaApp.add_order'),
        'change': request.user.has_perm('pekarnaApp.add_order'),
        'delete': request.user.has_perm('pekarnaApp.add_order'),
    }
    return model_view(request, order_id, Order, OrderForm, perms)


@api_view(['GET'])
def states(request):
    return Response(StateSerializer(State.objects.order_by('title'), many=True).data)


@api_view(['GET'])
def products_by_order(request, order_id):
    return Response(ProductOrderGetSerializer(ProductOrder.objects.filter(order=order_id), many=True).data)


@api_view(['GET'])
@permission_required('pekarnaApp.add_order')
def my_orders_cancel(request, order_id):
    order = Order.objects.get(id=order_id)
    stateCancel = State.objects.get(title="Zrušena zákazníkem")
    order.state = stateCancel
    order.save()
    return Response(StateSerializer(stateCancel).data)


@api_view(['GET'])
@permission_required('pekarnaApp.add_order')
def my_orders_pay(request, order_id):
    order = Order.objects.get(id=order_id)
    statePaid = State.objects.get(title="Zaplacena")
    order.state = statePaid
    order.save()
    return Response(StateSerializer(statePaid).data)


@api_view(['GET'])
@permission_required('pekarnaApp.change_order')
def my_orders_accept(request, order_id):
    order = Order.objects.get(id=order_id)
    stateAccept = State.objects.get(title="Potvrzena")
    order.state = stateAccept
    order.save()
    # Remove resources from stock
    for resource, amount in getResourcesFromOrder(order).items():
        resource.stock = max(resource.stock - amount, 0)  # Do not remove below zero
        resource.save()
    return Response(StateSerializer(stateAccept).data)


@api_view(['GET'])
@permission_required('pekarnaApp.change_order')
def my_orders_reject(request, order_id):
    order = Order.objects.get(id=order_id)
    stateRejected = State.objects.get(title="Zamítnuta")
    order.state = stateRejected
    order.save()
    return Response(StateSerializer(stateRejected).data)


@api_view(['GET'])
@permission_required('pekarnaApp.change_order')
def my_orders_complete(request, order_id):
    order = Order.objects.get(id=order_id)
    stateCompleted = State.objects.get(title="Připravena")
    order.state = stateCompleted
    order.save()
    return Response(StateSerializer(stateCompleted).data)


@api_view(['GET'])
@permission_required(ROUTE_PERMS)
def routes_view(request):
    return Response(RouteSerializer(Route.objects.order_by('driver__last_name'), many=True).data)


@api_view(['GET', 'POST', 'DELETE'])
@permission_required(ROUTE_PERMS)
def route_view(request, route_id=None):
    try:
        if request.method == 'GET':
            route = managers.route_from_id(route_id)
            return Response(RouteSerializer(route).data)
        elif request.method == 'POST':
            if route_id is None:
                route = managers.add_route(request.data)
            else:
                route = managers.update_route(route_id, request.data)
            return Response({'id': route.id})
        elif request.method == 'DELETE':
            managers.delete_route(route_id)
            return Response({})
    except managers.APIError as e:
        return Response({'errorMessage': e.message}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_required('pekarnaApp.view_product')
def product_allergens(request, product_id):
    allergen_set = set()
    for item in ProductResource.objects.filter(product=product_id):
        allergen_set = allergen_set.union(set(item.resource.allergens.all()))

    return Response(AllergenSerializer(allergen_set, many=True).data)


@api_view(['GET'])
@permission_required('pekarnaApp.change_order')
def order_set_state(request, order_id, state):
    state_obj = State.objects.get(title=state)
    if state == 'Doručena':
        Order.objects.filter(id=order_id).update(state=state_obj, delivered=datetime.datetime.today().isoformat())
    else:
        Order.objects.filter(id=order_id).update(state=state_obj)
    return Response({})


@api_view(['GET', 'POST'])
@permission_required('pekarnaApp.view_cookplan')
def orders_plan(request, date):
    ordersOnDate = Order.objects.filter(deliver_date=date)
    ordersConfirmed = ordersOnDate.filter(state__title="Potvrzena")
    newOrders = ordersOnDate.filter(state__title="Zaplacena")

    resourceList = {}
    resourcesPerOrder = {}
    newOrdersAcceptable = {}
    for order in ordersConfirmed:
        orderResources = getResourcesFromOrder(order)
        for resource, amount in orderResources.items():
            resourceList[resource] = resourceList.get(resource, 0) + amount
        resourcesPerOrder[order.id] = [(ResourceSerializer(resource).data, amount) for
                                       resource, amount in orderResources.items()]
    for order in newOrders:
        orderResources = getResourcesFromOrder(order)
        resourcesPerOrder[order.id] = [(ResourceSerializer(resource).data, amount) for
                                       resource, amount in orderResources.items()]
        newOrdersAcceptable[order.id] = all([(resource.stock >= amount) for resource, amount in orderResources.items()])
    ordersSer = MyOrderSerializer(ordersConfirmed, many=True).data
    newOrdersSer = MyOrderSerializer(newOrders, many=True).data
    resourcesSer = [(ResourceSerializer(resource).data, amount) for resource, amount in resourceList.items()]
    return Response({'orders': ordersSer, 'newOrders': newOrdersSer, 'resources': resourcesSer,
                     'resourcesPerOrder': resourcesPerOrder, 'newOrdersAcceptable': newOrdersAcceptable})


def getResourcesFromOrder(order):
    resourceList = {}
    for product, quantity in order.productorder_set.values_list('product', 'quantity'):
        for res in ProductResource.objects.filter(product=product):
            resourceList[res.resource] = resourceList.get(res.resource, 0) + res.weight * quantity

    return resourceList
