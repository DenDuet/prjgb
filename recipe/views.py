# import datetime
from pyexpat.errors import messages
import random
import time
from datetime import datetime, date, timedelta, time
from django.forms import Form
from django.http import HttpResponsePermanentRedirect, JsonResponse
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from recipe.models import Recipe, Category, Journal
from django.core.files.storage import FileSystemStorage
from .forms import ImageForm, RecipeForm, UserForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
# from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout

import logging

logger = logging.getLogger(__name__)


def logoutUser(request):
    '''
    Выход пользователя из системы
    '''
    logout(request)
    return redirect('login')


# def str_time_prop(start, end, time_format, prop):
#     """Get a time at a proportion of a range of two formatted times.

#     start and end should be strings specifying times formatted in the
#     given format (strftime-style), giving an interval [start, end].
#     prop specifies how a proportion of the interval to be taken after
#     start.  The returned time will be in the specified format.
#     """

#     stime = time.mktime(time.strptime(start, time_format))
#     etime = time.mktime(time.strptime(end, time_format))

#     ptime = stime + prop * (etime - stime)

#     return time.strftime(time_format, time.localtime(ptime))

# # time.strftime('%Y-%m-%d %H:%M', time.localtime(time.mktime(time.strptime( , '%Y-%m-%d %H:%M')))
#     #   datetime.today().strftime('%Y-%m-%d %H:%M')


# def random_date(start, end, prop):
#     return str_time_prop(start, end, '%Y-%m-%d %H:%M', prop)

# # print(random_date("1/1/2000 1:30 PM", "10/10/2022 4:50 AM", random.random()))


# def init_bases(request):

#     Recipe.objects.all().delete()
#     Category.objects.all().delete()
#     Journal.objects.all().delete()

#     dt = random_date("2022-10-02 11:30", "2023-10-02 14:50", random.random())
#     rec = [
#         Recipe(name="Пирог брусничный", description="Вкусный пирог из брусники и теста", steps="", add_date="",
#                image="", author="Василий", ingredients="сахар - 1 ст.л, соль - 2 ст.л, вода - 3 литра, брусника - 1 шт."),
#         Recipe(name="Пирог клюквенный", description="Вкусный пирог из клюквы и теста", steps="", add_date="",
#                image="", author="Семен", ingredients="сахар - 1 кг, соль - 0,5 ст.л, вода - 1 литр, клюква - 3 кг"),
#         Recipe(name="Суп из фрикаделек", description="Бульон из кубиков с добавлением подобия мясных шариков", steps="", add_date="",
#                image="", author="Петр", ingredients="соль - 2 ст.л, вода - 3 литра, бульонный кубик - 1 шт., фрикадельки - 12 шт."),
#         Recipe(name="Блины со сгущенкой", description="Блины со сгущенкой", steps="", add_date="", image="",
#                author="Василий", ingredients="сахар - 1 ст.л, соль - 2 ст.л, вода - 3 литра, мука - 1 кг., сгущенка - 3 литра"),
#         Recipe(name="Чай облепиховый", description="Пакетный чай с добавлением опавшей с куста облепихой", steps="", add_date="",
#                image="", author="Семен", ingredients="чай из пакетика - 1 шт., облепиха с земли - сколько соберется, сахар - по вкусу")
#     ]

#     usr = Recipe.objects.bulk_create(rec)

#     dt = random_date("2022-10-02 11:30", "2023-10-02 14:50", random.random())
#     category = [
#         Category(category_name="Супы",
#                  description="Разнообразные супы или нечто на них похожее"),
#         Category(category_name="Пироги сладкие",
#                  description="Разнообразные сладкие пироги"),
#         Category(category_name="Пироги не сладкие",
#                  description="Разнообразные не сладкие пироги"),
#         Category(category_name="Чаи", description="Чаеподобные напитки"),
#         Category(category_name="Десерты", description="Всё, что не пироги"),
#     ]

#     prod = Category.objects.bulk_create(category)

    # for i in range(50):
    #     dt = random_date("2022-10-02 11:30", "2023-10-02 14:50", random.random())
    #     print(dt)
    #     order = Orders(customer=User.objects.get(username=usr[random.randint(0,len(usr)-1)].username), total_price=200, date_ordered=dt)
    #     order.save()
    #     print(order.date_ordered)
    #     for j in range(random.randint(1,3)):
    #         order.goods.add(Goods.objects.filter(goods_name=goods[j].goods_name).first())
    # order.save()

    # return render(request, "recipe/base.html", context={"body": "index page", "title": "Главная страница"})


