from rest_framework import serializers

from posts.models import Post, PostViews


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'body',
            'status',
            'created_on'
        )
        extra_kwargs = {'body': {'write_only': True}}
        read_only_fields = ('id', 'created_on')

    def create(self, validated_data):
        post = Post.objects.create(
            title=validated_data['title'],
            body=validated_data['body'],
            status=validated_data.get('status', Post.PostStatus.DRAFT),
            author=validated_data.get('author')
        )

        # create postViews instance
        PostViews.objects.create(post=post)

        return post

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        return instance


class PostDetailSerializer(serializers.ModelSerializer):
    views = serializers.IntegerField(source='view_count')
    author = serializers.CharField(source='author.username')

    class Meta:
        model = Post
        exclude = ('id',)