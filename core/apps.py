from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    
    def ready(self) -> None:
        from django.conf import settings
        from conversor import urls
        from . import urls as url_core
        import os
        from pathlib import Path
        from django.conf.urls.static import static
        
        # Define Variables in Settings
        if settings.DEBUG:
            if not settings.STATIC_URL:
                settings.STATIC_URL = "/assets/"
            if not settings.STATIC_ROOT:
                settings.STATIC_ROOT = os.path.join(settings.BASE_DIR, 'assets')
            if not settings.STATICFILES_DIRS:
                settings.STATICFILES_DIRS.append(os.path.join(settings.BASE_DIR, '.static'))
        print(settings.STATICFILES_DIRS)
        if url_core.urlpatterns not in urls.urlpatterns:
            urls.urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
            urls.urlpatterns += url_core.urlpatterns
        if settings.TEMPLATES[0]:
            if settings.DEBUG:
                settings.TEMPLATES[0].get("DIRS").append(".templates")
        Path(os.path.join(settings.BASE_DIR),".templates").mkdir(parents=True,exist_ok=True)
        Path(os.path.join(settings.BASE_DIR),".static").mkdir(parents=True,exist_ok=True)
        return super().ready()
