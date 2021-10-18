import inspect
import json
from collections import OrderedDict

from aiohttp.http_exceptions import HttpBadRequest
from aiohttp.web import Request, Response
from aiohttp.web_exceptions import HTTPMethodNotAllowed

from models import Customer, Product, Purchase, session

__version__ = '0.1.0'

DEFAULT_METHODS = ('GET', 'POST', 'PUT', 'DELETE')


class RestEndpoint:
    def __init__(self):
        self.methods = {}

        for method_name in DEFAULT_METHODS:
            method = getattr(self, method_name.lower(), None)
            if method:
                self.register_method(method_name, method)

    def register_method(self, method_name, method):
        self.methods[method_name.upper()] = method

    async def dispatch(self, request: Request):
        method = self.methods.get(request.method.upper())
        if not method:
            raise HTTPMethodNotAllowed('', DEFAULT_METHODS)

        wanted_args = list(inspect.signature(method).parameters.keys())
        available_args = request.match_info.copy()
        available_args.update({'request': request})

        unsatisfied_args = set(wanted_args) - set(available_args.keys())
        if unsatisfied_args:
            # Expected match info that doesn't exist
            raise HttpBadRequest('')

        return await method(**{arg_name: available_args[arg_name] for arg_name in wanted_args})


class CustomerCollectionEndpoint(RestEndpoint):

    def __init__(self, resource):
        super().__init__()
        self.resource = resource

    async def post(self, request):
        data = await request.json()
        customer = Customer(
            first_name=data['first_name'],
            infix=data['infix'],
            last_name=data['last_name'],
            address_street=data['address_street'],
            address_number=data['address_number'],
            city=data['city'],
            zipcode=data['zipcode'],
            country=data['country']
        )
        session.add(customer)
        session.commit()

        return Response(status=201, body=self.resource.encode({
            'customer':
                {
                    'id': customer.id,
                    'first_name': customer.first_name,
                    'infix': customer.infix,
                    'last_name': customer.last_name,
                    'address_street': customer.address_street,
                    'address_number': customer.address_number,
                    'city': customer.city,
                    'zipcode': customer.zipcode,
                    'country': customer.country,

                }

        }), content_type='application/json')

    async def get(self) -> Response:
        data = []

        customers = session.query(Customer).all()
        for instance in self.resource.collection.values():
            data.append(self.resource.render(instance))
        data = self.resource.encode(data)
        return Response(status=200, body=self.resource.encode({
            'customers': [
                {
                    'id': customer.id,
                    'first_name': customer.first_name,
                    'infix': customer.infix,
                    'last_name': customer.last_name,
                    'address_street': customer.address_street,
                    'address_number': customer.address_number,
                    'city': customer.city,
                    'zipcode': customer.zipcode,
                    'country': customer.country
                }

                for customer in session.query(Customer)

            ]
        }), content_type='application/json')


class CustomerEndpoint(RestEndpoint):
    def __init__(self, resource):
        super().__init__()
        self.resource = resource

    async def get(self, instance_id):
        instance = session.query(Customer).filter(Customer.id == instance_id).first()
        if not instance:
            return Response(status=404, body=json.dumps({'customer not found': 404}), content_type='application/json')
        data = self.resource.render_and_encode(instance)
        return Response(status=200, body=data, content_type='application/json')

    async def put(self, request, instance_id):

        data = await request.json()

        customer = session.query(Customer).filter(Customer.id == instance_id).first()
        customer.first_name = data['first_name']
        customer.infix = data['infix']
        customer.last_name = data['last_name']
        customer.address_street = data['address_street']
        customer.address_number = data['address_number']
        customer.city = data['city']
        customer.zipcode = data['zipcode']
        customer.country = data['country']
        session.add(customer)
        session.commit()

        return Response(status=201, body=self.resource.render_and_encode(customer),
                        content_type='application/json')

    async def delete(self, instance_id):
        customer = session.query(Customer).filter(Customer.id == instance_id).first()
        if not customer:
            return Response(status=404, body=json.dumps({'Customer not  found': 404}), content_type='application/json')
        session.delete(customer)
        session.commit()
        return Response(status=204)


