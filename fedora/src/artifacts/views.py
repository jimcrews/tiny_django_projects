from django.http import HttpResponse


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