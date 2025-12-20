from rest_framework import serializers
from .models import Movie


# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(label="Movie ID", required=False)
#     title = serializers.CharField(max_length=255)
#     genres = serializers.ListField(
#         child=serializers.CharField(max_length=100), allow_empty=True, default=list
#     )

#     def create(self, validated_data):
#         """
#         Create and return a new `Movie` instance, given the validated data.
#         """
#         return Movie.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         """
#         Given the validated data, update and return an existing `Movie` instance.
#         """
#         instance.title = validated_data.get("title", instance.title)
#         instance.genres = validated_data.get("genres", instance.genres)
#         instance.save()
#         return instance

# Note that model has default values for genres and year attribute.
# So when the put method used upon one movie entity with omitted genres and year attribute in the json
# the serializer nevertheless validated this json.
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["id", "title", "genres", "year"]
