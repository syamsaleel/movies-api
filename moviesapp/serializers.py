from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Movie
from rest_framework.exceptions import ValidationError
from datetime import date, timedelta



GENRE_CHOICES = ["Action", "Drama", "Comedy", "Thriller", "Sci-Fi"]

class MovieSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        max_length=100,
        min_length=2,
        validators=[UniqueValidator(queryset=Movie.objects.all())]
    )
    release_date = serializers.DateField()
    genre = serializers.ChoiceField(choices=GENRE_CHOICES)
    duration_minutes = serializers.IntegerField()
    rating = serializers.FloatField(min_value=0.0, max_value=10.0, required=False)

    def validate_title(self,data):
        prefix = "Movie - "
        if not data.startswith(prefix):
            raise ValidationError(
                f"The title must start with '{prefix}'"
            )
        title_text = data[len(prefix):] 
        if len(title_text) < 2 or len(title_text) > 100:
            raise ValidationError("Titile must be : between ")
        return data
    
    
    def validate_release_date (self,data):
        if data is not None:
            if data > date.today():
                raise ValidationError("Release date cannot be a future date")
            if data <date.today()- timedelta(days=30*365) :
                raise ValidationError("Release date should be within the last 30 years")
        return data
    
    def validate_genre(self,data):
        GENRE_CHOICES = ["Action", "Drama", "Comedy", "Thriller", "Sci-Fi"]
        if data not in GENRE_CHOICES:
            raise serializers.ValidationError("Invalid genre choice!.you must be enter-Action, Drama, Comedy, Thriller, Sci-Fi")
        return data
    
    def validate_duration_minutes(self, data):
        if data < 1 or data > 600:
            raise ValidationError("Duration must be between 1 and 600 minutes")
        return data
    
    def validate_rating(self, data):
        if data is not None and (data < 0.0 or data> 10.0):
            raise ValidationError("Rating must be between 0.0 and 10.0")
        return data
    

    class Meta:
        model = Movie
        fields = '__all__'
        # exclude =["titile"]
