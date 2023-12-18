from django.views.generic import DetailView
from datetime import datetime
from django.views.generic import ListView
from .models import Product, Category
from .filters import ProductFilter
from .forms import ProductForm


class Products(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    ordering = ['-price']
    paginate_by = 1
    form_class = ProductForm  # добавляем форм класс, чтобы получать доступ к форме через метод POST

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ProductFilter(self.request.GET, queryset=self.get_queryset())

        context['categories'] = Category.objects.all()
        context['form'] = ProductForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса

        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новый товар
            form.save()

        return super().get(request, *args, **kwargs)
class ProductDetail(DetailView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product'

class ProductsList(ListView):
    model = Product
    ordering = 'name'
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = "Распродажа в среду!"
        return context