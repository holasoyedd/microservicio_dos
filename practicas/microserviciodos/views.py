from django.shortcuts import render
from .models import Usuarios
from django.contrib.auth.hashers import make_password, check_password
from uuid import uuid4

from django.http import (Http404, HttpResponse, HttpResponseNotAllowed,
                        HttpResponseNotFound, HttpResponseRedirect,
                        HttpResponseServerError, JsonResponse, request)

from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def users(request, username = '', password = ''):
    if request.method == 'POST':
        my_json = request.body.decode('utf8').replace("'", '"')
        data = json.loads(my_json)

        if data["nombre"] != "" and data["edad"] != "" and data["nombreUsuario"] != "" and data["contrasenia"] != "":

            respuestaExiste = None
            respuestaExiste = Usuarios.objects.filter(nombreUsuario=data['nombreUsuario']).exists()

            if respuestaExiste:
                return HttpResponse('Nombre de usuario existente', status=400) #si el no usuario existe

            newUsuario = Usuarios()
            newUsuario.nombre = data["nombre"]
            newUsuario.edad = data["edad"]
            newUsuario.nombreUsuario = data["nombreUsuario"]
            newUsuario.contrasenia = make_password(data["contrasenia"])

            newUsuario.save()

            rand_token = uuid4()

            data_set = {
                "id": newUsuario.usuarioId, 
                "name": newUsuario.nombre,
                "age": newUsuario.edad,
                "token": str(rand_token)
            }

            return HttpResponse(json.dumps(data_set), content_type="application/json")
         
        return HttpResponse("Error al completar los datos", status=400)

    elif request.method == 'GET':

        respuestaExiste = None
        respuestaExiste = Usuarios.objects.filter(nombreUsuario=username).exists()

        if respuestaExiste == False:
            return HttpResponse('Nombre de usuario existente', status=400) #si el no usuario existe

        usuarioData = Usuarios.objects.filter(nombreUsuario=username).get()


        if check_password(password, usuarioData.contrasenia) == False:
            return HttpResponse('Contrasenia incorrecta', status=400) #si el no usuario existe

        rand_token = uuid4()

        data_set = {
            "id": usuarioData.usuarioId, 
            "name": usuarioData.nombre,
            "age": usuarioData.edad,
            "token": str(rand_token)
        }

        return HttpResponse(json.dumps(data_set), content_type="application/json")
    else:
        return HttpResponseNotAllowed('')