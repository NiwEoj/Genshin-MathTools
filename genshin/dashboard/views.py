from django.http import HttpResponse
from django.shortcuts import render

# main page
def main_view(request, *args, **kwargs):
    context = {
        "title": "testing 234",
        "number": 3423
    }
    return render(request, "content/main.html", context)