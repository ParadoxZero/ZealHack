from django.db import models

# Create your models here.
TIME_FORMAT = '%d/%m/%Y %H:%M:%S'


class Service(models.Model):
    class Initiatives:
        SOCIAL_SERVICE = 'w'
        EDUCATION = 'e'
        HEALTHCARE = 'h'
        INFRASTRUCTURE = 'i'
        EMERGENCY_RESPONSE = "r"

        CHOICES = (
            (SOCIAL_SERVICE, "Social Service"),
            (EDUCATION, "Education"),
            (HEALTHCARE, "Healthcare"),
            (INFRASTRUCTURE, "Infrastructure"),
            (EMERGENCY_RESPONSE, "Emergency Response")

        )

    initiative = models.CharField(choices=Initiatives.CHOICES, max_length=10)
    name = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField()

    def __str__(self):
        return self.name


class ServiceImage(models.Model):
    image = models.ImageField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE)


class Location(models.Model):
    name = models.CharField(max_length=255)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    longitude = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Rating(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    rating = models.DecimalField(max_digits=1, decimal_places=0)
    review = models.TextField()

    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.email

    @staticmethod
    def create_rating(request):
        rating = Rating(
            name=request.POST['name'],
            email=request.POST['email'],
            rating=request.POST['rating'],
            review=request.POST['review']
        )
        rating.save()
        return rating


class Notifications(models.Model):
    date = models.DateTimeField()
    title = models.CharField(max_length=50)
    text = models.CharField(max_length=500)
    url = models.URLField()

    def __str__(self):
        return self.date.strftime(TIME_FORMAT) + " : " + self.text

    @staticmethod
    def get_latest_notifications(request):
        datetime = request.POST['datetime']
        datetime.strptime(datetime, TIME_FORMAT)
        return Notifications.objects.filter(date__gte=datetime)

    @staticmethod
    def get_latest_notifications(length=10):
        return Notifications.objects.all().order_by('-date')[:length]