def index(request):
    '''Стартовая страница
    '''

    logger.info('Index page accessed')
    return render(request, "recipe/base.html", context={"body": "index page", "title": "Главная страница"})


def main_recipe(request, cat_id: int):
    '''Журнал рецептов с выбором по категориям
    '''

    rcps = Journal.objects.filter(category=cat_id)
    cats = Category.objects.all()
    cat = Category.objects.get(pk=cat_id)
    rcp = Recipe.objects.all().count
    data = datetime.now()
    # print(len(rcps))
    # len(rcps)
    logger.info(f'Распечатали список рецептов: {rcps}')
    return render(request, "recipe/main_recipe.html", context={'date': data, 'count': rcp, 'cat': cat, 'cats': cats, "recipe": rcps, "title": "Рецепты по категориям"})

# _________________CATEGORY______________________


def read_caregory(request):
    '''Выводим журнал категорий
    '''

    cat = Category.objects.all()
    return render(request, "recipe/category.html", context={"category": cat, "title": "Категории"})


@login_required
def create_category(request):
    '''Создаем категорию
    '''

    if request.method == 'POST':
        if request.POST.get('category_name') != "":
            category_name = " ".join(request.POST.get("category_name").split())
        if request.POST.get('description') != "":
            description = request.POST.get("description")

        cat = Category(category_name=category_name, description=description)
        cat.save()

        logger.info(f'Успешно создали новую категорию: {cat}.')
        cat = Category.objects.all()
        return render(request, "recipe/category.html", context={"category": cat, "title": "Категории"})
    else:
        logger.info(f'Создаем новую категорию.')

        return render(request, 'recipe/category_create.html', {"title": "Создаем категорию"})


@login_required
def edit_category(request, cat_id):
    '''Редактируем категорию и сохраняем
    '''

    if request.method == 'POST':
        cat = Category.objects.get(pk=cat_id)
        if request.POST.get('category_name') != "":
            cat.category_name = " ".join(
                request.POST.get("category_name").split())
        if request.POST.get('description') != "":
            cat.description = request.POST.get("description")

        # created = Category.objects.update_or_create(
        #     category_name=category_name, description=description)
        cat.save()
        logger.info(f'Успешно обновили категорию: {cat}.')
        cat = Category.objects.all()
        return render(request, "recipe/category.html", context={"category": cat, "title": "Категории"})
    else:
        cat = Category.objects.get(pk=cat_id)
        logger.info(f'Редактируем категорию')

        return render(request, 'recipe/category_edit.html', {'cat': cat, "title": "Создаем категорию"})


@login_required
def delete_category(request, cat_id: int):
    '''Удаляем категорию
    '''

    cat = Category.objects.get(pk=cat_id)
    cat.delete()
    cat = Category.objects.all()
    # print(name)
    logger.info(f'Удалили категорию. Автор - {request.user}')
    return render(request, "recipe/category.html", context={"category": cat, "title": "Категории"})
# _________________CATEGORY______________________


# _________________RECIPE______________________

def read_recipe(request):
    '''Выводим все рецепты в таблице
    '''

    recipe = Recipe.objects.all()
    # print(name)
    logger.info(f'Распечатали список рецептов: {recipe}')
    return render(request, "recipe/recipe.html", context={"recipe": recipe, "title": "Рецепты"})


def upload_image(image, recipe_id):
    '''Загружаем картинку рецепта
    '''

    fs = FileSystemStorage()
    filename = fs.save(image.name, image)
    file_url = fs.url(filename)
    cat = Recipe.objects.get(pk=recipe_id)
    cat.image = file_url
    cat.save()
    return file_url


@login_required
def create_recipe(request):
    '''Создаем новый рецепт и сохраняем
    '''

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)

        if request.POST.get('name') != "":
            name = " ".join(request.POST.get("name").split())
        if request.POST.get('make_time') != "":
            make_time = " ".join(request.POST.get("make_time").split())
        if request.POST.get('description') != "":
            description = request.POST.get("description")
        if request.POST.get('steps') != "":
            steps = request.POST.get("steps")
        if request.POST.get('ingredients') != "":
            ingredients = request.POST.get("ingredients")
        recipe = Recipe(name=name, description=description, make_time=make_time,
                        steps=steps, ingredients=ingredients, author=request.user)
        recipe.save()

        file_ = request.FILES.get("image", None)
        if file_ != None:
            file = request.FILES['image']
            upload_image(file, recipe.id)
        logger.info(f'Успешно создали рецепт: {recipe}.')
        recipe = Recipe.objects.all()
        return render(request, "recipe/recipe.html", context={"recipe": recipe, "title": "Рецепты"})

    else:
        form = RecipeForm()
        cat = Category.objects.order_by('category_name')

    return render(request, 'recipe/recipe_create.html', {'cat': cat, 'form': form, "title": "Создаем рецепт"})


