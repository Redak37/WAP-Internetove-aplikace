from django.contrib.auth.models import UserManager
from .models import ProductCategory, Product, ProductResource, Resource, Route, Order, User
from .util import APIError
from datetime import datetime


def get_int(value_name, value_str, min_inclusive=None, max_inclusive=None):
    try:
        value = int(value_str)
    except:
        raise APIError(f'Nesprávné {value_name}')
    if min_inclusive is not None and value < min_inclusive:
        raise APIError(f'{value_name}: Hodnota musí být minimálně {min_inclusive}')
    if max_inclusive is not None and value > max_inclusive:
        raise APIError(f'{value_name}: Hodnota musí být maximálně {max_inclusive}')
    return value


def get_float(value_name, value_str, min_inclusive=None, max_inclusive=None):
    try:
        value = float(value_str)
    except:
        raise APIError(f'Nesprávné {value_name}')
    if min_inclusive is not None and value < min_inclusive:
        raise APIError(f'{value_name}: Hodnota musí být minimálně {min_inclusive}')
    if max_inclusive is not None and value > max_inclusive:
        raise APIError(f'{value_name}: Hodnota musí být maximálně {max_inclusive}')
    return value


def get_product_categories():
    return ProductCategory.objects.all()


def productcategory_from_name(name):
    try:
        return ProductCategory.objects.get(title=name)
    except Exception as e:
        raise APIError('Neexistující kategorie produktu')


def productcategory_from_id(product_category_id):
    if isinstance(product_category_id, str):
        product_category_id = get_int('ID kategorie produktu', product_category_id)
    try:
        return ProductCategory.objects.get(id=product_category_id)
    except Exception as e:
        raise APIError('Neexistující kategorie produktu')


def product_from_id(product_id):
    if isinstance(product_id, str):
        product_id = get_int('ID produktu', product_id)
    try:
        return Product.objects.get(id=product_id)
    except Exception as e:
        raise APIError('Neexistující produkt')


def resource_from_id(resource_id):
    if isinstance(resource_id, str):
        resource_id = get_int('ID suroviny', resource_id)
    try:
        return Resource.objects.get(id=resource_id)
    except Exception as e:
        raise APIError('Neexistující surovina')


def user_from_id(user_id):
    if isinstance(user_id, str):
        user_id = get_int('ID uživatele', user_id)
    try:
        return User.objects.get(id=user_id)
    except Exception as e:
        raise APIError('Neexistující uživatel')


def order_from_id(order_id):
    if isinstance(order_id, str):
        order_id = get_int('ID objednávky', order_id)
    try:
        return Order.objects.get(id=order_id)
    except Exception as e:
        raise APIError('Neexistující objednávka')


def route_from_id(route_id):
    if isinstance(route_id, str):
        route_id = get_int('ID cesty', route_id)
    try:
        return Route.objects.get(id=route_id)
    except Exception as e:
        raise APIError('Neexistující cesta')


def prepare_product_data(data):
    params = {}
    if not data.get('title'):
        raise APIError('Název produktu je prázdný')
    params['title'] = data['title']
    params['category'] = productcategory_from_id(data['category'])
    params['price'] = get_float('Cena', data['price'], 0)
    params['weight'] = get_float('Váha', data['weight'], 0)
    resources_params = [
        {
            'resource': resource_from_id(resource['resource']),
            'weight': get_float('Váha', resource['weight'], 0)
        }
        for resource in data.get('resources', [])
    ]
    return params, resources_params


def add_product(data):
    product_params, resources_params = prepare_product_data(data)
    product = Product.objects.create(**product_params)
    for resource_params in resources_params:
        ProductResource.objects.create(product=product, **resource_params)
    return product


def update_product(product_id, data):
    product = product_from_id(product_id)
    product_params, resources_params = prepare_product_data(data)
    ProductResource.objects.filter(product=product).delete()
    product.__dict__.update(**product_params)
    product.save()
    for resource_params in resources_params:
        ProductResource.objects.create(product=product, **resource_params)
    return product


def prepare_route_data(data, update=False):
    params = {'driver': user_from_id(data['driver'])}
    try:
        params['date'] = datetime.strptime(data['date'], r'%Y-%m-%d')
    except:
        raise APIError('Datum cesty: nesprávný formát data')
    orders_params = []
    for i, order in enumerate(data['orders']):
        order_obj = order_from_id(order['order'])
        if order_obj.route is not None and not update:
            raise APIError('Objednávka již má přiřazenou cestu')
        orders_params.append((order_obj, {'route_index': i}))
    return params, orders_params


def add_route(data):
    route_params, orders_params = prepare_route_data(data)
    route = Route.objects.create(**route_params)
    for order, order_params in orders_params:
        order.route = route
        order.route_index = order_params['route_index']
        order.save()
    return route


def update_route(route_id, data):
    route = route_from_id(route_id)
    route_params, orders_params = prepare_route_data(data, update=True)
    Order.objects.filter(route=route).update(route=None, route_index=0)
    route.date = route_params['date']
    route.driver = route_params['driver']
    route.save()
    for order, order_params in orders_params:
        order.route = route
        order.route_index = order_params['route_index']
        order.save()
    return route


def delete_route(route_id):
    route = route_from_id(route_id)
    Route.objects.filter(id=route.id).delete()
