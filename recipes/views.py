from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


from recipes.serializers import RecipeSerializer
from .models import Recipe


class RecipeListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        '''
        List all the recipes for given requested user
        '''
        recipes = Recipe.objects.filter(user = request.user.id)
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        '''
        Create Recipe with given data
        '''
        data = {
            'title': request.data.get('title'),
            'ingredients': request.data.get('ingredients'),
            'time_required': request.data.get('time_required'),
            'instructions': request.data.get('instructions'),
            'user': request.user.id
        }
        serializer = RecipeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class RecipeDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    def get_object(self, recipe_id, user_id):
        '''
        Helper method to get the object with given recipe_id, and user_id
        '''
        try:
            return Recipe.objects.get(id=recipe_id, user = user_id)
        except Recipe.DoesNotExist:
            return None
        
    def get(self, request, recipe_id, *args, **kwargs):
        '''
        Retrieves the Recipe with given recipe_id
        '''
        recipe_instance = self.get_object(recipe_id, request.user.id)
        if not recipe_instance:
            return Response(
                {"res": "Object with recipe id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = RecipeSerializer(recipe_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # 4. Update
    def put(self, request, recipe_id, *args, **kwargs):
        '''
        Updates the recipe item with given recipe_id if exists
        '''
        recipe_instance = self.get_object(recipe_id, request.user.id)
        if not recipe_instance:
            return Response(
                {"res": "Object with recipe id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'title': request.data.get('title'),
            'ingredients': request.data.get('ingredients'),
            'time_required': request.data.get('time_required'),
            'instructions': request.data.get('instructions'),
            'user': request.user.id 
        }
        serializer = RecipeSerializer(instance = recipe_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, recipe_id, *args, **kwargs):
        '''
        Deletes the recipe item with given recipe_id if exists
        '''
        recipe_instance = self.get_object(recipe_id, request.user.id)
        if not recipe_instance:
            return Response(
                {"res": "Object with recipe id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        recipe_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )