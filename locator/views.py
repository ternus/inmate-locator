# Create your views here.


from django.http import HttpResponse
from django.utils import simplejson
from locate import *

def inmatelookup(request):
    print request.GET.get("id")
    result = AZsearch(request.GET.get("id"))
    if not result:
        raise Http404
    ret = simplejson.dumps(result, default=encode_inmate)
    return HttpResponse(ret, mimetype='application/json')
