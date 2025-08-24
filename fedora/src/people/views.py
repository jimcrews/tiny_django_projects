from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Person
from .serializers import PersonSerializer


def test_view(request):
    html = """
        <html>
            <head><title>Simple Page</title></head>
            <body>
                <h1>Hello from Django!</h1>
                <p>This is a simple HTML response.</p>
            </body>
        </html>
    """
    return HttpResponse(html)

@api_view(["Get"])
def list_people(request):
    people = Person.objects.all()
    serializer = PersonSerializer(people, many=True)
    content = {
        "people": serializer.data,
    }
    
    return Response(content)