class ProductEndpoint(RestEndpoint):
    def __init__(self, resource):
        super().__init__()
        self.resource = resource

    async def post(self, request):
        data = await request.json()
        product = Product(
            name=data['name'],
            price=data['price'],
            description=data['description'],
            image_url=data['image_url'],

        )
        session.add(product)
        session.commit()

        return Response(status=201, body=self.resource.encode({
            'product':
                {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'description': product.description,
                    'image_url': product.image_url
                }

        }), content_type='application/json')

    async def get(self, instance_id):
        instance = session.query(Product).filter(Product.id == instance_id).first()
        if not instance:
            return Response(status=404, body=json.dumps({'product not found': 404}), content_type='application/json')
        data = self.resource.render_and_encode(instance)
        return Response(status=200, body=data, content_type='application/json')

    async def put(self, request, instance_id):

        data = await request.json()

        product = session.query(Product).filter(Product.id == instance_id).first()
        product.name = data['name']
        product.price = data['price']
        product.description = data['description']
        product.image_url = data['image_url']
        session.add(product)
        session.commit()

        return Response(status=201, body=self.resource.render_and_encode(product),
                        content_type='application/json')

    async def delete(self, instance_id):
        product = session.query(Product).filter(Product.id == instance_id).first()
        if not product:
            return Response(status=404, body=json.dumps({'Product not  found': 404}), content_type='application/json')
        session.delete(product)
        session.commit()
        return Response(status=204)


class ProductCollectionEndpoint(RestEndpoint):

    def __init__(self, resource):
        super().__init__()
        self.resource = resource

    async def post(self, request):
        data = await request.json()
        products = Product(
            name=data['name'],
            price=data['price'],
            description=data['description'],
            image_url=data['image_url']
        )
        session.add(products)
        session.commit()

        return Response(status=201, body=self.resource.encode({
            'product':
                {
                    'id': products.id,
                    'name': products.name,
                    'price': products.price,
                    'description': products.description,
                    'image_url': products.image_url

                }

        }), content_type='application/json')

    async def get(self) -> Response:
        data = []

        products = session.query(Product).all()
        for instance in self.resource.collection.values():
            data.append(self.resource.render(instance))
        data = self.resource.encode(data)
        return Response(status=200, body=self.resource.encode({
            'customers': [
                {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'description': product.description,
                    'image_url': product.image_url

                }

                for product in session.query(Customer)

            ]
        }), content_type='application/json')


class PurchasetEndpoint(RestEndpoint):

    def __init__(self, resource):
        super().__init__()
        self.resource = resource

    async def post(self, request):
        data = await request.json()
        purchase = Purchase(
            customer=data['customer'],
            product=data['product'],
            quantity=data['quantity']

        )
        session.add(purchase)
        session.commit()

        return Response(status=201, body=self.resource.encode({
            'purchase':
                {
                    'id': purchase.id,
                    'customer': purchase.customer,
                    'product': purchase.product,
                    'quantity': purchase.quantity

                }

        }), content_type='application/json')

    async def get(self, instance_id):
        instance = session.query(Purchase).filter(Purchase.id == instance_id).first()
        if not instance:
            return Response(status=404, body=json.dumps({'purchase not found': 404}), content_type='application/json')
        data = self.resource.render_and_encode(instance)
        return Response(status=200, body=data, content_type='application/json')

    async def put(self, request, instance_id):

        data = await request.json()

        purchase = session.query(Purchase).filter(Purchase.id == instance_id).first()
        purchase.customer = data['customer']
        purchase.product = data['product']
        purchase.quantity = data['quantity']

        session.add(purchase)
        session.commit()

        return Response(status=201, body=self.resource.render_and_encode(purchase),
                        content_type='application/json')

    async def delete(self, instance_id):
        purchase = session.query(Purchase).filter(Purchase.id == instance_id).first()
        if not purchase:
            return Response(status=404, body=json.dumps({'Purchase not  found': 404}), content_type='application/json')
        session.delete(purchase)
        session.commit()
        return Response(status=204)


class PurchaseCollectionEndpoint(RestEndpoint):

    def __init__(self, resource):
        super().__init__()
        self.resource = resource

    async def post(self, request):
        data = await request.json()
        purchase = Purchase(
            customer=data['customer'],
            product=data['product'],
            quantity=data['quantity']
        )
        session.add(purchase)
        session.commit()

        return Response(status=201, body=self.resource.encode({
            'purchase':
                {
                    'id': purchase.id,
                    'customer': purchase.customer,
                    'product': purchase.product,
                    'quantity': purchase.quantity,

                }

        }), content_type='application/json')

    async def get(self) -> Response:
        data = []

        purchases = session.query(Purchase).all()
        for instance in self.resource.collection.values():
            data.append(self.resource.render(instance))
        data = self.resource.encode(data)
        return Response(status=200, body=self.resource.encode({
            'purchase': [
                {
                    'id': purchase.id,
                    'customer': purchase.customer,
                    'product': purchase.product,
                    'quantity': purchase.quantity

                }

                for purchase in session.query(Purchase)

            ]
        }), content_type='application/json')


class RestResource:

    def __init__(self):

        self.collection = {}

    def render(self, instance):
        return OrderedDict((notes, getattr(instance, notes)) for notes in self.properties)

    @staticmethod
    def encode(data):
        return json.dumps(data, indent=4).encode('utf-8')

    def render_and_encode(self, instance):
        return self.encode(self.render(instance))
