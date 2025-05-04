from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, DateTimeWidget
from .models import Task
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskResource(resources.ModelResource):
    user = fields.Field(
        column_name='user',
        attribute='user',
        widget=ForeignKeyWidget(User, 'username')
    )
    
    class Meta:
        model = Task
        fields = ('id', 'user', 'title', 'description', 'completed', 'created_at')
        import_id_fields = ['id']
        skip_unchanged = True
        report_skipped = True
        use_bulk = True  # Enable bulk operations

    def before_import_row(self, row, **kwargs):
        """Force current user for all imported rows"""
        row['user'] = kwargs['user'].username
        
    def get_instance(self, instance_loader, row):
        """Enable updates for existing tasks"""
        return super().get_instance(instance_loader, row)

    def save_instance(self, instance, using_transactions=True, dry_run=False):
        """Custom save with user validation"""
        if not dry_run:
            instance.user = self.user
            super().save_instance(instance, using_transactions, dry_run)