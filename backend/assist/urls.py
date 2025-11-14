from django.urls import path
from .views import assist_apply, assist_thanks, school_app_dashboard, forward_all, forward_one

app_name = "assist"

urlpatterns = [
    # Public parent application (link from WhatsApp)
    path("assist/apply", assist_apply, name="assist_apply"),
    path("assist/thanks", assist_thanks, name="assist_thanks"),

    # School admin dashboard
    path("assist/admin", school_app_dashboard, name="school_app_dashboard"),
    path("assist/admin/forward-all", forward_all, name="forward_all"),
    path("assist/admin/forward/<int:app_id>", forward_one, name="forward_one"),
]
