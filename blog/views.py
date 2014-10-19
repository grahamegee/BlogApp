from django.shortcuts import render, redirect, get_object_or_404
from .models import Entry
from .forms import EntryForm

def blog(request):
    """
    Public blog view
    """
    entries = Entry.objects.order_by('created_date')
    return render(request, 'blog/main.html', {'entries' : entries})

def dashboard(request):
    """
    View for admin dashboard; similar to the public 'blog' view.
    """
    entries = Entry.objects.order_by('created_date')
    return render(request, 'blog/dashboard.html', {'entries' : entries})
 
def newentry(request):
    """
    View for creating new blog entries
    """
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog.views.dashboard')
    else:
        form = EntryForm()

    return render(request, 'blog/newentry.html', {'form' : form })

def editentry(request, pk):
    """
    View for editing existing blog entries
    """
    entry = get_object_or_404(Entry, pk=pk)
    if request.method == 'POST':
        if request.POST.get('delete'):
            entry.delete()
        else:
            form = EntryForm(request.POST, instance=entry)
            if form.is_valid():
                form.save()
        return redirect('blog.views.dashboard')
    else:
        form = EntryForm(instance=entry)

    return render(request, 'blog/editentry.html', {'form' : form })
