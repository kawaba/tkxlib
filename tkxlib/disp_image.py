"""
tkxlib.disp_image - 画像アニメーション表示ヘルパー (改善版)

開発中(編集を即反映させたい場合):
    python -m pip install -e .

配布用パッケージのビルド:
    python -m build
"""

import tkinter as tk
from PIL import Image, ImageTk
import time
import os
import logging
import threading
from pathlib import Path
from typing import Optional, Dict, Callable
from dataclasses import dataclass
from enum import IntEnum

__all__ = [
    "dispImg", 
    "dispImg_zoom_rotate", 
    "dispImg_zoom", 
    "zoom_rotate", 
    "zoom",
    "DisplayMode",
    "AnimationConfig"
]

# ロガーの設定
logger = logging.getLogger(__name__)

# 定数定義
class DisplayMode(IntEnum):
    """表示モードの列挙型"""
    ZOOM = 1
    ROTATION = 2
    ZOOM_ROTATION = 3

@dataclass
class AnimationConfig:
    """アニメーション設定"""
    zoom_steps: int = 60
    rotation_steps: int = 120
    rotation_angle_increment: int = 9
    min_scale: float = 0.1
    max_scale: float = 1.0
    min_window_size: int = 600
    final_display_duration: float = 0.5
    min_interval: float = 0.005
    default_display_time_ms: int = 1000

# デフォルト設定
DEFAULT_CONFIG = AnimationConfig()

class WindowState:
    """ウィンドウ状態管理クラス"""
    def __init__(self):
        self.closed = False

class ImageDisplayManager:
    """画像表示の排他制御を管理するクラス"""
    _lock = threading.Lock()
    _window_active = False
    
    @classmethod
    def can_display(cls) -> bool:
        """表示可能かチェックし、可能ならアクティブ化"""
        with cls._lock:
            if cls._window_active:
                return False
            cls._window_active = True
            return True
    
    @classmethod
    def release(cls) -> None:
        """アクティブ状態を解除"""
        with cls._lock:
            cls._window_active = False

class ImageLabel(tk.Label):
    """画像参照用属性を持つLabelのサブクラス"""
    image: Optional[ImageTk.PhotoImage] = None

def validate_parameters(display_time_ms: int, display_mode: int) -> None:
    """パラメータの検証
    
    Args:
        display_time_ms: 表示時間(ミリ秒)
        display_mode: 表示モード
        
    Raises:
        ValueError: パラメータが不正な場合
    """
    if display_time_ms <= 0:
        raise ValueError(f"display_time_msは正の値である必要があります: {display_time_ms}")
    
    try:
        DisplayMode(display_mode)
    except ValueError:
        raise ValueError(f"display_modeは1, 2, 3のいずれかである必要があります: {display_mode}")

def load_image(image_path: str | Path) -> Optional[Image.Image]:
    """画像を読み込む
    
    Args:
        image_path: 画像ファイルのパス
        
    Returns:
        読み込んだ画像、失敗時はNone
    """
    path = Path(image_path)
    
    if not path.exists():
        logger.error(f"画像ファイル '{path}' が見つかりません。")
        return None
    
    try:
        return Image.open(path)
    except Exception as e:
        logger.error(f"画像の読み込みに失敗しました: {e}")
        return None

def setup_window(root: tk.Tk, image_size: tuple[int, int], 
                 config: AnimationConfig = DEFAULT_CONFIG) -> None:
    """ウィンドウの初期設定
    
    Args:
        root: Tkinterルートウィンドウ
        image_size: 画像サイズ (width, height)
        config: アニメーション設定
    """
    root.title("画像表示")
    root.configure(bg='white')
    
    # ウィンドウサイズの決定
    img_width, img_height = image_size
    window_width = max(img_width, config.min_window_size)
    window_height = max(img_height, config.min_window_size)
    
    # 画面中央に配置
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # 最前面に表示
    root.attributes('-topmost', True)
    root.lift()
    root.focus_force()

def create_zoom_frames(original_image: Image.Image, steps: int, 
                       config: AnimationConfig = DEFAULT_CONFIG):
    """ズームアニメーション用のフレームを生成
    
    Args:
        original_image: 元画像
        steps: フレーム数
        config: アニメーション設定
        
    Yields:
        各フレームの画像
    """
    img_width, img_height = original_image.size
    scale_range = config.max_scale - config.min_scale
    
    for i in range(steps):
        scale = config.min_scale + (scale_range * i / (steps - 1))
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        yield original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

def create_rotation_frames(original_image: Image.Image, steps: int,
                           config: AnimationConfig = DEFAULT_CONFIG):
    """回転アニメーション用のフレームを生成
    
    Args:
        original_image: 元画像
        steps: フレーム数
        config: アニメーション設定
        
    Yields:
        各フレームの画像
    """
    for i in range(steps):
        angle = config.rotation_angle_increment * (i + 1)
        yield original_image.rotate(-angle, expand=True, fillcolor='white')

def create_zoom_rotation_frames(original_image: Image.Image, steps: int,
                                config: AnimationConfig = DEFAULT_CONFIG):
    """ズーム+回転アニメーション用のフレームを生成
    
    Args:
        original_image: 元画像
        steps: フレーム数
        config: アニメーション設定
        
    Yields:
        各フレームの画像
    """
    img_width, img_height = original_image.size
    scale_range = config.max_scale - config.min_scale
    
    for i in range(steps):
        scale = config.min_scale + (scale_range * i / (steps - 1))
        angle = config.rotation_angle_increment * (i + 1)
        
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        resized_image = original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        yield resized_image.rotate(-angle, expand=True, fillcolor='white')

