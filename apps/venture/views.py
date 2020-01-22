from django.shortcuts import render
from django.http import HttpResponseRedirect
from apps.venture.form import VentureForm, CommentForm, FundingForm
from apps.venture.models import Venture, Comment, Pledge
from django.contrib.auth.decorators import login_required


@login_required
def create_venture(request):
    if request.method == 'POST':
        form = VentureForm(request.POST, request.FILES)
        if form.is_valid():
            venture = form.save(commit=False)
            venture.creator = request.user
            venture.status = 0
            venture.save()
            return HttpResponseRedirect('/ventures/' + str(venture.id))
    else:
        form = VentureForm()
    return render(request, 'venture/create.html', {'form': form})

def pledge(request, id):
    c = {}
    try:
        c["venture"] = Venture.objects.get(id=id)
    except Venture.DoesNotExist:
        return HttpResponseRedirect('/ventures')

    if request.method == 'POST':
        form = FundingForm(request.POST, request.FILES)
        if form.is_valid():
            fundign = form.save(commit=False)  
            if request.user.amount < fundign.amount:
                form.add_error("amount","Pas assez d'argent")
                fundign.who = request.user
                fundign.to = c["venture"]
                fundign.save()
                return HttpResponseRedirect(f'/ventures/{ c["venture"].id }')
    else:
        form = FundingForm()
    c["form"] = form
    return render(request, 'venture/pledge.html', c)


def home(request):
    venture = Venture.objects.first()
    return render(request, 'index.html', {'venture': venture})


def filter(request, ventures):
    filter_state = request.GET.get('filter_state')
    from django.db.models import Prefetch, Sum, F
    from django.db.models.functions import Coalesce
    ventures = ventures.annotate(amount_current=Coalesce(Sum('pledge__amount'),0)).exclude(amount_current__isnull=True)
    ventures = ventures.annotate(percent_current=F('amount_current')*100/F('goal'))
 
    filter_amount = request.GET.get('filter_amount')
    if filter_amount == '1':
        ventures =ventures.filter(amount_current__lt=1000)
    elif filter_amount == '2':
        ventures = ventures.filter(amount_current__gte=1000, amount_current__lt=10000)
    elif filter_amount == '3':
        ventures = ventures.filter(amount_current__gte=10000, amount_current__lt=100000)
    elif filter_amount == '4':
        ventures = ventures.filter(amount_current__gte=100000, amount_current__lt=1000000)
    elif filter_amount == '5':
        ventures = ventures.filter(amount_current__gte=1000000)
    filter_goal = request.GET.get('filter_goal')
    if filter_goal == '1':
        ventures = ventures.filter(goal__lte=1000)
    elif filter_goal == '2':
        ventures = ventures.filter(goal__gte=1000, goal__lt=10000)
    elif filter_goal == '3':
        ventures = ventures.filter(goal__gte=10000, goal__lt=100000)
    elif filter_goal == '4':
        ventures = ventures.filter(goal__gte=100000, goal__lt=1000000)
    elif filter_goal == '5':
        ventures = ventures.filter(goal__gte=1000000)
    filter_percent = request.GET.get('filter_percent')
    if filter_percent == '1':
        ventures = ventures.filter(percent_current__lte=75)
    elif filter_percent == '2':
        ventures = ventures.filter(percent_current__gte=75, percent_current__lt=100)
    elif filter_percent == '3':
        ventures = ventures.filter(percent_current__gte=100)
    return ventures


def sort(request, ventures):
    sort_alpha = request.GET.get('sort_alpha')
    if sort_alpha == '1':
        ventures = ventures.order_by('name')
    elif sort_alpha == '2':
        ventures = ventures.order_by('-name')
    sort_new = request.GET.get('sort_new')
    if sort_new == '1':
        ventures = ventures.order_by('created_at')
    elif sort_new == '2':
        ventures = ventures.order_by('-created_at')
    return ventures


def show_ventures(request):
    if 'search' in request.GET:
        ventures = Venture.objects.filter(name__icontains=request.GET['search'])
    else:
        ventures = Venture.objects.all()
    if request.is_ajax():
        data = request.GET.get('sort')
        ventures = filter(request, ventures)
        ventures = sort(request, ventures)
        return render(request, 'venture/list_venture.html', {'ventures': ventures})
    return render(request, 'venture/ventures.html', {'ventures': ventures})


def show_venture(request, id):
    c = {}
    try:
        c["venture"] = Venture.objects.get(id=id)
    except Venture.DoesNotExist:
        return HttpResponseRedirect('/ventures')

    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)  
            comment.who = request.user
            comment.what = c["venture"]
            comment.save()
    else:
        form = CommentForm()
    c["form"] = form
    return render(request, 'venture/venture.html', c)