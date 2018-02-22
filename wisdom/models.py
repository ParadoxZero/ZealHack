from django.db import models

# Create your models here.
TIME_FORMAT = '%d/%m/%Y %H:%M:%S'


class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField()


class Location(models.Model):
    name = models.CharField(max_length=255)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    longitude = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255)


class Rating(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    rating = models.DecimalField(max_digits=1, decimal_places=0)
    review = models.TextField()

    @staticmethod
    def create_rating(request):
        rating = Rating(
            name=request.POST['name'],
            email=request.POST['email'],
            rating=request.POST['rating'],
            review=request.POST['review']
        )
        rating.save()


class Notifications(models.Model):
    date = models.DateTimeField()
    text = models.CharField(max_length=500)
    url = models.URLField()

    @staticmethod
    def get_latest_notifications(request):
        datetime = request.POST['datetime']
        datetime.strptime(datetime, TIME_FORMAT)
        return Notifications.objects.filter(date__gte=datetime)

    @staticmethod
    def get_latest_notifications(length=10):
        return Notifications.objects.all().order_by('-date')[:length]
