from django.shortcuts import render
from markdown2 import markdown
from . import util
from random import randint


def index(request):
    return render(request, 'encyclopedia/index.html', {
        "entries": util.list_entries()
    })


def display_entry(request, entry_name):
    # Get entry data
    entry = util.get_entry(entry_name)

    # Check if entry is found
    if entry:
        return render(request, "encyclopedia/entry.html", {
            'title': util.get_entry_title(entry_name),
            'entry': markdown(entry)
        })
    # if entry is not found return error
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "Page Not Found"
        })


def search(request):
    # Get q arugument and clean it
    q = request.GET.get('q').strip().lower()

    # if entry is found display it
    if util.get_entry(q):
        return display_entry(request, q)
    # if not found check if it's a sub entry
    else:
        # List all available entries
        available_entries = util.list_entries()
        # q_sub is a set to store all entries in which q is a substring
        q_sub = set()

        # Iterate over available entries and check if q is a sub entry
        # If yes add to q_sub
        for entry in available_entries:
            if q in entry.lower():
                q_sub.add(entry)

        # If there is only on matched entity at least
        # Render search_result.html to display a list of matches
        if len(q_sub):
            return render(request, "encyclopedia/search_result.html", {
                "entries": q_sub
            })
        # If there is no match render error
        else:
            return render(request, "encyclopedia/error.html", {
                "message": "No Results!"
            })


def create_page(request):
    # If method is POST
    if request.method == "POST":
        # Retrive Data
        title = request.POST.get('title')
        content = request.POST.get('content')

        # If Entry title is found retrun error
        if util.get_entry(title):
            return render(request, "encyclopedia/error.html", {
                "message": "Page already exists!"
            })

        # Save entry
        util.save_entry(title, content)
        # Display entry page
        return display_entry(request, title)

    # If method is GET render create_page.html
    return render(request, "encyclopedia/create_page.html")


def edit_page(request):
    if request.POST.get("edited") == 'false':
        title = request.POST.get('title')
        return render(request, "encyclopedia/edit_page.html", {
            "title": title,
            "content": util.get_entry(title)
        })
    else:
        new_title = request.POST.get('new_title')
        old_title = request.POST.get('old_title')

        if new_title != old_title:
            util.delete_entry(request.POST.get('old_title'))

        print(request.POST.get('new_content'))
        util.save_entry(new_title, request.POST.get('new_content'))

        return display_entry(request, new_title)


# Return random entry page
def random_page(request):
    available_entries = util.list_entries()
    random_index = randint(0, len(available_entries)-1)

    return display_entry(request, available_entries[random_index])
