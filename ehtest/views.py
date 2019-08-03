from django.shortcuts import render
from ehtest.models import ehExplorer


def explorer_view(request):
    hero = ehExplorer.objects.get(id=1)  # Yallatir -- later this will need to be based on the logged-in user...
    if request.method == 'POST':
        direction = request.POST.get('direction', None)
        print("direction: {}".format(direction))
        if direction is not None:
            direction = int(direction)
            if direction in [0, 1, 2, 3]:
                hero.move(direction)
    return render(request, 'ehtileview.html', {'hero': hero}, content_type="text/html")
    # 4 images -- Exit, Goal, Blank, Marked.  64px square.
