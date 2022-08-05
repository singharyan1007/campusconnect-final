from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="ShopHome"),
    path("hoodies/", views.hoodies, name="hoodies"),
    path("tshirts/", views.tshirts, name="tshirts"),
    path("about Us/", views.aboutus, name="aboutus"),
    path("productview/<int:myid>", views.productview, name="productview"),
    path('cart/', views.cart, name="cart"),
    path('managecart/', views.managecart, name="managecart"),
    path('delete-from-cart/', views.delete_items, name="delete_items"),
    path('update-cart/', views.update_items, name="update_items"),
    path('checkout/', views.checkout, name="checkout"),
    path('handlerequest/', views.handlerequest, name="handlerequest"),
    path('success/', views.success, name="handlerequest"),

]
