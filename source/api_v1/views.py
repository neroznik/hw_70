import json
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import ensure_csrf_cookie

from api_v1.serializers import ArticleSerializer
from webapp.models import Article


@ensure_csrf_cookie
def get_token_view(request, *args, **kwargs):
    if request.method == 'GET':
        return HttpResponse()
    return HttpResponseNotAllowed('Only GET request are allowed')


class ArticleListView(View):
    def get(self, request, *args, **kwargs):
        objects = Article.objects.all()
        slr = ArticleSerializer(objects, many=True)
        return JsonResponse(slr.data, safe=False)


class ArticleDetailView(View):
    def get(self, request, *args, **kwargs):
        object = Article.objects.get(pk=self.kwargs['pk'])
        slr = ArticleSerializer(object)
        return JsonResponse(slr.data, safe=False)


class ArticleCreateView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        print(data)
        slr = ArticleSerializer(data=data)
        if slr.is_valid():
            article = slr.save()
            return JsonResponse(slr.data, safe=False)
        else:
            response = JsonResponse(slr.errors, safe=False)
            response.status_code = 400
            return response


class ArticleUpdateView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        object = Article.objects.get(pk=self.kwargs['pk'])
        slr = ArticleSerializer(data=data, instance=object)
        if slr.is_valid():
            article = slr.update()
            return JsonResponse(slr.data, safe=False)
        else:
            response = JsonResponse(slr.errors, safe=False)
            response.status_code = 400
            return response


class ArticleDeleteView(View):
    def get(self, request, *args, **kwargs):
        object = Article.objects.get(pk=self.kwargs['pk'])
        object.delete()
        return JsonResponse(
            {"pk": object.pk})
