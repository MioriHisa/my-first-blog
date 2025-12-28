from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "app1/index.html", context)

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "app1/detail.html", {"question": question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "app1/results.html", {"question":question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # request.Post にchoiceがあった場合、そのidを文字列として返す
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # request.Post にchoiceがなかったとき、エラーメッセージを返す
        # formから入力内容を再表示
        return render(
            request,
            "app1/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # reverse関数で、関数名からURLを逆引きし、そのURLにリダイレクトする。戻るボタンを使って2回送信されることを防ぐとこができる。
        return HttpResponseRedirect(reverse("app1:results", args=(question.id,)))
