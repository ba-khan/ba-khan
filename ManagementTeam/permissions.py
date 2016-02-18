from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

content_type = ContentType.objects.get(app_label='bakhanapp', model='administrator')
permission = Permission.objects.create(codename='isAdmin',
                                       name='Is Admin',
                                       content_type=content_type)
user = User.objects.get(username='utp@lsmb.cl')
group = Group.objects.get(name='administrators')
group.permissions.add(permission)
user.groups.add(group)