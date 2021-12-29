from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from accounts.api.serializers import (
    UserSerializer,
    LoginSerializer,
    SignupSerializer,
)
from django.contrib.auth import (
    login as django_login,
    logout as django_logout,
    authenticate as django_authenticate,
)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class AccountViewSet(viewsets.ViewSet):
    serializer_class = SignupSerializer

    @action(methods=['GET'], detail=False)
    def login_status(self, request):
        data = {'has_logged_in': request.user.is_authenticated}
        if request.user.is_authenticated:
            data['user'] = UserSerializer(request.user).data
        return Response(data)

    @action(methods=['POST'], detail=False)
    def logout(self, request):
        django_logout(request)
        return Response({'success': True})

    @action(methods=['POST'], detail=False)
    def login(self, request):
        # get username and password from request
        serializer = LoginSerializer(data=request.data)
        # check if the username and password input is valid
        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Please Check Input",
                "errors": serializer.errors,
            }, status=400)

        # username and password input is validated, try to log in
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        # check if the username exists
        if not User.objects.filter(username=username).exists():
            return Response({
                "success": False,
                "message": "username does not exist",
            }, status=400)

        user = django_authenticate(request, username=username, password=password)
        # if the username and password combination is incorrect
        if not user or user.is_anonymous:
            return Response({
                "success": False,
                "message": "username and password does not match",
            }, status=400)
        django_login(request, user)
        # the default status is 200
        return Response({
            "success": True,
            "user": UserSerializer(instance=user).data,
        })

    @action(methods=['POST'], detail=False)
    def signup(self, request):
        # validate the username, email and password
        serializer = SignupSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Please Check Input",
                "errors": serializer.errors,
            }, status=400)

        # create the user if validated
        user = serializer.save()

        # login automatically after signup
        django_login(request, user)

        return Response({
            "success": True,
            "user": UserSerializer(instance=user).data,
        }, status=201)












