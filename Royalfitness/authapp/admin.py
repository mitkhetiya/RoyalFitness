from django.contrib import admin
from authapp.models import Enrollment
from authapp.models import Trainer
from authapp.models import MembershipPlan
from authapp.models import Contact
from authapp.models import Gallery
from authapp.models import Attendance
from authapp.models import about
from authapp.models import services
from authapp.models import free_trial


# Register your models here.
admin.site.register(Contact)
admin.site.register(Enrollment)
admin.site.register(Trainer)
admin.site.register(MembershipPlan)
admin.site.register(Gallery)
admin.site.register(Attendance)
admin.site.register(free_trial)
