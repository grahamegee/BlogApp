from django.shortcuts import render, redirect, get_object_or_404
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
    
    return render(request, 'blog/dashboard.html', 
                  {'forms' : forms, 'blankform' : blankform, 'entries' : entries})
 
def newentry(request, pk):
    entry = get_object_or_404(Entry, pk=pk)

    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog.views.dashboard')
    else:
        form = EntryForm(instance=entry)

    return render(request, 'blog/newentry.html', {'form' : form })
