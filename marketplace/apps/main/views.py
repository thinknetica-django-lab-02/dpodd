from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


from apps.main.models import Goods, Tag
from apps.main.forms import AddItemOfGoodsForm, EditItemOfGoodsForm


class IndexView(View):
    """A view for an index page of the site."""
    def get(self, request, *args, **kwargs):
        turn_on_block = True
        return render(request, 'index.html', {'turn_on_block': turn_on_block})


class GoodsItemsList(ListView):
    """A view for listing items of goods at `/goods/`.
    Supports chaining tags: `/goods/?tag=New&tag=Hot` will show items that have both tags `New` and `Hot`."""
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
        """Filters items in the queryset which have all of the tags in `tag_name_list`."""
        tag_queries = [Q(tags__name=tag) for tag in tag_names_list]

        for tag_query in tag_queries:
            queryset = queryset.filter(tag_query)
        return queryset

    def get_queryset(self):
        queryset = super().get_queryset()

        tag_names_list = self.request.GET.getlist("tag")
        queryset = self.filter_queryset_by_tags(queryset, tag_names_list)
        return queryset


class GoodsDetailView(DetailView):
    """A detail view for an item of goods."""
    model = Goods
    template_name = 'main/goods_detail.html'

    def get_object(self, queryset=None):
        return Goods.objects.get(slug=self.kwargs.get("slug"))


class AddItemOfGoodsView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Goods
    form_class = AddItemOfGoodsForm
    permission_required = 'main.add_goods'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.seller = self.request.user
        instance.save()
        return super().form_valid(form)


class EditItemOfGoodsView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Goods
    form_class = EditItemOfGoodsForm
    template_name = "main/edit_goods.html"
    permission_required = 'main.change_goods'

    def dispatch(self, request, *args, **kwargs):
        """Override to assure that only owner can edit an item of goods."""
        obj = self.get_object()
        if obj.seller != request.user:
            return redirect(obj)
        return super().dispatch(request, *args, **kwargs)
