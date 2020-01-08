from django.db import models
import re


class SClist(models.Model):
    name = models.CharField(max_length=44)
    number = models.IntegerField()
    info = models.CharField(max_length=88000)


class Metadata(models.Model):
    type = models.CharField(max_length=8)
    value = models.CharField(max_length=66)


class SCManager:

    def __init__(self, id):
        self.scRoot = Metadata.objects.filter(type="ROOT").values("value")
        self.scRoot = self.scRoot[0].get('value')
        self.id = id
        self.sticker = SClist.objects.filter(name=self.id)
        self.stickerSet = re.split("<option", self.sticker[0].info)
        self.ln = self.sticker[0].number
        self.size = Metadata.objects.filter(type="SIZE")
        self.size = int(self.size[0].value)


    def getListNumber(self):
        return self.ln


    def getListSize(self):
        return self.size


    def getListbyTimeframe(self, tf):

        params = []
        stickers = []
        rePattern = "\w:" + re.escape(tf)

        for s in self.stickerSet:
            try:
                if re.search(rePattern, s, re.IGNORECASE):
                    str = re.search("'s=(.+)'", s).group(1)
                    params.append(str)
                    str = re.search(">(.*)<", s).group(1)
                    stickers.append(str)
            except AttributeError:
                continue

        sclist = zip(stickers, params)
        return sclist



    def getList(self):
        sclist = []
        params = []
        stickers = []
        psticker = ''

        for s in self.stickerSet:
            try:
                str = re.search(">(.*):.*<", s).group(1)
                if psticker != str:
                    if len(stickers) > 0:
                        slist = zip(stickers, params)
                        sclist.append(slist)
                        params = []
                        stickers = []

                    psticker = str

                stickers.append(psticker)
                str = re.search("'s=(.+)'", s).group(1)
                params.append(str)

            except AttributeError:
                if len(stickers) > 0:
                    slist = zip(stickers, params)
                    sclist.append(self, slist)
                continue

        slist = zip(stickers, params)
        sclist.append(slist)
        return sclist


