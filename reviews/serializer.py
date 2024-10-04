from reviews.models import Review
from rest_framework import serializers


class ReviewsSerializer(serializers.ModelSerializer):
   

    class Meta:
            model = Review
            fields = ['id', 'user_id', 'description', 'reviewed_at',\
                       'review_updated_at', 'rating', 'rated_at', 'rate_updated_at']

    def create(self, validated_data):
        user_id = self.context['request'].user.id
        if Review.objects.filter(user_id=user_id).exists():
            raise serializers.ValidationError("A review with this user already exists.")
        validated_data['user_id'] = user_id
        return super().create(validated_data)
    