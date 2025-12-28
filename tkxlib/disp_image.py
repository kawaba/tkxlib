"""tkxlib.disp_image - 画像アニメーション表示ヘルパー"""

# --- 必要なライブラリをインポート ---
import tkinter as tk  # GUI作成用の標準ライブラリ（ウィンドウ表示、画像ラベルなど）
from PIL import Image, ImageTk  # Pillowライブラリ。画像処理（Image）とTkinterとの橋渡し（ImageTk）
import time  # アニメーション用に待機時間を入れるための標準ライブラリ
import os  # ファイルの存在確認など、OS関連の処理
from typing import Optional

__all__ = ["dispImg", "dispImg_zoom_rotate", "dispImg_zoom"]

# Pylanceの型チェックに対応するため、画像参照用属性を持つLabelのサブクラスを用意
class ImageLabel(tk.Label):
    image: Optional[ImageTk.PhotoImage] = None

# --- 画像表示のメイン関数 ---
def dispImg(image_path, display_time_ms, display_mode):
    """
    指定された画像を、指定されたモード（ズーム・回転・ズーム+回転）でアニメーション表示する関数

    Args:
        image_path (str): 表示する画像ファイルのパス
        display_time_ms (int): アニメーション表示の合計時間（ミリ秒）
        display_mode (int): 表示モード（1:ズーム, 2:回転, 3:ズーム+回転）
    """

    # ファイルが存在するかチェック（なければエラーメッセージ）
    if not os.path.exists(image_path):
        print(f"エラー: 画像ファイル '{image_path}' が見つかりません。")
        return

    # Pillowを使って画像を読み込み
    try:
        original_image = Image.open(image_path)
    except Exception as e:
        print(f"エラー: 画像の読み込みに失敗しました。{e}")
        return

    # Tkinterのウィンドウ作成
    root = tk.Tk()
    root.title("画像表示")
    root.configure(bg='white')  # 背景色を白に設定

    # 最前面に表示
    root.attributes('-topmost', True)
    root.lift()
    root.focus_force()

    # ウィンドウサイズを画像サイズに応じて決定（最小600x600）
    img_width, img_height = original_image.size
    window_width = max(img_width, 600)
    window_height = max(img_height, 600)

    # ウィンドウを画面中央に配置
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # 画像表示用ラベル（背景も白にする）
    label = ImageLabel(root, bg='white')
    label.pack(expand=True)

    # 表示モードごとに関数を切り替え
    if display_mode == 1:
        zoom_display(root, label, original_image, display_time_ms)
    elif display_mode == 2:
        rotation_display(root, label, original_image, display_time_ms)
    elif display_mode == 3:
        zoom_rotation_display(root, label, original_image, display_time_ms)
    else:
        print("エラー: モードは 1, 2, 3 のいずれかを指定してください。")
        root.destroy()
        return

    # アニメーション後、元の画像を2秒間表示
    final_photo = ImageTk.PhotoImage(original_image)
    label.configure(image=final_photo)
    label.image = final_photo
    root.update()
    time.sleep(2.0)

    # ウィンドウを閉じる
    root.destroy()


def dispImg_zoom_rotate(image_path):
    """画像パスのみ指定でズーム+回転モードを簡単に呼び出す補助関数"""
    default_time_ms = 1000
    default_mode = 3
    dispImg(image_path, default_time_ms, default_mode)

def dispImg_zoom(image_path):
    """画像パスのみ指定でズームを簡単に呼び出す補助関数"""
    default_time_ms = 1000
    default_mode = 1
    dispImg(image_path, default_time_ms, default_mode)

# --- ズームアニメーション関数 ---
def zoom_display(root, label, original_image, display_time_ms):
    steps = 60  # フレーム数
    interval = display_time_ms / steps  # 各フレームの間隔

    img_width, img_height = original_image.size

    for i in range(steps):
        scale = 0.1 + (0.9 * i / (steps - 1))  # 拡大率（0.1倍→1.0倍）
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)

        resized_image = original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(resized_image)
        label.configure(image=photo)
        label.image = photo

        root.update()
        time.sleep(max(interval / 1000.0, 0.01))  # 秒に変換してsleep

# --- 回転アニメーション関数 ---
def rotation_display(root, label, original_image, display_time_ms):
    steps = 120  # フレーム数（3回転分）
    interval = display_time_ms / steps

    for i in range(steps):
        angle = 9 * (i + 1)  # 回転角（9度ずつ）
        rotated_image = original_image.rotate(-angle, expand=True, fillcolor='white')  # 背景白

        photo = ImageTk.PhotoImage(rotated_image)
        label.configure(image=photo)
        label.image = photo

        root.update()
        time.sleep(max(interval / 1000.0, 0.005))

# --- ズーム＋回転アニメーション関数 ---
def zoom_rotation_display(root, label, original_image, display_time_ms):
    steps = 120
    interval = display_time_ms / steps
    img_width, img_height = original_image.size

    for i in range(steps):
        scale = 0.1 + (0.9 * i / (steps - 1))
        angle = 9 * (i + 1)

        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        resized_image = original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        rotated_image = resized_image.rotate(-angle, expand=True, fillcolor='white')  # ★ 修正済み：背景白

        photo = ImageTk.PhotoImage(rotated_image)
        label.configure(image=photo)
        label.image = photo

        root.update()
        time.sleep(max(interval / 1000.0, 0.005))


