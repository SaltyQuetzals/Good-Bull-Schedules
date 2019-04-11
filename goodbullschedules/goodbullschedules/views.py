from rest_framework import renderers, response, views, permissions


class IndexView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [renderers.TemplateHTMLRenderer]

    def get(self, request):
        return response.Response(template_name="index.html")
