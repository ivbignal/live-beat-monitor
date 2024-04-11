from contextvars import ContextVar
from pathlib import Path

from utils.track import Track

perform_mode: ContextVar[bool] = ContextVar('perform_mode', default=False)
show_directory_path: ContextVar[Path | None] = ContextVar('show_directory_path', default=None)
tracks: ContextVar[list[Track]] = ContextVar('tracks', default=[])
current_track: ContextVar[int] = ContextVar('current_track', default=0)


def get_show_name():
    path = show_directory_path.get()
    name = 'No current show'

    if path and path.is_dir():
        name = path.name

    return name
