"""tkxlib.kbinput - 入力ヘルパー関数集"""

__all__ = [
    "get_int",
    "get_float",
    "get_str",
    "get_bool",
    "get_list",
    "get_list_int",
    "get_list_float",
    "get_tuple",
    "get_tuple_int",
    "get_tuple_float",
    "get_set",
    "get_set_int",
    "get_set_float",
    "get_dict",
]

# intの値を入力する関数(失敗時0)
def get_int(prompt="int>"):
    value = input(prompt)
    try:
        return int(value)
    except Exception:
        return 0

# floatの値を入力する関数（失敗時0）
def get_float(prompt="float>"):
    value = input(prompt)
    try:
        return float(value)
    except Exception:
        return 0.0

# strの値を入力する関数（常に文字列。空文字はそのまま。例外発生時None）
def get_str(prompt="str>"):
    try:
        value = input(prompt)
        return value
    except Exception:
        return None

# boolの値を入力する関数（y/yes/true/1 => True, n/no/false/0 => False, その他はNone）
def get_bool(prompt="bool>"):
    try:
        raw = input(prompt).strip().lower()
    except Exception:
        return None
    truthy = ['y', 'yes', 'true', '1']
    falsy = ['n', 'no', 'false', '0']
    if raw in truthy:
        return True
    if raw in falsy:
        return False
    return None

# 文字列のlistの値を入力する関数（失敗時None）
def get_list(prompt="CSV>"):
    try:
        value = input(prompt)
        return [item.strip() for item in value.split(',')]
    except Exception:
        return None

# intのlistの値を入力する関数（要素変換失敗時None）
def get_list_int(prompt="CSV>"):
    try:
        value = input(prompt)
        result = []
        for item in value.split(','):
            try:
                result.append(int(item.strip()))
            except Exception:
                return None
        return result
    except Exception:
        return None

# floatのlistの値を入力する関数（要素変換失敗時None）
def get_list_float(prompt="CSV>"):
    try:
        value = input(prompt)
        result = []
        for item in value.split(','):
            try:
                result.append(float(item.strip()))
            except Exception:
                return None
        return result
    except Exception:
        return None

# strのtupleの値を入力する関数（失敗時None）
def get_tuple(prompt="CSV>"):
    try:
        value = input(prompt)
        return tuple(item.strip() for item in value.split(','))
    except Exception:
        return None

# intのtupleの値を入力する関数（要素変換失敗時None）
def get_tuple_int(prompt="CSV>"):
    try:
        value = input(prompt)
        converted = []
        for item in value.split(','):
            try:
                converted.append(int(item.strip()))
            except Exception:
                return None
        return tuple(converted)
    except Exception:
        return None

# floatのtupleの値を入力する関数（要素変換失敗時None）
def get_tuple_float(prompt="CSV>"):
    try:
        value = input(prompt)
        converted = []
        for item in value.split(','):
            try:
                converted.append(float(item.strip()))
            except Exception:
                return None
        return tuple(converted)
    except Exception:
        return None

# strのsetの値を入力する関数（失敗時None）
def get_set(prompt="CSV>"):
    try:
        value = input(prompt)
        return set(item.strip() for item in value.split(','))
    except Exception:
        return None

# intのsetの値を入力する関数（要素変換失敗時None）
def get_set_int(prompt="CSV>"):
    try:
        value = input(prompt)
        converted = set()
        for item in value.split(','):
            try:
                converted.add(int(item.strip()))
            except Exception:
                return None
        return converted
    except Exception:
        return None

# floatのsetの値を入力する関数（要素変換失敗時None）
def get_set_float(prompt="CSV>"):
    try:
        value = input(prompt)
        converted = set()
        for item in value.split(','):
            try:
                converted.add(float(item.strip()))
            except Exception:
                return None
        return converted
    except Exception:
        return None

# dictの値を入力する関数（形式不正時None）
def get_dict(prompt="CSV (k:v)>"):
    try:
        value  = input(prompt)
        items = [item.strip() for item in value.split(',') if item.strip()]
        result = {}
        for item in items:
            if ':' not in item:
                return None
            try:
                key, val = item.split(':', 1)
            except Exception:
                return None
            result[key.strip()] = val.strip()
        return result
    except Exception:
        return None
