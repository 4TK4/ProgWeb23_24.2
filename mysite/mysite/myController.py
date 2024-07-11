import json
from django.shortcuts import render
from django.http import HttpResponse
def index(request):
    output1 = "<html> <body>"
    output2 = "<p>Welcome to DJANGO</p>"
    output3 = "</body> </html>"
    return HttpResponse(output1 + output2 + output3)
def index2(request):
    response= HttpResponse(
    content_type="text/html")
    response.write("<html> <body>")
    response.write("<p>Welcome to DJANGO again</p>")
    response.write("</body> </html>")
    return response
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