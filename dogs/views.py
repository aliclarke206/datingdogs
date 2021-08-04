from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Dog, Breed
from .forms import NewDogForm

# Create your views here.


def all_dogs(request):
    """ A view to show all dogs, including sorting and search queries """

    dogs = Dog.objects.all()
    query = None
    breeds = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                dogs = dogs.annotate(lower_name=Lower('name'))
            if sortkey == 'breed':
                sortkey = 'breed__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            dogs = dogs.order_by(sortkey)

    if request.GET:
        if 'breed' in request.GET:
            breeds = request.GET['breed'].split(',')
            dogs = dogs.filter(breed__name__in=breeds)
            breeds = Breed.objects.filter(name__in=breeds)

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('dogs'))
            
            queries = Q(location__icontains=query) | Q(description__icontains=query)
            dogs = dogs.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'dogs': dogs,
        'search_term': query,
        'current_breeds': breeds,
        'current_sorting': current_sorting,
    }

    return render(request, 'dogs/dogs.html', context)


def dog_detail(request, dog_id):
    """ A view to show individual dog details """

    dog = get_object_or_404(Dog, pk=dog_id)

    context = {
        'dog': dog,
    }

    return render(request, 'dogs/dog_detail.html', context)


def add_dog(request):
    """ Add a dog to the store """
    if request.method == 'POST':
        form = NewDogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added dog!')
            return redirect(reverse('add_dog'))
        else:
            messages.error(request, 'Failed to add dog. Please ensure the form is valid.')
    else:
        form = NewDogForm()
        
    template = 'dogs/add_dog.html'
    context = {
        'form': form,
    }

    return render(request, template, context)