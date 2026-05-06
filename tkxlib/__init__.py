"""tkxlib - 画像表示・入力・サイコロヘルパー"""

from .disp_image import dispImg, dispImg_zoom, dispImg_zoom_rotate, zoom, zoom_rotate
from .kbinput import (
	get_bool,
	get_coordinate,
	get_dict,
	get_dict_float,
	get_dict_int,
	get_float,
	get_int,
	get_list,
	get_list_float,
	get_list_int,
	get_set,
	get_set_float,
	get_set_int,
	get_str,
	get_tuple,
	get_tuple_float,
	get_tuple_int,
)
from .dice import dice

__all__ = [
	"dispImg",
	"dispImg_zoom",
	"dispImg_zoom_rotate",
	"zoom",
	"zoom_rotate",
	"get_bool",
	"get_coordinate",
	"get_dict",
	"get_dict_float",
	"get_dict_int",
	"get_float",
	"get_int",
	"get_list",
	"get_list_float",
	"get_list_int",
	"dice",
	"get_set",
	"get_set_float",
	"get_set_int",
	"get_str",
	"get_tuple",
	"get_tuple_float",
	"get_tuple_int",
]

__version__ = "2.0.1"
__download_url__ = "https://k-webs.jp/python/lib/"