@login_required
def edit_recipe(request, rcp_id: int):
    '''Редактируем рецепт и обновляем запись '''

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        recipe = Recipe.objects.get(pk=rcp_id)
        if request.POST.get('name') != "":
            recipe.name = " ".join(request.POST.get("name").split())
        if request.POST.get('make_time') != "":
            recipe.make_time = " ".join(request.POST.get("make_time").split())
        if request.POST.get('description') != "":
            recipe.description = request.POST.get("description")
        if request.POST.get('steps') != "":
            recipe.steps = request.POST.get("steps")
        if request.POST.get('ingredients') != "":
            recipe.ingredients = request.POST.get("ingredients")
        recipe.save()
        file_ = request.FILES.get("image", None)
        if file_ != None:
            file = request.FILES['image']
            upload_image(file, recipe.id)
        print(f"file_ = {file_}, recipe.image = {recipe.image} ")
        logger.info(f'Успешно обновили рецепт: {recipe}.')
        recipe = Recipe.objects.get(pk=rcp_id)

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

    else:
        form = RecipeForm()
        cat = Category.objects.order_by('category_name')
        recipe = Recipe.objects.get(pk=rcp_id)
        journal = Journal.objects.filter(recipe_name=recipe)

    return render(request, 'recipe/recipe_edit.html', {'journal': journal, 'category': cat, 'recipe': recipe, 'form': form, "title": "Редактируем рецепт"})


@login_required
def delete_recipe(request, rcp_id: int):
    '''Удаляем рецепт из базы'''

    rcp = Recipe.objects.get(pk=rcp_id)
    rcp.delete()
    name = Recipe.objects.all()
    # print(name)
    logger.info(f'Удалили рецепт. Автор - {request.user}')
    return render(request, "recipe/recipe.html", context={"recipe": name, "title": "Рецепты"})
# _________________RECIPE______________________


@login_required
def create_jrn(request, rcp_id: int):
    '''Создаем запись в журнале принадлежности рецепта к категории
        это делается из редактора рецепта'''

    path_url = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        if request.POST.get('name') != "":
            name = request.POST.get("name")
        if request.POST.get('cat') != "":
            cat = request.POST.get("cat")
        path_url = request.POST.get("path_url")
        rcp = Recipe.objects.get(name=name)
        cat = Category.objects.get(category_name=cat)

        jrn = Journal.objects.update_or_create(recipe_name=rcp, category=cat)

        logger.info(f'Успешно создали этап проекта: {jrn}.')
        return HttpResponsePermanentRedirect(path_url)

    else:
        cat = Category.objects.all()
        recipe = Recipe.objects.get(pk=rcp_id)
        return render(request, "recipe/journal_create.html", context={'path_url': path_url, 'recipe': recipe, "category": cat, "title": "Рецепты"})


@login_required
def delete_jrn(request, jrn_id: int):
    '''Удаляем запись в журнале принадлежности рецепта к категории
        это делается из редактора рецепта'''

    stage = Journal.objects.get(pk=jrn_id)
    stage.delete()
    logger.info(f'Успешно удалили этап проекта.')
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


@login_required
def edit_jrn(request, rcp_id: int, cat_id: int):
    '''Редактируем запись в журнале принадлежности рецепта к категории
        Редактируется это в редакторе рецепта'''

    path_url = request.META.get('HTTP_REFERER')
    # print(f'Адрес страницы: {path_url}')
    if request.method == 'POST':
        if request.POST.get('name') != "":
            name = request.POST.get("name")
        if request.POST.get('cat') != "":
            cat = request.POST.get("cat")
        path_url = request.POST.get("path_url")
        rcp = Recipe.objects.get(name=name)
        cat = Category.objects.get(category_name=cat)

        jrn = Journal.objects.update_or_create(recipe_name=rcp, category=cat)

        logger.info(f'Успешно обновили этап проекта: {jrn}.')

        return HttpResponsePermanentRedirect(path_url)

    else:
        cat = Category.objects.get(pk=cat_id)
        recipe = Recipe.objects.get(pk=rcp_id)
    return render(request, "recipe/journal_edit.html", context={'path_url': path_url, 'recipe': recipe, "category": cat, "title": "Рецепты"})
