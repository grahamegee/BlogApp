from django.shortcuts import render
from .models import Entry
from .forms import EntryForm

def blog(request):
    entries = Entry.objects.order_by('created_date')
    return render(request, 'blog/main.html', {'entries' : entries})

def dashboard(request):

    entries = Entry.objects.order_by('created_date')
    forms = [EntryForm({'title' : entry.title, 'text' : entry.text})\
             for entry in entries]
    blankform = EntryForm()
    
   # if request.method == 'POST':
   #     pass
   # else:
   #     form = EntryForm()
    
    return render(request, 'blog/dashboard.html', 
                  {'forms' : forms, 'blankform' : blankform})
