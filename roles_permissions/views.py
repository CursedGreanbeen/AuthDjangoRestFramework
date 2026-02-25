from .utils import check_permission
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


class MockArticle:
    def __init__(self, id, title, content, owner_id):
        self.id = id
        self.title = title
        self.content = content
        self.owner_id = owner_id


article_list = [
    MockArticle(
        1,
        "Гипотеза стрелка и фермера",
        "«Гипотеза стрелка: снайпер стреляет в мишень, "
        "пробивая ее через каждые десять сантиметров. Двумерные "
        "существа, живущие на мишени, открывают великий закон: "
        "„Через каждые десять сантиметров во Вселенной имеется отверстие“. "
        "Они приняли сиюминутную прихоть стрелка за закон природы. "
        "Гипотеза фермера: индюшка, которую кормят каждый день в 11 утра, "
        "приходит к выводу: „Каждое утро прибывает еда“. В День благодарения "
        "в 11 утра вместо кормежки фермер забивает всех индюшек.»",
        owner_id=1
    ),
    MockArticle(
        2,
        "Тёмный лес космоса",
        "«Вселенная – это темный лес. Каждая цивилизация — "
        "вооруженный охотник, крадущийся среди деревьев. Он должен действовать "
        "тихо, даже дышать осторожно, потому что везде таятся другие охотники. "
        "Если он найдет кого-то другого — будь то другой охотник, демон или ангел — "
        "он может лишь сделать одно: выстрелить на поражение. В этом лесу ад — это другие.»",
        owner_id=2
    ),
    MockArticle(
        3,
        "Айсберг и океан",
        "«Что, если отношения между человечеством и злом "
        "подобны отношениям между океаном и айсбергом? "
        "И то, и другое состоит из одного вещества. И если "
        "айсберг кажется чем-то отличным от океана, то лишь потому, "
        "что у него другая форма. В действительности айсберг — часть "
        "того же необозримого океана. Совесть человечества спит, "
        "и не стоит рассчитывать, что она проснется сама. Это невозможно, "
        "как попытка вытащить себя из болота за волосы. Нужна помощь извне.»",
        owner_id=1
    )
]


@csrf_exempt
def article_list(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    if not check_permission(request.user, 'article', 'read'):
        return JsonResponse({'error': 'Forbidden'}, status=403)

    can_read_all = check_permission(request.user, 'article', 'read_all')

    if can_read_all:
        articles = article_list
    else:
        articles = [a for a in article_list if a.owner_id == request.user.id]

    data = [{'id': a.id, 'title': a.title, 'content': a.content} for a in articles]
    return JsonResponse({'articles': data}, status=200)
