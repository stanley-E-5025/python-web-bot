import threading
from django.shortcuts import render, redirect, get_object_or_404
from scraper_app.forms.scrap_form import ScraperForm
from .models import Scraper
from .helpers.web_scraper import ScraperClient
import json


def dashboard(request):
    form = ScraperForm()
    if request.method == 'POST':
        form = ScraperForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        # Get all workers from the database
        workers = Scraper.objects.all()
        return render(request, 'dashboard.html', {'form': form, 'workers': workers})

def run_worker(request, worker_id):
    worker = get_object_or_404(Scraper, id=worker_id)
    # Start a new thread to run the worker
    thread = threading.Thread(target=run_worker_in_thread, args=(worker,))
    thread.start()
    return redirect('dashboard')

def run_worker_in_thread(worker):
    # Here, put the code that will actually run the worker.
    steps = json.loads(worker.steps)
    scraper = ScraperClient(url=worker.url, steps=steps, case=worker.case, data=worker.data)
    result = scraper.extract_blob()
    # Do something with the result...