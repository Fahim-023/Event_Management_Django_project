from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from django.utils import timezone
from events.models import Event, Category, Participant
from events.forms import  EventForm, ParticipantForm, CategoryForm
from django.contrib import messages

def home(request):
    category_id=request.GET.get('category')
    search_query=request.GET.get('q')
    events=Event.objects.select_related('category').prefetch_related('participants').annotate(participant_count=Count('participants'))

    if category_id:
        events=events.filter(category_id=category_id)
    
    if search_query:
         events = events.filter(Q(name__icontains=search_query) | Q(location__icontains=search_query))

    categories = Category.objects.all()
    return render(request, 'events/home.html', {
        'events': events,
        'categories': categories,
        'selected_category': category_id,
        'search_query': search_query,
    })

def event_detail(request,pk):
    event= get_object_or_404(Event.objects.prefetch_related('participants',pk=pk))
    return render(request, 'events/event_detail.html', {'event': event})

#organizer-dashboard
def dashboard(request):
    today = timezone.now().date()
    events = Event.objects.all()
    total_events = events.count()
    total_participants = Participant.objects.count()
    upcoming_events = events.filter(date__gte=today).count()
    past_events = events.filter(date__lt=today).count()
    todays_events = events.filter(date=today)

    return render(request, 'events/dashboard.html', {
        'total_events': total_events,
        'total_participants': total_participants,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'todays_events': todays_events,
    }) 


def create_event(request):
    if request.method=='POST':
        form =EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form=EventForm()
    return render(request, 'events/event_form.html', {'form': form})



def update_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_detail', pk=pk)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form})


def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('home')
    return render(request, 'events/event_confirm_delete.html', {'event': event})

def delete_participant(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == "POST":
        participant.delete()
        messages.success(request, "Participant deleted successfully.")
        return redirect('dashboard')  # or wherever appropriate
    return render(request, 'events/participant_confirm_delete.html', {'participant': participant})


def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')  # or wherever you want
    else:
        form = CategoryForm()
    return render(request, 'events/category_form.html', {'form': form})


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'events/category_list.html', {'categories': categories})



def update_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'events/category_form.html', {'form': form})

def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'events/category_confirm_delete.html', {'category': category})



def create_participant(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        event_id = request.POST.get('event_id')  # get selected event
        if form.is_valid() and event_id:
            participant = form.save()
            event = get_object_or_404(Event, id=event_id)
            event.participants.add(participant)
            return redirect('dashboard')  # or wherever you want
    else:
        form = ParticipantForm()
    
    events = Event.objects.all()  # For dropdown
    return render(request, 'events/create_participant.html', {'form': form, 'events': events})


def participant_list(request):
    participants = Participant.objects.all()
    return render(request, 'events/participant_list.html', {'participants': participants})


def update_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully.")
            return redirect('dashboard')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'events/category_form.html', {'form': form, 'category': category})

def update_participant(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == "POST":
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            messages.success(request, "Participant updated successfully.")
            return redirect('dashboard')
    else:
        form = ParticipantForm(instance=participant)
    return render(request, 'events/participant_update_form.html', {'form': form, 'participant': participant})

