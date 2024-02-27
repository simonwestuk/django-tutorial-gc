from django.shortcuts import redirect, render, get_object_or_404
from django.utils.timezone import datetime
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from hello.forms import LogMessageForm, EditMessageForm
from hello.models import LogMessage


class HomeListView(ListView):
    """Renders the home page, with a list of all polls."""

    model = LogMessage

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context


def about(request):
    """Renders the about page."""
    return render(request, "hello/about.html")


def contact(request):
    """Renders the contact page."""
    return render(request, "hello/contact.html")


def hello_there(request, name):
    """Renders the hello_there page.
    Args:
        name: Name to say hello to
    """
    return render(
        request, "hello/hello_there.html", {"name": name, "date": datetime.now()}
    )


def log_message(request):
    form = LogMessageForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            message.log_date = datetime.now()
            message.save()
            return redirect("home")
        else:
            return render(request, "hello/log_message.html", {"form": form})
    else:
        return render(request, "hello/log_message.html", {"form": form})


def edit_message(request, message_id):
    message = get_object_or_404(LogMessage, id=message_id)
    print(message)
    if request.method == "POST":
        form = EditMessageForm(request.POST, instance=message)

        if form.is_valid():
            form.save()
            return redirect("home")
        else:
            return render(request, "hello/log_message.html", {"form": form})
    else:
        form = EditMessageForm(instance=message)
        return render(request, "hello/edit_message.html", {"form": form})


@require_POST
def delete_message(request, message_id):
    """Deletes a specific log message."""
    message = get_object_or_404(LogMessage, id=message_id)
    message.delete()
    return redirect('home')
