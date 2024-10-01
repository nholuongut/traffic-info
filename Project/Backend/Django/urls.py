"""Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from TrafficJammer import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('info_street/<str:city>/',views.info_street,name="info"),
    path('all_streets/',views.all_streets,name="all_streets"),
    path('street/',views.street,name="crud_street"),
    path('car/',views.car_to_street,name="crud_car"),
    path('accident/',views.add_to_accident,name="accident"),
    path('specific_car/<str:license_plate>/',views.get_car,name='get_car'),
    path('all_cars/<int:section>/',views.all_cars,name='all_cars'),
    path('statistics/<int:street>/<str:begin>/<str:end>/',views.statistics,name='statistics'),
    path('statistics/<int:street>/<str:begin>/<str:end>/<str:week_day>/', views.statistics, name='statistics'),
    path('visibility/',views.visibility,name='visibility'),
    path('police/',views.police,name='police'),
    path('roadblock/',views.roadblock,name='roadblock'),
    path('licenses_by_city/<str:city>/',views.licenses_by_section,name='licenses_by_city'),
    path('charts/<str:type>/street=<int:street>&start_date=<str:begin>&end_date=<str:end>/',views.charts,name='charts'),
    path('available_cities/',views.available_cities,name='available cities')
]
