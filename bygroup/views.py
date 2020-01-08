from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from .models import SClist, SCManager
import string


def index(request):
    lists = SClist.objects.all()
    return render(request, 'index.html', {'lists': lists})


def lists(request):
    id = request.GET.get('id')
    tf = request.GET.get('tf')

    mgr = SCManager(id)
    rsclist = list(mgr.getListbyTimeframe(tf))

    fileidx = list(string.ascii_lowercase)

    #Break a list into chunks of size N
    n = 1;
    rsclist = [rsclist[i * mgr.getListSize():(i + 1) * mgr.getListSize()]
               for i in range((len(rsclist) + mgr.getListSize() - 1) // mgr.getListSize())]

    for lst in rsclist:
        context = {'ln': mgr.getListNumber, 'sclist': lst}
        content = render_to_string('byTimeframe.html', context)
        filename = mgr.scRoot + "/" + id + "/" + tf + fileidx[n-1] + ".html"
        with open(filename, 'w') as static_file:
            static_file.write(content)
        n += 1

    #sclist = mgr.getListbySticker("DIA")
    sclist = mgr.getListbyTimeframe(tf)

    if id:
        message = 'Completed %r' % request.GET['id']
        message += ' : Total = ' + str(len(list(sclist)))

    else:
        message = 'Missing parameter'

    sclist = mgr.getListbyTimeframe(tf)
    return render(request, 'success.html',
           {'message': message, 'sclist': sclist})









