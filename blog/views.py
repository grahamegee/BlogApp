from django.shortcuts import render
from .models import Entry

def blog(request):
    entries = Entry.objects.order_by('created_date')
    return render(request, 'blog/main.html', {'entries' : entries})
