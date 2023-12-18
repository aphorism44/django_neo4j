from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse


def index(request):
    neo4j_crud = request.neo4j_crud
    latest_question_list = neo4j_crud.get_latest_questions(num=5)
    template = loader.get_template("polls/index.html")
    context = {
        "latest_question_list": latest_question_list,
    }
    return HttpResponse(template.render(context, request))


#used only for setup
#def index(request):
#    populate_test_database(request)
#    return HttpResponse("You added 2 questions")

def detail(request, question_id):
    neo4j_crud = request.neo4j_crud
    question = neo4j_crud.get_question_by_id(question_id)
    choices = neo4j_crud.get_choices_by_question_id(question_id)
    if question:
        return render(request, "polls/detail.html", {"question": question, "choices" : choices})
    else:
        raise Http404("Question does not exist")
    
def vote(request, question_id):
    neo4j_crud = request.neo4j_crud
    question = neo4j_crud.get_question_by_id(question_id)
    if not question:
        raise Http404("Question does not exist")
    selected_choice_id = request.POST["choice"]
    if not selected_choice_id:
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        data = neo4j_crud.add_votes_to_choice(selected_choice_id, 1)
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question['id'],)))

def results(request, question_id):
    neo4j_crud = request.neo4j_crud
    question = neo4j_crud.get_question_by_id(question_id)
    choices = neo4j_crud.get_choices_by_question_id(question_id)
    if not question:
        raise Http404("Question does not exist")
    return render(request, "polls/results.html", {"question": question, "choices": choices})


#only run this once to populate a test database    
def populate_test_database(request):
    neo4j_crud = request.neo4j_crud
    q1 = neo4j_crud.create_question("Who discovered America?")
    neo4j_crud.add_choice_to_question(q1['id'], "Ferdinand Magellan")
    neo4j_crud.add_choice_to_question(q1['id'], "Vasco de Gama")
    neo4j_crud.add_choice_to_question(q1['id'], "Christopher Columbus")
    neo4j_crud.add_choice_to_question(q1['id'], "Walter Raleigh")
    q2 = neo4j_crud.create_question("Which of these signed the Declaration of Independence?")
    neo4j_crud.add_choice_to_question(q2['id'], "George Washington")
    neo4j_crud.add_choice_to_question(q2['id'], "John Adams")
    neo4j_crud.add_choice_to_question(q2['id'], "Alexander Hamilton")
    neo4j_crud.add_choice_to_question(q2['id'], "James Madison")