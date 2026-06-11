from django.db import models


class TgMessageCache(models.Model):
    """Tracks the last bot message id(s) per Telegram chat so old
    registration-confirmation messages can be deleted before sending new ones.
    Stored in the DB (not a temp file) so it survives restarts and works
    across the web dyno and the bot process.
    """
    chat_id = models.CharField(max_length=32, unique=True)
    message_ids = models.JSONField(default=list, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.chat_id}: {self.message_ids}"
