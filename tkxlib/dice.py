"""サイコロアニメーションを提供するモジュール"""

import random
from importlib import resources

import tkxlib as tkx


def dice() -> int:
    """サイコロを振り、表示後に出目を返す。

    引数:
        なし
    戻り値:
        int: サイコロの出目。
    """

    rd = random.randint(1, 6)  # 1から6までの乱数を取得
    resource_path = resources.files("tkxlib").joinpath("img", f"d-{rd}.png")

    try:
        # importlib.resources 経由で絶対パスを取得し、zip配布でも正しく動作させる
        with resources.as_file(resource_path) as img_path:
            tkx.dispImg_zoom_rotate(str(img_path))
    except FileNotFoundError as exc:
        raise RuntimeError("サイコロ画像ファイルが見つかりません。") from exc
    except Exception as exc:  # 表示処理での予期せぬ例外を捕捉
        raise RuntimeError("サイコロ画像の表示に失敗しました。") from exc

    return rd
