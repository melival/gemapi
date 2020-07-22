from .models import Deals
from . import helpers
from rest_framework import mixins, generics, permissions, views
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.settings import api_settings


class DealsUploadView(views.APIView):
    parser_classes = (FileUploadParser, )

    def post(self, request, filename="filename", format="csv"):
        if 'file' not in request.data:
            return Response({'status': "Error", 'desc': "No file"})

        file = request.data['file']
        print("File recieved")
        csv_decoded = file.read().decode('utf-8')

        return Response(helpers.upload_from_csv(csv_decoded, Deals))


class DealsGetView(views.APIView):

    def get(self, request):
        print("requested:", request.data)
        deals = Deals.objects.all()
        return Response(helpers.get_data(Deals))
