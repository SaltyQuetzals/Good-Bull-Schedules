from rest_framework import renderers, response, views, permissions
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import redirect, render


def register(request):
    if request.method == "POST":
        f = UserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, "Account created successfully.")
            return redirect("/")
    else:
        f = UserCreationForm()
    return render(request, "register.html", {"form": f})


class IndexView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [renderers.TemplateHTMLRenderer]

    def get(self, request):
        return response.Response(template_name="index.html")
