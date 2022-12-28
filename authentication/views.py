from rest_framework import generics, status
from authentication.serializers import *
from django.contrib.auth import authenticate
from rest_framework.response import Response
from django.contrib.auth.models import update_last_login


# Create your views here.
class RegisterAPI(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class LoginAPI(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        user = authenticate(email=email, password=password)

        if user is None:
            return Response({"email": "not correct"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )

        serializer = UserSerializer(user)
        return Response(serializer.data)


class SetUserInfoAPI(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    # TODO: 해결하지 못한 것: 만약 username 이나 student_id 둘 중 하나만 입력하였을 때, is_qualified 가 제대로 업데이트되지 않음.
    def patch(self, request, *args, **kwargs):
        try:
            if request.data["username"] is None or request.data["student_id"] is None:
                return super().patch(request, *args, **kwargs)
            instance = self.get_object()
            instance.is_qualified = True
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        except KeyError:
            return super().patch(request, *args, **kwargs)
