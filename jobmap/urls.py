from . import views, geo
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('figures',views.figuresAPI,name='figures'),
    path('scrape',geo.scrapeJobs,name='scrape'),
    path('discription/<int:id>',views.discriptionAPI,name='discriptions'),
]
