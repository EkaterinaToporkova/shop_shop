from django.views.generic import ListView, DetailView
from shop.models import Recipe, Product


class RecipesListView(ListView):
    model = Recipe
    template_name = 'recipes/soups.html'

class RecipesDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/recipes_details.html'
