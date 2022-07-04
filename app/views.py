import numpy as np

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from app.forms import DataForm
from app.models import Data
from app.topsis import Topsis


# Create your views here.


def index(request):
    data = Data.objects.all()
    field_names = [f.verbose_name for f in Data._meta.get_fields()]
    weights = [5, 5, 9, 0]
    criterias = np.array([True, True, True, True])
    field_names = [f.verbose_name for f in Data._meta.get_fields()]
    arr = []
    for d in data:
        arr.append(
            [
                [d.nilai_score],
                [d.penghasilan],
                [d.tanggungan],
                [d.organisasi],
            ]
        )

    evaluation_matrix = np.array(arr)
    t = Topsis(evaluation_matrix, weights, criterias)
    t.calc()

    for i, d in enumerate(data):
        d.best_distance = t.best_distance[i]
        d.worst_distance = t.worst_distance[i]
        d.worst_similarity = t.worst_similarity[i]
        d.worst_similarity_rank = t.rank_to_worst_similarity()[i]
        d.best_similarity = t.best_similarity[i]
        d.best_similarity_rank = t.rank_to_best_similarity()[i]
    context = {
        "data": data,
        "field_names": field_names,
    }

    return render(request, "index.html", context)


def analysis(request):
    data = Data.objects.all()
    weights = [5, 5, 9, 0]
    criteria = np.array([True, True, True, True])
    arr = []
    for d in data:
        arr.append(
            [
                [d.nilai_score],
                [d.penghasilan],
                [d.tanggungan],
                [d.organisasi],
            ]
        )

    evaluation_matrix = np.array(arr)
    t = Topsis(evaluation_matrix, weights, criteria)
    t.calc()

    for i, d in enumerate(data):
        d.best_distance = t.best_distance[i]
        d.worst_distance = t.worst_distance[i]
        d.worst_similarity = t.worst_similarity[i]
        d.worst_similarity_rank = t.rank_to_worst_similarity()[i]
        d.best_similarity = t.best_similarity[i]
        d.best_similarity_rank = t.rank_to_best_similarity()[i]

    context = {"data": data}

    return render(request, "analysis.html", context)


def create(request):

    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = DataForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect(redirect_to=reverse("index"))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = DataForm()

    context = {"form": form}

    return render(request, "create.html", context)
