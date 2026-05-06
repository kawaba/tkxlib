"""tkxlib.disp_image - 画像アニメーション表示ヘルパー"""

import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path
from typing import Optional, Iterator
from dataclasses import dataclass
from enum import IntEnum

__all__ = [
    "dispImg",
    "dispImg_zoom_rotate",
    "dispImg_zoom",
    "zoom_rotate",
    "zoom",
    "DisplayMode",
    "AnimationConfig",
]

class DisplayMode(IntEnum):
    ZOOM = 1
    ROTATION = 2
    ZOOM_ROTATION = 3

@dataclass
class AnimationConfig:
    zoom_steps: int
    rotation_steps: int
    rotation_angle_increment: int
    min_scale: float
    max_scale: float
    min_window_size: int
    final_display_duration: float
    min_interval: float
    default_display_time_ms: int

class WindowState:
    closed: bool
    def __init__(self) -> None: ...

class ImageDisplayManager:
    @classmethod
    def can_display(cls) -> bool: ...
    @classmethod
    def release(cls) -> None: ...

class ImageLabel(tk.Label):
    image: Optional[ImageTk.PhotoImage]

def validate_parameters(display_time_ms: int, display_mode: int) -> None: ...
def load_image(image_path: str | Path) -> Optional[Image.Image]: ...
def setup_window(
    root: tk.Tk,
    image_size: tuple[int, int],
    config: AnimationConfig = ...,
) -> None: ...
def create_zoom_frames(
    original_image: Image.Image,
    steps: int,
    config: AnimationConfig = ...,
) -> Iterator[Image.Image]: ...
def create_rotation_frames(
    original_image: Image.Image,
    steps: int,
    config: AnimationConfig = ...,
) -> Iterator[Image.Image]: ...
def create_zoom_rotation_frames(
    original_image: Image.Image,
    steps: int,
    config: AnimationConfig = ...,
) -> Iterator[Image.Image]: ...
def animate_frames(
    root: tk.Tk,
    label: ImageLabel,
    frames: Iterator[Image.Image],
    display_time_ms: int,
    window_state: WindowState,
    config: AnimationConfig = ...,
) -> None: ...
def display_final_image(
    root: tk.Tk,
    label: ImageLabel,
    original_image: Image.Image,
    window_state: WindowState,
    config: AnimationConfig = ...,
) -> None: ...
def dispImg(
    image_path: str | Path,
    display_time_ms: int,
    display_mode: int,
    config: AnimationConfig = ...,
) -> None: ...
def dispImg_zoom_rotate(
    image_path: str | Path,
    config: AnimationConfig = ...,
) -> None: ...
def dispImg_zoom(
    image_path: str | Path,
    config: AnimationConfig = ...,
) -> None: ...
def zoom_rotate(
    image_path: str | Path,
    config: AnimationConfig = ...,
) -> None: ...
def zoom(
    image_path: str | Path,
    config: AnimationConfig = ...,
) -> None: ...
