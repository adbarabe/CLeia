from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from bygroup.models import SClist, SCManager
import os


def index(request):
    lists = SClist.objects.all()
    return render(request, 'bystock/index.html', {'lists': lists})


def lists(request):
    listName = request.GET.get('id')

    mgr = SCManager(listName)
    masterList = list(mgr.getList())

    if id:
        message = 'Completed %r' % request.GET['id']
        message += ' : Total = ' + str(len(masterList))

    else:
        message = 'Missing parameter'


    for item in masterList:

        sclist = list(item)
        stickerList = sclist[0]
        sticker = stickerList[0]
        print("**********")
        print(stickerList)
        print("**********")

        path = mgr.scRoot + "/" + listName
        if not os.path.exists(path):
            try:
                os.mkdir(path)
            except OSError:
                print("Creation of the directory %s failed" % path)
            else:
                print("Successfully created the directory %s " % path)
        filename = path + "/" + sticker + ".html"
        context = {'ln': mgr.getListNumber, 'sticker': sticker, 'sclist': sclist}
        content = render_to_string('bystock/bySticker.html', context)
        with open(filename, 'w') as static_file:
            static_file.write(content)

    return render(request, 'success.html',
           {'message': message})



