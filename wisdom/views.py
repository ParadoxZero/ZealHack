from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from wisdom.models import *


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


#####################
#   Template View   #
#####################

class Index(TemplateView):
    template_name = 'wisdom/index.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['notifications'] = [{
            'date': i.date,
            'text': i.text,
            'url': i.url
        } for i in Notifications.get_latest_notifications()]
        context['services'] = [{
            'name': i.name,
            'description': i.description,
            'image': i.image
        } for i in Service.objects.all()]
        return context
