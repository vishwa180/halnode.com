from . import models
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse
from rest_framework import status
from django.db import IntegrityError


class WebsiteAPI(APIView):
    authentication_classes = tuple()
    renderer_classes = (JSONRenderer,)
    parser_classes = (JSONParser,)


def index(request):
    return render(request, template_name='index.html')


def careers(request):
    return render(request, template_name='careers.html')


def create_contact(email, name, subject, message):
    try:
        contact = models.ContactMessage(email=email, name=name, subject=subject, message=message)
        contact.save()
        return True
    except IntegrityError:
        return False


def create_lead(email):
    try:
        lead = models.Lead(email=email)
        lead.save()
        return True
    except IntegrityError:
        return False


class ContactUs(WebsiteAPI):

    @staticmethod
    def post(request):
        done = create_contact(request.data['email'], request.data['name'], request.data['subject'],
                              request.data['message'])
        if done:
            return JsonResponse({"status": True, "description": "Message Received! We will get back to you ASAP."},
                                status=status.HTTP_200_OK)
        else:
            return JsonResponse({"status": False, "description": "Try again later!"}, status=status.HTTP_200_OK)


class CreateLead(WebsiteAPI):

    @staticmethod
    def post(request):
        done = create_lead(request.data['email'])
        if done:
            return JsonResponse({"status": True,
                                 "description": "Thank you for your interest. Our Sales Team will get back to you ASAP!"},
                                status=status.HTTP_200_OK)
        else:
            return JsonResponse({"status": False, "description": "Try again later!"}, status=status.HTTP_200_OK)
