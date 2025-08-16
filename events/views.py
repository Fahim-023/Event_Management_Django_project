from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from django.utils import timezone
from events.models import Event, Category
from events.forms import EventForm, CategoryForm
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from users.forms import AssignRoleForm, CreateGroupForm

# ========= ROLE CHECK FUNCTIONS =========
def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()

def is_participant(user):
    return user.groups.filter(name='User').exists()

# ========= HOME PAGE =========
@login_required
def home(request):
    category_id = request.GET.get('category')
    search_query = request.GET.get('q')
    events = Event.objects.select_related('category').prefetch_related('participants') \
                .annotate(participant_count=Count('participants'))

    if category_id:
        events = events.filter(category_id=category_id)
    
    if search_query:
        events = events.filter(
            Q(name__icontains=search_query) | Q(location__icontains=search_query)
        )

    categories = Category.objects.all()
    return render(request, 'events/home.html', {
        'events': events,
        'categories': categories,
        'selected_category': category_id,
        'search_query': search_query,
    })

# ========= EVENT DETAIL =========
@login_required
def event_detail(request, pk):
    event = get_object_or_404(Event.objects.prefetch_related('participants'), pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})

# ========= CREATE EVENT =========
@login_required
@user_passes_test(lambda u: is_admin(u) or is_organizer(u), login_url='no-permission')
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST,request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user  # Set event creator
            event.save()
            form.save_m2m()
            messages.success(request, "Event created successfully.")
            return redirect('home')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form})

# ========= UPDATE EVENT =========
@login_required
@user_passes_test(lambda u: is_admin(u) or is_organizer(u), login_url='no-permission')
def update_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    #  Only allow organizers to edit their own events
    if is_organizer(request.user) and event.created_by != request.user:
        return redirect('no-permission')

    if request.method == 'POST':
        form = EventForm(request.POST,request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully.")
            return redirect('event_detail', pk=pk)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form})

# ========= DELETE EVENT =========
@login_required
@user_passes_test(lambda u: is_admin(u) or is_organizer(u), login_url='no-permission')
def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    #  Only allow organizers to delete their own events
    if is_organizer(request.user) and event.created_by != request.user:
        return redirect('no-permission')

    if request.method == 'POST':
        event.delete()
        messages.success(request, "Event deleted successfully.")
        return redirect('home')
    return render(request, 'events/event_confirm_delete.html', {'event': event})

# ========= CATEGORY CRUD (ADMIN ONLY) =========
@login_required
@user_passes_test(is_admin, login_url='no-permission')
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'events/category_form.html', {'form': form})

@login_required
@user_passes_test(is_admin, login_url='no-permission')
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'events/category_list.html', {'categories': categories})

@login_required
@user_passes_test(is_admin, login_url='no-permission')
def update_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully.")
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'events/category_form.html', {'form': form})

@login_required
@user_passes_test(is_admin, login_url='no-permission')
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, "Category deleted successfully.")
        return redirect('category_list')
    return render(request, 'events/category_confirm_delete.html', {'category': category})

# ========= FRONT PAGE =========
def frontpage(request):
    return render(request, 'events/frontpage.html')

# ========= RSVP TOGGLE =========
@login_required
@user_passes_test(is_participant, login_url='no-permission')
def rsvp_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user

    if user in event.participants.all():
        event.participants.remove(user)
        messages.success(request, f"You have canceled RSVP for '{event.name}'.")
    else:
        event.participants.add(user)
        messages.success(request, f"You have RSVP'd for '{event.name}'.")

    return redirect(request.META.get("HTTP_REFERER", "home"))

# ========= DASHBOARDS =========
@login_required
@user_passes_test(is_admin, login_url='no-permission')
def admin_dashboard(request):
    users = User.objects.all().annotate(group_name=Count('groups'))
    return render(request, 'dashboard/admin_dashboard.html', {'users': users})

@login_required
@user_passes_test(is_organizer, login_url='no-permission')
def organizer_dashboard(request):
    events = Event.objects.filter(created_by=request.user)  # Show only their events
    return render(request, 'dashboard/organizer_dashboard.html', {'events': events})

@login_required
@user_passes_test(is_participant, login_url='no-permission')
def participant_dashboard(request):
    my_rsvp_events = request.user.rsvp_event.all()
    available_events = Event.objects.exclude(participants=request.user)
    context = {
        'available_events': available_events,
        'my_rsvp_events': my_rsvp_events
    }
    return render(request, 'dashboard/participant_dashboard.html', context)

@login_required
def dashboard(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_organizer(request.user):
        return redirect('organizer-dashboard')
    elif is_participant(request.user):
        return redirect('participant-dashboard')
    else:
        return redirect('no-permission')

# ========= GROUP MANAGEMENT (ADMIN ONLY) =========
@login_required
@user_passes_test(is_admin, login_url='no-permission')
def create_group(request):
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group '{group.name}' created successfully.")
            return redirect('group-list')
    else:
        form = CreateGroupForm()
    return render(request, 'events/create_group.html', {'form': form})

@login_required
@user_passes_test(is_admin, login_url='no-permission')
def group_list(request):
    groups = Group.objects.all()
    return render(request, 'events/group_list.html', {'groups': groups})

@login_required
@user_passes_test(is_admin, login_url='no-permission')
def assign_role(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            user.groups.clear()
            user.groups.add(role)
            messages.success(request, f"Role for '{user.username}' updated to '{role.name}'.")
            return redirect('admin-dashboard')
    else:
        form = AssignRoleForm()
    return render(request, 'events/assign_role.html', {'form': form, 'user': user})

# ========= NO PERMISSION =========
def no_permission(request):
    return render(request, 'events/no_permission.html')
