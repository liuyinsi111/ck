from django.shortcuts import render

from django.views.generic import View

class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')
    def post(self, request):
        pass

