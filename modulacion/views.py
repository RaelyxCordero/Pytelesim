from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .FM.ModulacionFM import ModulacionFM


from matplotlib import *
from scipy import *
import random
import django
import datetime

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter

from django import forms


# Create your views here.
class ViewModulacionFM(View):
    def get(self, request):

        obj = ModulacionFM()


        # fig = Figure()
        # ax = fig.add_subplot(111)
        # x = []
        # y = []
        # now = datetime.datetime.now()
        # delta = datetime.timedelta(days=1)
        # for i in range(10):
        #     x.append(now)
        #     now += delta
        #     y.append(random.randint(0, 1000))
        # ax.plot_date(x, y, '-')
        # ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
        # fig.autofmt_xdate()
        # canvas = FigureCanvas(fig)
        # response = django.http.HttpResponse(content_type='image/png')
        # canvas.print_png(response)

        #name = forms.CharField()
        #name = forms.TextInput(attrs={'size': 10, 'title': 'Your name', })
        #name.render('name', 'A name')


        return response