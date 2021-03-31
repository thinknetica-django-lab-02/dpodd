from django.shortcuts import render
from django.views.generic import View, ListView, DetailView

from .models import Goods, Tag


class IndexView(View):
    def get(self, request, *args, **kwargs):
        turn_on_block = True
        return render(request, 'index.html', {'turn_on_block': turn_on_block})


class GoodsItemsList(ListView):
    model = Goods
    paginate_by = 10
    template_name = 'main/goods_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags_list'] = Tag.objects.all()

        return context


class GoodsDetailView(DetailView):
    model = Goods
    template_name = 'main/goods_detail.html'
