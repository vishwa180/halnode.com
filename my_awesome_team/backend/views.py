from rest_framework import parsers, renderers, permissions, authentication, views, status
from rest_framework.response import Response
from django.db import IntegrityError
from ..models import Project, Entry
from ..functions import get_date_time
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import CursorPagination


class MyPagination(CursorPagination):
    page_size = 10
    ordering = '-created_at'


@api_view(['POST'])
@permission_classes([AllowAny])
def obtain_auth_token(request):
    user = authenticate(request, username=request.data['username'], password=request.data['password'])
    if user:
        token = Token.objects.get_or_create(user=user)[0]
        data = {
            "user": user.username,
            "full_name": user.get_full_name(),
            "token": str(token)
        }
        return Response(status=status.HTTP_200_OK, data=data)
    return Response(status=status.HTTP_400_BAD_REQUEST, data={"messages": ["Invalid Credentials"]})


@api_view(['GET'])
@permission_classes([AllowAny])
def auth_load_user(request):
    if request.user.is_authenticated:
        data = {
            "user": request.user.username,
            "full_name": request.user.get_full_name(),
        }
        return Response(status=status.HTTP_200_OK, data=data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CSRFExemptSessionAuth(authentication.SessionAuthentication):

    def enforce_csrf(self, request):
        pass


class JSONApi(views.APIView):
    authentication_classes = (authentication.TokenAuthentication, CSRFExemptSessionAuth,)
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = (renderers.JSONRenderer,)
    parser_classes = (parsers.JSONParser,)


class GetProjects(JSONApi):
    @staticmethod
    def get(request):
        return Response(data={"projects": list(Project.objects.filter(is_active=True).values("id", "name"))})


class EntryView(JSONApi):
    @staticmethod
    def post(request):
        try:
            data = request.data
            data["created_by_id"] = request.user.id
            tagged_users = list()
            if "tagged_users" in data:
                tagged_users = data.pop("tagged_users")
            entry = Entry(**data)
            entry.save()
            if len(tagged_users) > 0:
                for tagged_user_id in tagged_users:
                    entry.tagged_users.add(tagged_user_id)
            return Response(data={"id": entry.id})
        except IntegrityError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(e)})

    @staticmethod
    def get(request):
        from_date = request.GET["from"]
        to_date = request.GET["to"]

        entries = list(Entry.objects.filter(created_date__range=(get_date_time(from_date),
                                                                 get_date_time(to_date, start=False)))
                       .values("id", "title", "created_by", "type", "created_at"))

        return Response(data={"entries": entries})
