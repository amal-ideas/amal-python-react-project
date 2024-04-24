from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Avg

# Register your models here.
from . import models
from django import forms


class TestimonialAdminForm(forms.ModelForm):
    class Meta:
        model = models.PartyTestimonial
        fields = "__all__"

    def clean_rating(self):
        if self.cleaned_data["rating"] >     5:
            raise forms.ValidationError("Rating is out of 5. Please rate the party within the range of 1-5!")

        return self.cleaned_data["rating"]


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "userID", "create_at")
    list_filter = ("create_at", "partyID")
    search_fields = ("title__startswith",)
    fields = ("title", "description", "userID", "partyID", "locationID", "picture", "postTag")

@admin.register(models.Comment)
class PostAdmin(admin.ModelAdmin):
    list_display = ("user", "postDate")
    fields = ("user", "postID", "content")


@admin.register(models.PostReaction)
class PostAdmin(admin.ModelAdmin):
    list_display = ("postId", "Total_support", "Total_unsupport")

    def Total_support(self, obj):
        count = obj.supportCnt.count()
        return format_html('{} Users', count)

    def Total_unsupport(self, obj):
        count = obj.unSupportCnt.count()
        return format_html('{} Users', count)


@admin.register(models.Party)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "Total_posts", "Testimonials", "rating")
    search_fields = ("title__startswith",)
    fields = ("title", "description",)

    def Total_posts(self, obj):
        count = models.Post.objects.filter(partyID=obj).count()
        return format_html('{}', count)

    def Testimonials(self, obj):
        count = models.PartyTestimonial.objects.filter(party=obj).count()
        return format_html('{}', count)

    def rating(self, obj):
        from django.utils.html import format_html

        result = models.PartyTestimonial.objects.filter(party=obj).aggregate(Avg("rating"))
        return format_html("<b><i>{}</i></b>", result["rating__avg"])


@admin.register(models.Location)
class PostAdmin(admin.ModelAdmin):
    list_display = ("name", "shortName")


@admin.register(models.Tag)
class PostAdmin(admin.ModelAdmin):
    list_display = ("name", )
    search_fields = ("name__startswith",)


@admin.register(models.UserInfo)
class PostAdmin(admin.ModelAdmin):
    list_display = ("user", "address", "status", "Total_posted")
    search_fields = ("user__username__startswith",)

    def Total_posted(self, obj):
        count = models.Post.objects.filter(userID=obj).count()
        return format_html('{} Posts', count)


@admin.register(models.UserTag)
class PostAdmin(admin.ModelAdmin):
    list_display = ("tagId",)


@admin.register(models.PartyTestimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "party", "created", "lastmodified")
    list_filter = ("created",)
    search_fields = ("title__startswith",)
    form = TestimonialAdminForm

@admin.register(models.Status)
class PostAdmin(admin.ModelAdmin):
    list_display = ("label",)
