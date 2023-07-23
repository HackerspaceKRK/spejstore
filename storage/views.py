import shlex

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.postgres.search import SearchVector, TrigramSimilarity
from django.http import Http404, JsonResponse, HttpResponse
from django.contrib.admin.models import LogEntry
from django_select2.views import AutoResponseView
from django.db import connection
from django.db.models import Q

from storage.models import Item, Label

from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token


def apply_smart_search(query, objects):
    general_term = []

    filters = {}

    for prop in shlex.split(query):
        if ":" not in prop:
            general_term.append(prop)
        else:
            key, value = prop.split(":", 1)
            if key in ["owner", "taken_by"]:
                filters[key + "__username"] = value
            elif hasattr(Item, key):
                filters[key + "__search"] = value
            elif key == "ancestor":
                objects = Item.objects.get(pk=value).get_children()
            elif key == "prop" or value:
                if key == "prop":
                    key, _, value = value.partition(":")
                if not value:
                    filters["props__isnull"] = {key: False}
                else:
                    filters["props__contains"] = {key: value}
            else:
                # "Whatever:"
                general_term.append(prop)

    objects = objects.filter(**filters)

    if not general_term:
        return objects
    general_term = " ".join(general_term)

    objects = (
        objects.annotate(
            search=SearchVector("name", "description", "props", config="simple"),
            similarity=TrigramSimilarity("name", general_term),
        )
        .filter(Q(similarity__gte=0.15) | Q(search__contains=general_term))
        .order_by("-similarity")
    )
    return objects


def index(request):
    # get_roots was removed, so we're doing it this way now.
    return render(
        request, "results.html", {"results": Item.objects.filter(**{"path__level": 1})}
    )


def search(request):
    query = request.GET.get("q", "")

    results = apply_smart_search(query, Item.objects).all()

    if results and (len(results) == 1 or getattr(results[0], "similarity", 0) == 1):
        return redirect(results[0])

    return render(
        request,
        "results.html",
        {
            "query": query,
            "results": results,
        },
    )


def item_display(request, pk):
    if not pk:
        return index(request)
    item = get_object_or_404(Item, pk=pk)

    labels = item.labels.all()
    has_one_label = len(labels) == 1

    return render(
        request,
        "item.html",
        {
            "title": item.name,
            "item": item,
            "categories": item.categories.all(),
            "props": sorted(item.props.items()),
            "images": item.images.all(),
            "labels": labels,
            "has_one_label": has_one_label,
            "history": LogEntry.objects.filter(object_id=item.pk),
            "ancestors": item.get_ancestors(),
            "children": item.get_children().prefetch_related("categories"),
        },
    )


def label_lookup(request, pk):
    try:
        label = Label.objects.get(pk=pk)
        return redirect(label.item)
    except Label.DoesNotExist:
        try:
            # look up by short id
            item = Item.objects.get(uuid__startswith=pk)
            return redirect(item)
        except Item.DoesNotExist:
            raise Http404("Very sad to say, I could not find this thing")


def apitoken(request):
    print(Token)
    token, created = Token.objects.get_or_create(user=request.user)
    return HttpResponse(token.key, content_type="text/plain")


class ItemSelectView(AutoResponseView):
    def get(self, request, *args, **kwargs):
        self.widget = self.get_widget_or_404()
        self.term = kwargs.get("term", request.GET.get("term", ""))
        self.object_list = apply_smart_search(self.term, Item.objects)
        context = self.get_context_data()
        return JsonResponse(
            {
                "results": [
                    {
                        "text": obj.name,
                        "path": [o.name for o in obj.get_ancestors()],
                        "id": obj.pk,
                    }
                    for obj in context["object_list"]
                ],
                "more": context["page_obj"].has_next(),
            }
        )


class PropSelectView(AutoResponseView):
    def get(self, request, *args, **kwargs):
        # self.widget = self.get_widget_or_404()
        self.term = kwargs.get("term", request.GET.get("term", ""))
        # context = self.get_context_data()
        with connection.cursor() as c:
            c.execute(
                """
                SELECT key, count(*) FROM
                (SELECT (each(props)).key FROM storage_item) AS stat
                WHERE key like %s
                GROUP BY key
                ORDER BY count DESC, key
                limit 10;
            """,
                ["%" + self.term + "%"],
            )
            props = [e[0] for e in c.fetchall()]
        return JsonResponse(
            {
                "results": [
                    {
                        "text": p,
                        "id": p,
                    }
                    for p in props
                ],
            }
        )
