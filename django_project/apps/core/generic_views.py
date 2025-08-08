from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class BaseListView(PermissionRequiredMixin, ListView):
    """
    Base view for displaying a list of objects.
    """
    object_actions = []
    actions = []
    template_name = 'core/generic_list.html'
    table_fields = []

    def get_permission_required(self):
        """
        can view if has any one of the read, change, delete permission
        """
        user = self.request.user
        self.app_label = self.model._meta.app_label
        self.model_name = self.model._meta.model_name
        for action in ["view", "change", "delete"]:
            if user.has_perm(f'{self.app_label}.{action}_{self.model_name}'):
                return [f'{self.app_label}.{action}_{self.model_name}']
        return [f'{self.app_label}.view_{self.model_name}']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # filter the action perm
        context["object_actions"] = {}
        for action, url, permission in self.object_actions:
            # it can be None for when this view can derive the permission on its own
            if not permission:
                _, permission = url.split(':')
            if user.has_perm(permission):
                context["object_actions"][action] = url
        
        # filter the action perm
        context["actions"] = {}
        for action, url, permission in self.actions:
            # it can be None for when this view can derive the permission on its own
            if not permission:
                _, permission = url.split(':')
            if user.has_perm(permission):
                context["actions"][action] = url

        context['table_fields'] = self.table_fields
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        # Get all potential foreign key fields from table_fields
        related_fields = set()
        for field in getattr(self, 'table_fields', []):
            # Add direct fields that might be foreign keys
            field = field.replace('.', '__')
            direct_field = field.split('__')[0]
            try: field_obj = self.model._meta.get_field(direct_field)
            except: continue
            direct_field_is_relation = field_obj.is_relation and field_obj.many_to_one and field_obj.concrete
            
            if direct_field_is_relation:
                related_fields.add(direct_field)

            if ("__" in field) and direct_field_is_relation:
                # check if the chained field is also a relation
                field_model = field_obj.related_model
                chained_obj = field_model._meta.get_field(field.split('__')[1])
                if chained_obj.is_relation and chained_obj.many_to_one and chained_obj.concrete:
                    related_fields.add(field)
            
        # Apply select_related if we have any related fields
        if related_fields:
            queryset = queryset.select_related(*related_fields)
        
        return queryset

class BaseWriteView(PermissionRequiredMixin):
    pk_url_kwarg = 'pk'
    template_name = 'core/generic_form.html'

    def get_success_url(self):
        return reverse_lazy(f'{self.app_label}:view_{self.model_name}')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.model_name
        context['cancel_url'] = reverse_lazy(f'{self.app_label}:view_{self.model_name}')
        return context

class BaseCreateView(BaseWriteView, CreateView):
    def get_permission_required(self):
        self.app_label = self.model._meta.app_label
        self.model_name = self.model._meta.model_name
        return [f'{self.app_label}.add_{self.model_name}']

class BaseUpdateView(BaseWriteView, UpdateView):
    def get_permission_required(self):
        self.app_label = self.model._meta.app_label
        self.model_name = self.model._meta.model_name
        return [f'{self.app_label}.change_{self.model_name}']

class BaseDeleteView(BaseWriteView, DeleteView):
    def get_permission_required(self):
        self.app_label = self.model._meta.app_label
        self.model_name = self.model._meta.model_name
        return [f'{self.app_label}.delete_{self.model_name}']