def animate_frames(root: tk.Tk, label: ImageLabel, frames, 
                   display_time_ms: int, window_state: WindowState,
                   config: AnimationConfig = DEFAULT_CONFIG) -> None:
    """フレームをアニメーション表示
    
    Args:
        root: Tkinterルートウィンドウ
        label: 画像表示ラベル
        frames: 表示するフレームのジェネレータ
        display_time_ms: 表示時間(ミリ秒)
        window_state: ウィンドウ状態
        config: アニメーション設定
    """
    frames_list = list(frames)
    steps = len(frames_list)
    interval = display_time_ms / steps if steps > 0 else 0
    
    for frame_image in frames_list:
        if window_state.closed:
            break
        
        photo = ImageTk.PhotoImage(frame_image)
        
        try:
            label.configure(image=photo)
            label.image = photo
            root.update()
        except tk.TclError:
            window_state.closed = True
            break
        
        time.sleep(max(interval / 1000.0, config.min_interval))

def display_final_image(root: tk.Tk, label: ImageLabel, 
                       original_image: Image.Image, window_state: WindowState,
                       config: AnimationConfig = DEFAULT_CONFIG) -> None:
    """最終的な元画像を表示
    
    Args:
        root: Tkinterルートウィンドウ
        label: 画像表示ラベル
        original_image: 元画像
        window_state: ウィンドウ状態
        config: アニメーション設定
    """
    if not window_state.closed:
        try:
            final_photo = ImageTk.PhotoImage(original_image)
            label.configure(image=final_photo)
            label.image = final_photo
            root.update()
            time.sleep(config.final_display_duration)
        except tk.TclError:
            pass

def dispImg(image_path: str | Path, display_time_ms: int, display_mode: int,
            config: AnimationConfig = DEFAULT_CONFIG) -> None:
    """指定された画像を、指定されたモードでアニメーション表示する関数

    Args:
        image_path: 表示する画像ファイルのパス
        display_time_ms: アニメーション表示の合計時間(ミリ秒)
        display_mode: 表示モード(1:ズーム, 2:回転, 3:ズーム+回転)
        config: アニメーション設定(オプション)
        
    Raises:
        ValueError: パラメータが不正な場合
    """
    # パラメータ検証
    validate_parameters(display_time_ms, display_mode)
    
    # 重複実行チェック
    if not ImageDisplayManager.can_display():
        logger.warning("既に画像が表示中です。前の表示が終了してから再度実行してください。")
        return
    
    try:
        # 画像読み込み
        original_image = load_image(image_path)
        if original_image is None:
            return
        
        # フレーム生成関数の選択
        frame_generators: Dict[int, Callable] = {
            DisplayMode.ZOOM: lambda: create_zoom_frames(
                original_image, config.zoom_steps, config),
            DisplayMode.ROTATION: lambda: create_rotation_frames(
                original_image, config.rotation_steps, config),
            DisplayMode.ZOOM_ROTATION: lambda: create_zoom_rotation_frames(
                original_image, config.rotation_steps, config),
        }
        
        # ウィンドウ作成
        root = tk.Tk()
        window_state = WindowState()
        
        # ウィンドウ設定
        setup_window(root, original_image.size, config)
        
        # クローズハンドラ
        def on_closing():
            window_state.closed = True
            root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        # 画像表示用ラベル
        label = ImageLabel(root, bg='white')
        label.pack(expand=True)
        
        # アニメーション実行
        frames_gen = frame_generators[display_mode]()
        animate_frames(root, label, frames_gen, display_time_ms, window_state, config)
        
        # 最終画像表示
        display_final_image(root, label, original_image, window_state, config)
        
        # ウィンドウクローズ
        if not window_state.closed:
            root.destroy()
            
    finally:
        ImageDisplayManager.release()

# 便利関数群
def dispImg_zoom_rotate(image_path: str | Path, 
                       config: AnimationConfig = DEFAULT_CONFIG) -> None:
    """画像パスのみ指定でズーム+回転モードを簡単に呼び出す補助関数

    Args:
        image_path: 表示する画像ファイルのパス
        config: アニメーション設定(オプション)
    """
    dispImg(image_path, config.default_display_time_ms, DisplayMode.ZOOM_ROTATION, config)

def dispImg_zoom(image_path: str | Path,
                config: AnimationConfig = DEFAULT_CONFIG) -> None:
    """画像パスのみ指定でズームを簡単に呼び出す補助関数

    Args:
        image_path: 表示する画像ファイルのパス
        config: アニメーション設定(オプション)
    """
    dispImg(image_path, config.default_display_time_ms, DisplayMode.ZOOM, config)

def zoom_rotate(image_path: str | Path,
               config: AnimationConfig = DEFAULT_CONFIG) -> None:
    """`dispImg_zoom_rotate` の短縮エイリアス

    Args:
        image_path: 表示する画像ファイルのパス
        config: アニメーション設定(オプション)
    """
    dispImg_zoom_rotate(image_path, config)

def zoom(image_path: str | Path,
        config: AnimationConfig = DEFAULT_CONFIG) -> None:
    """`dispImg_zoom` の短縮エイリアス

    Args:
        image_path: 表示する画像ファイルのパス
        config: アニメーション設定(オプション)
    """
    dispImg_zoom(image_path, config)
