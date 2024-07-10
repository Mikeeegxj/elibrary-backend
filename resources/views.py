from rest_framework import generics,mixins
from django.db.models import F
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Resource
from categories.models import Category
from .serializers import ResourceSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Q, Value
from django.db.models.functions import Concat

class ResourceMixinListView(mixins.CreateModelMixin,mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        category_id = self.request.data.get('category')
        category = Category.objects.get(id=category_id)
        serializer.save(user=self.request.user, category=category)

    def get_serializer_context(self):
        """
        Pass the request object to the serializer context.
        """
        context = super(ResourceMixinListView, self).get_serializer_context()
        context.update({
            "request": self.request
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.query_params.get('sort')
        search_term = self.request.query_params.get('search', None)
        category_id = self.request.query_params.get('category', None)

        if sort_by:
            if sort_by.startswith('-'):
                field_name = sort_by[1:]
                queryset = queryset.order_by(F(field_name).desc())
            else:
                queryset = queryset.order_by(sort_by)

        if search_term:
            queryset = queryset.filter(Q(title__icontains=search_term) | Q(author__icontains=search_term))
        
        if category_id:
            queryset = queryset.filter(category__id=category_id)
        
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ResourceMixinDetailView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    lookup_field = 'pk'

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_count += 1
        instance.save()
        return self.retrieve(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    def perform_update(self, serializer):
        category_id = self.request.data.get('category')
        if category_id:
            category = get_object_or_404(Category, id=category_id)
            serializer.save(category=category)
        else:
            serializer.save()
    
    def get_serializer_context(self):
        context = super(ResourceMixinDetailView, self).get_serializer_context()
        context.update({
            "request": self.request
        })
        return context