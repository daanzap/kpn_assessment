from aiohttp.web import Application, run_app

from shop_rest import RestResource, CustomerEndpoint, CustomerCollectionEndpoint, ProductEndpoint, \
    ProductCollectionEndpoint, PurchasetEndpoint, PurchaseCollectionEndpoint

customers = {}
app = Application()
rest_resource = RestResource()
customer_endpoint = CustomerEndpoint(rest_resource)
customer_list_endpoint = CustomerCollectionEndpoint(rest_resource)

app.router.add_route('*', '/customer/{instance_id}', CustomerEndpoint(rest_resource).dispatch)
app.router.add_route('*', '/customer/', CustomerCollectionEndpoint(rest_resource).dispatch)
app.router.add_route('*', '/product/{instance_id}', ProductEndpoint(rest_resource).dispatch)
app.router.add_route('*', '/product/', ProductCollectionEndpoint(rest_resource).dispatch)
app.router.add_route('*', '/purchase/{instance_id}', PurchasetEndpoint(rest_resource).dispatch)
app.router.add_route('*', '/purchase/', PurchaseCollectionEndpoint(rest_resource).dispatch)

if __name__ == '__main__':
    run_app(app)
