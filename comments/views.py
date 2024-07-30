from rest_framework import generics, mixins
from django.db.models import F
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Comment
from .serializers import CommentSerializer

class CommentMixinListView(mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.query_params.get('sort')
        resource_id = self.request.query_params.get('resource_id')
        
        if resource_id:                                                                                                                                                                                                                    
                queryset = queryset.filter(resource_id=resource_id)

        if sort_by:
            if sort_by.startswith('-'):
                field_name = sort_by[1:]
                queryset = queryset.order_by(F(field_name).desc())
            else:
                queryset = queryset.order_by(sort_by)

        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CommentMixinDetailView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)