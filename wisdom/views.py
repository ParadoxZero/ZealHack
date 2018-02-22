from datetime import datetime
import googlemaps

from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

import config
from wisdom.models import *

initiative_slug = {
    'health': Service.Initiatives.HEALTHCARE,
    'social-service': Service.Initiatives.SOCIAL_SERVICE,
    'education': Service.Initiatives.EDUCATION,
    'emergency-services': Service.Initiatives.EMERGENCY_RESPONSE,
    'infrastructure': Service.Initiatives.INFRASTRUCTURE
}

map_client = googlemaps.Client(key=config.key)


def sort_key(x):
    return float(x['distance'][:-2])


#################
#   API calls   #
#################

@csrf_exempt
def get_notifications(request):
    if request.POST:
        notifications = Notifications.get_latest_notifications(request)
        return JsonResponse(data={
            'status': 'ok',
            'notifications': [{
                'text': i.text,
                'url': i.url,
                'date': i.date.strftime(TIME_FORMAT)
            } for i in notifications]
        })
    return JsonResponse(data={'status': 'Invalid Method'})


def get_service_all(request):
    services = Service.objects.all()
    return JsonResponse(data={
        'status': 'ok',
        'services': [{
            'name': i.name,
            'description': i.description,
            'image': i.image
        } for i in services]
    })


def get_service(request, id):
    try:
        service = Service.objects.get(id=id)
        locations = Location.objects.filter(service=service)
        return JsonResponse(data={
            'status': 'ok',
            'service_name': service.name,
            'description': service.description,
            'image': service.image,
            'locations': [{
                'name': i.name,
                'latitude': i.latitude,
                'longitude': i.longitude,
            } for i in locations]
        })
    except Service.DoesNotExist:
        return JsonResponse(data={
            'status': 'Does not exist'
        })


def post_review(request):
    Rating.create_rating(request)
    return JsonResponse(data={
        'status': 'ok'
    })


def get_nearest_locations(request):
    latitude = request.POST['latitude']
    longitude = request.POST['longitudes']

    location_list = Location.objects.all()
    destination_list = [[i.latitude, i.longitude] for i in location_list]
    result = map_client.distance_matrix(origins=[[latitude, longitude], ], destinations=destination_list)
    context = []
    for i in range(len(location_list)):
        context.append({
            'name': location_list[i].name,
            'distance': result['rows'][0]['elements'][i]['distance']['text'],
            'coordinates': [location_list[i].latitude, location_list[i].longitude]
        })
    context.sort(key=sort_key)
    return JsonResponse(data={
        "status": 'ok',
        'locations': context[:10]
    })


def get_nearest_locations_service(request, slug):
    latitude = request.POST['latitude']
    longitude = request.POST['longitudes']

    location_list = Location.objects.filter(service__initiative=initiative_slug[slug])
    destination_list = [[i.latitude, i.longitude] for i in location_list]
    result = map_client.distance_matrix(origins=[[latitude, longitude], ], destinations=destination_list)
    context = []
    for i in range(len(location_list)):
        context.append({
            'name': location_list[i].name,
            'distance': result['rows'][0]['elements'][i]['distance']['text'],
            'coordinates': [location_list[i].latitude, location_list[i].longitude]
        })
    context.sort(key=sort_key)
    return JsonResponse(data={
        "status": 'ok',
        'locations': context[:10]
    })


#####################
#   Template View   #
#####################

class Index(TemplateView):
    template_name = 'wisdom/index.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['notifications'] = [i for i in Notifications.get_latest_notifications()]
        context['services'] = [i for i in Service.objects.all()]
        return context


class ServiceDetails(TemplateView):
    template_name = 'wisdom/service_details.html'

    def get_context_data(self, **kwargs):
        context = super(ServiceDetails, self).get_context_data(**kwargs)
        try:
            service = Service.objects.get(slug=kwargs['slug'])
        except Service.DoesNotExist:
            raise Http404
        location_list = Location.objects.filter(service=service)
        image_list = ServiceImage.objects.filter(service=service)
        context['service'] = service
        context['location_list'] = location_list
        context['image_list'] = image_list
        return context


class InitiativeServiceList(TemplateView):
    template_name = 'wisdom/service-list.html'

    def get_context_data(self, **kwargs):
        context = super(InitiativeServiceList, self).get_context_data(**kwargs)
        try:
            service_list = Service.objects.filter(initiative=initiative_slug[kwargs['initiative_slug']])
        except KeyError:
            raise Http404
        context['service_list'] = service_list
        return context
