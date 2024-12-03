from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, serializers
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from .models import Ingredient, Recipe
from .serializers import IngredientSerializer, RecipeSerializer

from django.shortcuts import get_object_or_404


class RecipeViewSet(viewsets.ModelViewSet):
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    model = Recipe
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['title']
    ordering_fields = ['id', 'title', 'created_at', 'updated_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        pk = self.kwargs['pk']
        author_id = get_object_or_404(Recipe, pk=pk).author.id
        print(author_id)
        if author_id == self.request.user.id:
            serializer.save(author = self.request.user)
        return serializers.ValidationError('You can only update your own recipes')

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            instance.delete()
        return serializers.ValidationError('You can only delete your own recipes')

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    model = Ingredient

    def perform_create(self, serializer):
        recipe = serializer.validated_data['recipe']
        if recipe.author != self.request.user:
            serializer.save(recipe=recipe)
        return serializers.ValidationError('You can only add ingredients to your own recipes')

    def perform_update(self, serializer):
        pk = self.kwargs['pk']
        ingredient = get_object_or_404(Ingredient, pk=pk)
        if ingredient.recipe.author != self.request.user:
            serializer.save()
        return serializers.ValidationError('You can only update ingredients in your own recipes')

    def perform_destroy(self, instance):
        if instance.recipe.author != self.request.user:
            instance.delete()
        return serializers.ValidationError('You can only delete ingredients in your own recipes')
