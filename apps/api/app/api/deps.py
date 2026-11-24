from app.core.config import settings
from app.storage import LocalStorage


def get_storage() -> LocalStorage:
    return LocalStorage(settings.storage_dir)
