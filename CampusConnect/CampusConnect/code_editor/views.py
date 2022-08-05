from django.shortcuts import render, HttpResponse, redirect
import requests
import json
# Create your views here.


def editor(request):
    return render(request,'code/code_editor.html')


def code(request):
    if request.method == "POST":
        language = request.POST['']
        code = {
            "code": "kkk",
            "language": "python",
            "input": ""

        }
        code_data = json.dumps(code)
        url = "https://codexweb.netlify.app/.netlify/functions/enforceCode"
        response = requests.post(url, data=code_data, headers={"Content-type": "application/json"}).json()
        return render(request,'code/code_editor.html',{'output':response})
