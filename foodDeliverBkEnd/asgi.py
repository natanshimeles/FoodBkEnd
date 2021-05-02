# import os

# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.core.asgi import get_asgi_application
# import Order.routing

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

# application = ProtocolTypeRouter({
#   "http": get_asgi_application(),
#   "websocket": AuthMiddlewareStack(
#         URLRouter(
#             Order.routing.websocket_urlpatterns
#         )
#     ),
# })

"""
ASGI config for BackEnd project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodDeliverBkEnd.settings')

application = get_asgi_application()
