from django.shortcuts import render
from django.views.generic import View


class IndexView(View):
    def get(self, request, *args, **kwargs):
        turn_on_block = True
        return render(request, 'index.html', {'turn_on_block': turn_on_block})
