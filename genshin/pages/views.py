from django.http import HttpResponse
from django.shortcuts import render
from models.weapon.models import Weapon
from models.character.models import Character
from django.forms import Form


# builder page
def builder_view(request, *args, **kwargs):

    characters = Character.objects.all();

    if request.method == "GET" and 'character' in request.GET:
        form = Form(request.GET)
        if form.is_valid():
            selected_char = Character.objects.get(id=form.data['character'])
    else:
        selected_char = Character.objects.get(id=1)

    weapon = Weapon.objects.filter(type=selected_char.user)

    context = {
        "characters": characters,
        "selected_char": selected_char,
        "weapon": weapon
    }

    return render(request, "content/builder/main.html", context)


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