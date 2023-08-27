from django.shortcuts import render
from .models import Advertisement
from .forms import AdvertisementForm
from django.urls import reverse
from django.shortcuts import redirect
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from django.contrib.auth import get_user_model
from django.db.models import Count

User = get_user_model()

def example(request):
    # введем обработку параметров GET запроса
    # request.GET -> получаем словарь и в этом словаре ищем ключ "query"
    # по значению ключа производим фильтрацию
    title = request.GET.get("query")
    if title:
        advertisements = Advertisement.objects.filter(title__icontains=title)
    else:
        advertisements = Advertisement.objects.all()
    context = {
        "advertisements": advertisements,
        "title": title
    }
    return render(request, "app_advertisements/index.html", context)

def top_sellers(request):
    users = User.objects.annotate(adv_count=Count('advertisement')).order_by("-adv_count")
    context = {
        'users': users
    }
    return render(request, "app_advertisements/top-sellers.html", context)

@login_required(login_url=reverse_lazy("login"))
def advertisement_post(request):
    # если пришел запрос на добавление
    if request.method == "POST":
        # заполняем форму введенной ифнормацией
        form = AdvertisementForm(request.POST, request.FILES)
        # делаем проверку на правильность заполнения
        if form.is_valid():
            # создаем новый объект для добавления в БД
            advertisement = Advertisement(**form.cleaned_data)
            # т.к. пользователя не вводили в форме, то получим его из запроса
            advertisement.user = request.user
            # отсюда вывод - формы смогут заполнять только залогиненные пользователи
            # пока логина нету - может заполнять админ (входим под админкой)
            advertisement.save()
            url = reverse("main-page")
            return redirect(url)
    else:
        # при загрузке страницы создаем новую пустую форму
        form = AdvertisementForm()
        # передаем ее через контекст
    context = {'form': form}
    return render(request, "app_advertisements/advertisement-post.html", context)

def advertisement_detail(request, pk):
    advertisement = Advertisement.objects.get(id=pk)
    context = {
        'advertisement': advertisement
        }
    return render(request, 'app_advertisements/advertisement.html', context)