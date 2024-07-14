import json
from django.shortcuts import render
from django.http import HttpResponse
"""
esempio slides
def paramsToJson(request):
    if request.method== "GET":
        params= request.GET
    else:
        params= request.POST
    o = {}
    for n in params.dict().keys():
        o[n] = params.get(n)
        res = HttpResponse(content_type="application/json")
        res.write(json.dumps(o))
        return res
"""
   
"""
utilizzo sessioni (potrebbero servirci in futuro) 
def StartSession(request):
    res = HttpResponse(content_type="text/html")
    counter= request.session.get("counter")
    if counter== None:
        request.session["counter"] = 1
        res.write("Session Started")
    else:
        res.write("Session alreadystarted")
    return res

def CloseSession(request):
    res = HttpResponse(content_type="text/html")
    counter= request.session.get("counter")
    if counter!= None:
        del request.session["counter"]
        res.write("Session stopped")
    else:
        res.write("Session notstarted")
    return res

def SessionCount(request):
    res = HttpResponse(content_type="text/html")
    counter= request.session.get("counter")
    if counter== None:
        res.write("No session activated")
    else:
        counter+=1;
        res.write("Counteris{}".format(counter))
        request.session["counter"]=counter;
    return res
"""

def home(request):
    return render(request, '../Templates/index.html')   #mando richiesta (contesto) del template che voglio chiamare

def contrattoTelefonico(request):
    return render(request, '../Templates/contrattoTelefonico.html')

def sim(request):
    return render(request, '../Templates/sim.html')

def telefonata(request):
    return render(request, '../Templates/telefonata.html')
