from django.views.generic import ListView
from shop.models import Recipe


class RecipesListView(ListView):
    model = Recipe
    template_name = 'recipes/soups.html'

class RecipesDetailView(ListView):
    model = Recipe
    template_name = 'recipes/recipes_details.html'

