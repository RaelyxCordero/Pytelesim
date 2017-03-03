from django.shortcuts import render

# Create your views here.
def home_view_fbv(request, *args, **kwargs):
    if request.method == "POST":
        print(request.POST)
    return render(request, "base/mod_fm.html", {})