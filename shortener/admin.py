from django.contrib import admin

from coin32_test.logger import log_info

from .models import ShortUrls


class ShortUrlsAdmin(admin.ModelAdmin):
    model = ShortUrls

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            msg = obj.create_log_message()
            log_info(f'Удален сокращенный URL. {msg}')

        super().delete_queryset(request, queryset)

    def delete_model(self, request, obj):
        msg = obj.create_log_message()
        log_info(f'Удален сокращенный URL. {msg}')

        super().delete_model(request, obj)


admin.site.register(ShortUrls, ShortUrlsAdmin)
