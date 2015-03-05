from django.shortcuts import render_to_response
from django.template import RequestContext


def readme(request):
    context = RequestContext(request)
    args = {}
    return render_to_response("readme.html", args, context_instance=context)


def query(request):
    context = RequestContext(request)
    args = {}
    return render_to_response("query.html", args, context_instance=context)
