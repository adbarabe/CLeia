from django.db import models
from requests_html import HTML
import re
from django.template.defaultfilters import first


class SClist(models.Model):
    name = models.CharField(max_length=44)
    number = models.IntegerField()
    #info = models.CharField(max_length=88000)


class Metadata(models.Model):
    type = models.CharField(max_length=8)
    value = models.CharField(max_length=66)


class SCManager:

    def __init__(self, id, type="NONE"):
        self.scRoot = Metadata.objects.filter(type="ROOT").values("value")
        self.scRoot = self.scRoot[0].get('value')
        self.id = id
        self.sticker = SClist.objects.filter(name=self.id)
        #self.stickerSet = re.split("<option", self.sticker[0].info)
        self.ln = self.sticker[0].number
        self.size = Metadata.objects.filter(type="SIZE")
        self.size = int(self.size[0].value)

        if type == 'plain':

            filename = self.scRoot + "/plain-src/" + self.id + '.html'
            with open(filename) as html_file:
                source = html_file.read()
                html = HTML(html=source)

            select = html.find('#favoritesLoad', first=True)
            options = select.find('option')

            self.stickerSet = []
            for o in options:
                if 'Your Saved Charts' in o.text:
                    continue

                re_en = re.compile("&en=[0-9-]*")
                o.attrs['value'] = re_en.sub("", o.attrs['value'])
                self.stickerSet.append(o)

        elif type == 'sorted':
            filename = self.scRoot + "/sorted-src/" + id + '.html'
            with open(filename) as html_file:
                source = html_file.read()
                html = HTML(html=source)

            div = html.find('#summaryTable_wrapper', first=True)

            # Calculate time period
            select_period = div.find('#select_period', first=True)
            period = select_period.find('option')
            selected = period[0].find('option:checked')

            self.selected = ''
            for p in period:
                if 'selected' in p.attrs:
                    self.selected = p.attrs['name']

            # Extract data rows
            table = div.find('#summaryTable', first=True)
            self.stickerSet = table.find('tbody > tr')

    def getListNumber(self):
        return self.ln

    def getListSize(self):
        return self.size

    def getListbyTimeframe(self, tf):

        params = []
        stickers = []
        if tf == "X15":
            rePattern = ".*"
        else:
            rePattern = "\w:" + re.escape(tf)

        print("********&")
        print(self.stickerSet)
        print("********")

        for s in self.stickerSet:

            atts = s.attrs
            try:
                if re.search(rePattern, s.text, re.IGNORECASE):
                    atts = s.attrs
                    params.append(atts['value'])
                    stickers.append(s.text)

            except AttributeError:
                continue

        # self.__printList(self.getListbyTimeframe.__name__ + " stickers",
        #                 stickers)
        # self.__printList(self.getListbyTimeframe.__name__ + " params",
        #                 params)
        sclist = zip(stickers, params)
        return sclist

    def getList(self):
        sclist = []
        params = []
        stickers = []
        psticker = ''

        print("********")
        print(self.stickerSet)
        print("********")

        for s in self.stickerSet:

            try:
                sticker = s.text
                if re.search("\*", sticker):
                    continue

                str = re.search("(.*):.*", sticker).group(1)
                if psticker != str:
                    if len(stickers) > 0:
                        slist = zip(stickers, params)
                        sclist.append(slist)
                        params = []
                        stickers = []

                    psticker = str

                stickers.append(psticker)

                # TODO
                #atts = s.attrs
                #re_en = re.compile("&en=[0-9-]*")
                #param = re_en.sub("", atts['value'])
                #print("iiiiii " + param)
                params.append(s.attrs['value'])

            except AttributeError:
                if len(stickers) > 0:
                    slist = zip(stickers, params)
                    sclist.append(self, slist)
                continue

        self.__printList(self.getList.__name__,
                         zip(stickers, params))
        slist = zip(stickers, params)
        sclist.append(slist)
        return sclist

    def getListSymbols(self):
        sclist = []
        stickers = []
        psticker = ''

        print("********")
        print("getListSymbols -->")
        print(self.stickerSet)
        print("********")

        for s in self.stickerSet:

            sticker = s.text
            str = re.search("(.*):.*", sticker).group(1)
            if psticker != str:
                psticker = str
                sclist.append(psticker)

        self.__printList(self.getListSymbols.__name__, sclist)
        return sclist

    def getSortedListbyTimeframe(self, tf):

        params = []
        stickers = []
        stickerSymbols = []
        for row in self.stickerSet:
            col = row.find('td')

            symbol = col[1].find('span')[0].text
            a = col[2].find('a')
            sticker = a[0].text
            print(sticker + '######   ' + tf)
            if tf not in sticker:
                continue

            param = col[2].xpath('//a/@href')[0][11:]

            priceChange = col[4].find('span')[0].text
            percentageChange = col[5].find('span')[0].text
            time = col[7].find('span')[0].text

            stickerSymbols.append(symbol)
            stickers.append('{}{}{}{}{}'.format(sticker.ljust(20),
                                                priceChange.ljust(20),
                                                percentageChange.ljust(10),
                                                self.selected[0:5].ljust(10),
                                                time))
            params.append(param)

        self.__printList(self.getSortedListbyTimeframe.__name__,
                         zip(stickers, params))
        sclist = zip(stickerSymbols, stickers, params)
        return sclist

    def __printList(self, methodName, list):

        print('Begin = DEBUG models.py: ' + methodName)
        for i in list:
            print(i)
        print('End = DEBUG models.py: ' + methodName)
