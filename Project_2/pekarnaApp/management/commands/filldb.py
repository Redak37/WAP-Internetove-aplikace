from django.contrib.auth.models import Permission
from django.core.management.base import BaseCommand
from pekarnaApp.models import *


class Command(BaseCommand):
    help = 'Fill database with initial data'

    @staticmethod
    def _add_states():
        for state in ["Vytvořena", "Zaplacena", "Potvrzena", "Připravena", "Na cestě", "Doručena", "Zamítnuta",
                      "Zrušena zákazníkem"]:
            State.objects.get_or_create(title=state)

    def add_arguments(self, parser):
        parser.add_argument(
            '--with_test_data',
            action='store_true',
            help='Also include test data',
        )

    def handle(self, *args, **kwargs):
        self._add_groups()
        self._add_states()
        if kwargs['with_test_data']:
            self._add_product_categories()
            self._add_products()
            self._add_users()

    @staticmethod
    def _add_groups():
        auth_permissions = Permission.objects.filter(content_type__app_label='auth')
        app_permissions = Permission.objects.filter(content_type__app_label='pekarnaApp')

        view_product = app_permissions.get(codename='view_product')

        add_order = app_permissions.get(codename='add_order')

        view_car = app_permissions.get(codename='view_car')
        view_order = app_permissions.get(codename='view_order')
        change_order = app_permissions.get(codename='change_order')

        view_resourceorder = app_permissions.get(codename='view_resourceorder')
        change_resourceorder = app_permissions.get(codename='change_resourceorder')
        add_resourceorder = app_permissions.get(codename='add_resourceorder')
        delete_resourceorder = app_permissions.get(codename='delete_resourceorder')

        add_user = auth_permissions.get(codename='add_user')
        change_user = auth_permissions.get(codename='change_user')
        delete_user = auth_permissions.get(codename='delete_user')
        view_user = auth_permissions.get(codename='view_user')

        add_resource = app_permissions.get(codename='add_resource')
        change_resource = app_permissions.get(codename='change_resource')
        delete_resource = app_permissions.get(codename='delete_resource')
        view_resource = app_permissions.get(codename='view_resource')

        change_product = app_permissions.get(codename='change_product')
        add_product = app_permissions.get(codename='add_product')
        delete_product = app_permissions.get(codename='delete_product')

        add_car = app_permissions.get(codename='add_car')
        change_car = app_permissions.get(codename='change_car')
        delete_car = app_permissions.get(codename='delete_car')

        add_route = app_permissions.get(codename='add_route')
        change_route = app_permissions.get(codename='change_route')
        delete_route = app_permissions.get(codename='delete_route')
        view_route = app_permissions.get(codename='view_route')

        view_cookplan = app_permissions.get(codename='view_cookplan')

        groups = {
            'Uživatel': [view_product],
            'Zákazník': [add_order, view_product],
            'Zaměstnanec': [view_car, view_order, change_order, view_product],
            'Skladník': [view_resource, view_resourceorder, change_resourceorder, add_resourceorder,
                         delete_resourceorder,
                         view_car, view_order, change_order, view_product, view_cookplan],
            'Řidič': [view_car, view_order, change_order, view_product, add_route, change_route, delete_route,
                      view_route],
            'Pekař': [view_car, view_order, change_order, view_product, view_cookplan],
            'Správce': [add_user, change_user, delete_user, view_user, add_resource, change_resource, delete_resource,
                        view_resource, change_product, add_product, delete_product, add_car, change_car, delete_car,
                        view_car, view_order, change_order, view_product, add_route, change_route, delete_route,
                        view_route,
                        view_cookplan]
        }

        for group, perms in groups.items():
            new_group, created = Group.objects.get_or_create(name=group)
            new_group.permissions.set(perms)

    @staticmethod
    def _add_product_categories():
        for title in [
            'Chléb',
            'Rohlíky',
            'Housky a kaiserky',
            'Bagety',
            'Ostatní slané pečivo',
            'Sladké pečivo'
        ]:
            ProductCategory.objects.get_or_create(title=title)

    @staticmethod
    def _add_products():
        resources = [
            ('Mouka', 14, 1000, ["Lepek"]),
            ('Droždí', 57, 1000, []),
            ('Sůl', 20, 1000, []),
            ('Olej', 29, 1000, []),
            ('Sádlo', 60, 1000, ["Mléko (laktóza)"]),
            ('Máslo', 220, 1000, ["Mléko (laktóza)"]),
            ('Žitná mouka', 25, 1000, ["Lepek"]),
            ('Celozrnná mouka', 41, 1000, ["Lepek"]),
            ('Mák', 128, 1000, ["Lepek"]),
            ('Cukr', 15, 1000, []),
            ('Kmín', 380, 1000, []),
            ('Vejce', 380, 1000, ['Vejce']),
            ('Sója', 380, 1000, ['Sója']),
            ('Sezam', 380, 1000, ['Sezam']),
        ]

        for title, price, amount, allergens in resources:
            resource = Resource.objects.get_or_create(title=title, price=price, stock=amount)[0]
            for allergen in allergens:
                resource.allergens.add(Allergen.objects.get_or_create(title=allergen)[0])
            resource.save()

        data = [
            ('Chléb', [
                ('Chléb pšeničný', 24.90, 750, 'Velmi chutný pšeničný chléb!',
                 {'Mouka': 500, 'Droždí': 25, 'Sůl': 10, 'Olej': 20}),
                ('Chléb pšeničný malý', 24.90, 350, 'Velmi chutný pšeničný chléb!',
                 {'Mouka': 200, 'Droždí': 12, 'Sůl': 5, 'Olej': 10}),
                ('Chléb celozrnný', 34.90, 500, 'Velmi chutný celozrnný chléb.',
                 {'Mouka': 200, 'Celozrnná mouka': 180, 'Droždí': 20, 'Sůl': 10, 'Olej': 20, 'Vejce': 10}),
                ('Chléb žitný', 54.90, 500, 'Velmi chutný žitný chléb.',
                 {'Žitná mouka': 380, 'Droždí': 20, 'Sůl': 10, 'Olej': 20}),
                ('Chléb podmáslový', 54.90, 500, 'Velmi chutný podmáslový hléb.',
                 {'Mouka': 500, 'Droždí': 25, 'Sůl': 10, 'Máslo': 30}),
            ]),
            ('Rohlíky', [
                ('Rohlík tukový', 1.40, 50, 'Velmi chutný tukový rohlík.',
                 {'Mouka': 38, 'Droždí': 2, 'Sůl': 3, 'Olej': 6}),
                ('Rohlík sádlový', 2.90, 60, 'Velmi chutný sádlový rohlík.',
                 {'Mouka': 42, 'Droždí': 3, 'Sůl': 4, 'Sádlo': 7}),
                ('Rohlík celozrnný', 3.90, 50, 'Velmi chutný celozrnný rohlík.',
                 {'Mouka': 15, 'Celozrnná mouka': 12, 'Droždí': 2, 'Sůl': 3, 'Olej': 5, 'Vejce': 10}),
                ('Rohlík žitný', 6.90, 75, 'Velmi chutný žitný rohlík.',
                 {'Žitná mouka': 45, 'Droždí': 4, 'Sůl': 5, 'Olej': 7}),
                ('Rohlík královský', 4.40, 100, 'Velmi chutný rohlík, královsky velký.',
                 {'Mouka': 60, 'Droždí': 5, 'Sůl': 6, 'Olej': 8}),
            ]),
            ('Housky a kaiserky', [
                ('Houska razená bez posypu', 2.40, 50, 'Velmi chutná houska.',
                 {'Mouka': 38, 'Droždí': 2, 'Sůl': 3, 'Olej': 6}),
                ('Houska ražená se solí', 2.90, 55, 'Velmi chutná houska se solí.',
                 {'Mouka': 40, 'Droždí': 2, 'Sůl': 10, 'Olej': 6}),
                ('Houska ražená sypaná mákem', 3.40, 55, 'Velmi chutná houska s mákem.',
                 {'Mouka': 40, 'Droždí': 2, 'Sůl': 1, 'Cukr': 2, 'Mák': 5, 'Olej': 6}),
                ('Kaiserka cereální', 2.50, 60, 'Velmi chutná kaiserka.',
                 {'Mouka': 25, 'Celozrnná mouka': 15, 'Droždí': 3, 'Sůl': 4, 'Olej': 7, 'Vejce': 10}),
                ('Kaiserka řemeslná tmavá', 4.40, 75, 'Velmi chutná kaiserka.',
                 {'Mouka': 10, 'Celozrnná mouka': 30, 'Droždí': 2, 'Sůl': 3, 'Olej': 6}),
                ('Dalamánek', 5.90, 60, 'Velmi chutný dalamánek.',
                 {'Mouka': 38, 'Droždí': 2, 'Sůl': 3, 'Olej': 6, 'Kmín': 5}),
            ])
        ]

        for category, products in data:
            category_ = ProductCategory.objects.get_or_create(title=category)[0]
            for title, price, weight, desc, resources in products:
                product = Product.objects.get_or_create(title=title, price=price, weight=weight, description=desc,
                                                        category=category_)[0]
                for resource, amount in resources.items():
                    newResource = Resource.objects.get_or_create(title=resource)[0]
                    ProductResource.objects.get_or_create(product=product, resource=newResource, weight=amount)

    @staticmethod
    def _add_users():
        zamestnanec_group = Group.objects.get(name="Zaměstnanec")

        zakaznik = {
            "first_name": "Franta",
            "last_name": "Zakaznik",
            "username": "zakaznik",
            "email": "zakaznik@centrum.cz",
            "is_active": True,
        }
        user = User.objects.get_or_create(**zakaznik)[0]
        user.groups.add(zamestnanec_group)
        user.groups.add(Group.objects.get(name="Zákazník"))
        user.set_password("zakaznik")
        user.save()

        skladnik = {
            "first_name": "Franta",
            "last_name": "Skladník",
            "username": "skladnik",
            "email": "skladnik@centrum.cz",
            "is_active": True,
        }
        user = User.objects.get_or_create(**skladnik)[0]
        user.groups.add(zamestnanec_group)
        user.groups.add(Group.objects.get(name="Skladník"))
        user.set_password("skladnik")
        user.save()

        ridic = {
            "first_name": "Franta",
            "last_name": "Řidič",
            "username": "ridic",
            "email": "ridic@centrum.cz",
            "is_active": True,
        }
        user = User.objects.get_or_create(**ridic)[0]
        user.groups.add(zamestnanec_group)
        user.groups.add(Group.objects.get(name="Řidič"))
        user.set_password("ridic")
        user.save()

        pekar = {
            "first_name": "Franta",
            "last_name": "Pekař",
            "username": "pekar",
            "email": "pekar@centrum.cz",
            "is_active": True,
        }
        user = User.objects.get_or_create(**pekar)[0]
        user.groups.add(zamestnanec_group)
        user.groups.add(Group.objects.get(name="Pekař"))
        user.set_password("pekar")
        user.save()

        spravce = {
            "first_name": "Franta",
            "last_name": "Správce",
            "username": "spravce",
            "email": "spravce@centrum.cz",
            "is_active": True,
        }
        user = User.objects.get_or_create(**spravce)[0]
        user.groups.add(zamestnanec_group)
        user.groups.add(Group.objects.get(name="Správce"))
        user.set_password("spravce")
        user.save()
