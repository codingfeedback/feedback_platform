from rest_framework import mixins, viewsets

from .models import User
from .serializers import PublicUserSerializer, UserCreateSerializer


class UserViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.order_by("-date_joined")

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return PublicUserSerializer
