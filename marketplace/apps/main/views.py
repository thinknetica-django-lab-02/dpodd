from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Goods, Tag
from .forms import AddItemOfGoodsForm, EditItemOfGoodsForm


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
        context['tag_list'] = Tag.objects.all()
        context['request_tags'] = self.request.GET.getlist('tag')

        return context

    @staticmethod
    def filter_queryset_by_tags(queryset, tag_names_list):
        """Filters items in the queryset which have all of the tags in `tag_name_list`"""
        q_list = [Q(tags__name=tag) for tag in tag_names_list]

        for q in q_list:
            queryset = queryset.filter(q)
        return queryset

    def get_queryset(self):
        queryset = super().get_queryset()

        tag_names_list = self.request.GET.getlist("tag")
        queryset = self.filter_queryset_by_tags(queryset, tag_names_list)
        return queryset


class GoodsDetailView(DetailView):
    model = Goods
    template_name = 'main/goods_detail.html'


class AddItemOfGoodsView(LoginRequiredMixin, CreateView):
    model = Goods
    form_class = AddItemOfGoodsForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.seller = self.request.user
        instance.save()
        return super().form_valid(form)


class EditItemOfGoodsView(LoginRequiredMixin, UpdateView):
    model = Goods
    form_class = EditItemOfGoodsForm
    template_name = "main/edit_goods.html"

    def dispatch(self, request, *args, **kwargs):
        """Override to assure that only owner can edit an item of goods."""
        obj = self.get_object()
        if obj.seller != request.user:
            return redirect(obj)
        return super().dispatch(request, *args, **kwargs)
