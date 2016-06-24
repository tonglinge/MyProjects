from django.contrib import admin
from chatroom import models
# Register your models here.


class UserGroupAdmin(admin.ModelAdmin):
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        #print(request.user)
        if db_field.name == "members":
            kwargs["queryset"] = models.LoginUser.objects.filter(user=request.user).first().friends
            #print(kwargs)
        return super(UserGroupAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


admin.site.register(models.LoginUser)
admin.site.register(models.UserGroup, UserGroupAdmin)
admin.site.register(models.WebGroups)
