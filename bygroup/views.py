from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from .models import SClist, SCManager
import string
import os


def index(request):
    lists = SClist.objects.all()
    return render(request, 'bygroup/index.html', {'lists': lists})


def lists(request):

    id = request.GET.get('id')
    type = request.GET.get('type')
    time_frame = request.GET.get('tf').split(',')

    mgr = SCManager(id, type)
    dir_path = mgr.scRoot + "/plain-html/" + id + "/"
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

    for tf in time_frame:
        path = dir_path + tf
        sclist = createList(id, type, tf, path)

    sclist = mgr.getListbyTimeframe(tf)
    total = len(list(sclist))
    if id:
        message = 'Completed %r' % id
        message += ' : Total = ' + str(total)

    else:
        message = 'Missing parameter'

    # TODO
    sclist = mgr.getListbyTimeframe(tf)
    return render(request, 'bygroup/success.html',
                  {'message': message, 'path': path, 'sclist': sclist})


def createList(id, type, tf, path):

    mgr = SCManager(id, type)
    rsclist = list(mgr.getListbyTimeframe(tf))
    fileidx = list(string.ascii_lowercase)

    # Break a list into chunks of size N
    n = 1
    rsclist = [rsclist[i * mgr.getListSize():(i + 1) * mgr.getListSize()]
               for i in range((len(rsclist) + mgr.getListSize() - 1) // mgr.getListSize())]
    if len(rsclist) < mgr.getListSize():
        doFraction = True
    else:
        doFraction = False

    for lst in rsclist:
        context = {'ln': mgr.getListNumber, 'sclist': lst}
        content = render_to_string('bygroup/byTimeframe.html', context)
        if doFraction:
            filename = path + fileidx[n - 1] + ".html"
        else:
            filename = path + ".html"

        with open(filename, 'w') as static_file:
            static_file.write(content)
        n += 1

    return mgr.getListbyTimeframe(tf)
