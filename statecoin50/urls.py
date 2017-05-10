from django.conf.urls import url
from . import views
#app_name = 'statecoin50'
urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^user/(?P<user_pk>\d+)/$', views.coin_collector, name='coin_collector'),
    url(r'^user/(?P<user_pk>\d+)/wishlist$', views.collection_wishlist, name='collection_wishlist'),
    url(r'^coin/(?P<coin_pk>\d+)/$', views.coindetail, name='coindetail'),

]
