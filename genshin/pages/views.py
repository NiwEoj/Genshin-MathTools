from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import render
from models.weapon.models import Weapon
from models.character.models import Character
from django.forms import Form
from django.core import serializers


# builder page
def builder_view(request):

    if request.method == "GET" and "id" in request.GET:
        selected_character = Character.objects.filter(id=request.GET.get("id", None))
    
    else:
        selected_character = Character.objects.filter(id=1)

    selected_weapon = serializers.serialize("json", Weapon.objects.filter(type=selected_character.values_list("user", flat=True).first()).all()[:1])

    context = {
        "selected_character": serializers.serialize("json", selected_character),
        "selected_weapon": selected_weapon
    }

    return render(request, "content/builder/main.html", context)

def weapon(request):
    selected_weapon = serializers.serialize("json", Weapon.objects.filter(id=request.GET.get("id", None)))

    context = {
        "selected_weapon": selected_weapon
    }

    return render(request, "content/builder/weaponStats.html", context)


def get_characters(request):
    characters = Character.objects.values_list("id", "name", "pic")

    return JsonResponse({"characters": list(characters)})

def get_weapons(request):
    weapons = Weapon.objects.filter(type=request.GET.get("type", None)).values_list("id", "name", "pic")

    return JsonResponse({"weapons": list(weapons)})


# builds suggestions
def builds_view(request, *args, **kwargs):
    print(request)
    if request.method == "GET" and 'character' in request.GET:
        form = Form(request.GET)
        if form.is_valid():
            selected_char = Character.objects.get(id=form.data['character'])
    else:
        selected_char = Character.objects.get(id=1)

    characters = Character.objects.all();
    weaponTypes = ["Sword", "Claymore", "Polearm", "Bow", "Catalyst"]

    context = {
        "characters": characters,
        "selected_char": selected_char,
        "weaponTypes": weaponTypes
    }

    return render(request, "content/builds/main.html", context)