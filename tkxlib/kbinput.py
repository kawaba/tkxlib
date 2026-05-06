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
    "get_dict_int",
    "get_dict_float",
    "get_coordinate"
]

# 文字列をカンマで分割し、空でない要素のみのリストにする補助関数
def _row_list(value):
    """カンマ区切り文字列を分割し、空要素を省いたリストを返す。

    引数:
        value (str): 分割対象となるカンマ区切り文字列。

    戻り値:
        list[str]: 空文字を取り除いた項目を格納したリスト。
    """
    # カンマで分割してリストにする
    raw_items = value.split(',')
    
    # 前後の空白を除去し、空でない要素だけを集める
    items = []
    for item in raw_items:
        item = item.strip()
        if item:
            items.append(item)
    
    return items

# intの値を入力する関数(失敗時0)
def get_int(prompt="int>"):
    """整数入力を受け取り、変換に失敗した場合は0を返す。

    引数:
        prompt (str): 入力時に表示するプロンプト文字列。

    戻り値:
        int: 入力文字列を整数化した値。変換できない場合は0。
    """
    try:
        value = input(prompt)
        return int(value)
    except (Exception, KeyboardInterrupt):
        return 0

# floatの値を入力する関数（失敗時0）
def get_float(prompt="float>"):
    """浮動小数点数入力を受け取り、変換失敗時は0.0を返す。

    引数:
        prompt (str): 入力時に表示するプロンプト文字列。

    戻り値:
        float: 入力文字列を浮動小数点数へ変換した値。変換できない場合は0.0。
    """
    try:
        value = input(prompt)
        return float(value)
    except (Exception, KeyboardInterrupt):
        return 0.0

# strの値を入力する関数（常に文字列。空文字はそのまま。例外発生時""）
def get_str(prompt="str>"):
    """文字列入力を取得し、例外発生時は空文字を返す。

    引数:
        prompt (str): 入力時に表示するプロンプト文字列。

    戻り値:
        str: 入力された文字列。例外時は空文字。
    """
    try:
        value = input(prompt)
        return value
    except (Exception, KeyboardInterrupt):
        return ""

# boolの値を入力する関数（y/yes/true/1 => True, n/no/false/0 => False, その他はNone）
def get_bool(prompt="bool>"):
    """真偽値入力を判定し、該当しない場合はNoneを返す。

    引数:
        prompt (str): 入力時に表示するプロンプト文字列。

    戻り値:
        Optional[bool]: 真偽値に変換された結果。判別不可の場合はNone。
    """
    try:
        raw = input(prompt).strip().lower()
    except (Exception, KeyboardInterrupt):
        return None
    truthy = ['y', 'yes', 'true', '1']
    falsy = ['n', 'no', 'false', '0']
    if raw in truthy:
        return True
    if raw in falsy:
        return False
    return None

# 文字列のlistの値を入力する関数（失敗時[]）
def get_list(prompt="CSV>"):
    """カンマ区切り文字列をリスト化し、入力失敗時は空リストを返す。

    引数:
        prompt (str): 入力時に表示するプロンプト文字列。

    戻り値:
        list[str]: 分割された文字列要素。例外発生時は空リスト。
    """
    try:
        value = input(prompt)
        # 文字列を分割して空でない要素のみのリストにする
        items = _row_list(value)
        return items
    except (Exception, KeyboardInterrupt):
        return []

# intのlistの値を入力する関数（要素変換失敗時[]）
def get_list_int(prompt="CSV>"):
    """整数リスト入力を取得し、変換失敗時は空リストを返す。

    引数:
        prompt (str): 入力時に表示するプロンプト文字列。

    戻り値:
        list[int]: 整数に変換された要素を持つリスト。変換できない場合は空リスト。
    """
    try:
        value = input(prompt)
        # まず、文字列を分割して空でない要素のみのリストにする
        items = _row_list(value)
        
        # 各要素を整数に変換する
        result = []
        for item in items:
            result.append(int(item))
        return result
    except (Exception, KeyboardInterrupt):
        return []



# floatのlistの値を入力する関数（要素変換失敗時[]）
def get_list_float(prompt="CSV>"):
    """浮動小数点数リスト入力を取得し、変換失敗時は空リストを返す。

    引数:
        prompt (str): 入力時に表示するプロンプト文字列。

    戻り値:
        list[float]: 浮動小数点数に変換された要素を持つリスト。変換できない場合は空リスト。
    """
    try:
        value = input(prompt)
        # まず、文字列を分割して空でない要素のみのリストにする
        items = _row_list(value)
        
        # 各要素を浮動小数点数に変換する
        result = []
        for item in items:
            result.append(float(item))
        return result
    except (Exception, KeyboardInterrupt):
        return []

# strのtupleの値を入力する関数（失敗時()）
def get_tuple(prompt="CSV>"):
    """文字列のカンマ区切り入力をタプルに変換する。

    引数:
        prompt (str): 入力時に表示するプロンプト文字列。

    戻り値:
        tuple[str, ...]: 入力値を要素に持つタプル。例外時は空タプル。
    """

    items = get_list(prompt)
    return tuple(items)

# intのtupleの値を入力する関数（要素変換失敗時()）
def get_tuple_int(prompt="CSV>"):
    """整数のカンマ区切り入力をタプルに変換する。

    引数:
        prompt (str): 入力時に表示するプロンプト文字列。

    戻り値:
        tuple[int, ...]: 整数に変換された値を持つタプル。例外時は空タプル。
    """

    items = get_list_int(prompt)
    return tuple(items)

# floatのtupleの値を入力する関数（要素変換失敗時()）
def get_tuple_float(prompt="CSV>"):
    """浮動小数点数のカンマ区切り入力をタプルに変換する。

    引数:
        prompt (str): 入力時に表示するプロンプト文字列。

    戻り値:
        tuple[float, ...]: 浮動小数点数に変換された値を持つタプル。例外時は空タプル。
    """
    
    items = get_list_float(prompt)
    return tuple(items)

# strのsetの値を入力する関数（失敗時set{}）
def get_set(prompt="CSV>"):
    """文字列のカンマ区切り入力を集合に変換する。

    引数:
        prompt (str): 入力時に表示するプロンプト文字列。

    戻り値:
        set[str]: 入力値を要素に持つ集合。例外時は空集合。
    """

    items = get_list(prompt)
    return set(items)

# intのsetの値を入力する関数（要素変換失敗時set{}）
def get_set_int(prompt="CSV>"):
    """整数のカンマ区切り入力を集合に変換する。

    引数:
        prompt (str): 入力時に表示するプロンプト文字列。

    戻り値:
        set[int]: 整数に変換された値を持つ集合。例外時は空集合。
    """

    items = get_list_int(prompt)
    return set(items)

# floatのsetの値を入力する関数（要素変換失敗時set{}）
def get_set_float(prompt="CSV>"):
    """浮動小数点数のカンマ区切り入力を集合に変換する。

    引数:
        prompt (str): 入力時に表示するプロンプト文字列。

    戻り値:
        set[float]: 浮動小数点数に変換された値を持つ集合。例外時は空集合。
    """

    items = get_list_float(prompt)
    return set(items)

# dictの値を入力する関数（形式不正時 {} ）
def get_dict(prompt="CSV (k:v)>"):
    """キーと値をコロン区切りで受け取り、文字列辞書に変換する。

    引数:
        prompt (str): 入力時に表示するプロンプト文字列。

    戻り値:
        dict[str, str]: 変換に成功したキーと値の辞書。形式不正時は空辞書。
    """
    try:
        value  = input(prompt)

        # 文字列を分割して空でない要素のみのリストにする
        items =  _row_list(value)

        result = {}
        for item in items:
            if ':' not in item:
                return {}
            try:
                key, val = item.split(':', 1)
            except (Exception):
                return {}
            result[key.strip()] = val.strip()
        return result
    except (Exception, KeyboardInterrupt):
        return {}

# intの値を持つdictを入力する関数（値の変換失敗時 {} ）
def get_dict_int(prompt="CSV (k:v)>"):
    """値を整数に変換した辞書を生成し、失敗時は空辞書を返す。

    引数:
        prompt (str): 入力時に表示するプロンプト文字列。

    戻り値:
        dict[str, int]: 整数に変換された値を持つ辞書。変換失敗時は空辞書。
    """
    # まず文字列のdictを取得
    str_dict = get_dict(prompt)
    
    # 各値を整数に変換する
    result = {}
    try:
        for key, val in str_dict.items():
            result[key] = int(val)
        return result
    except (Exception, KeyboardInterrupt):
        return {}

# floatの値を持つdictを入力する関数（値の変換失敗時 {} ）
def get_dict_float(prompt="CSV (k:v)>"):
    """値を浮動小数点数に変換した辞書を生成し、失敗時は空辞書を返す。

    引数:
        prompt (str): 入力時に表示するプロンプト文字列。

    戻り値:
        dict[str, float]: 浮動小数点数に変換された値を持つ辞書。変換失敗時は空辞書。
    """
    # まず文字列のdictを取得
    str_dict = get_dict(prompt)

    # 各値を浮動小数点数に変換する
    result = {}
    try:
        for key, val in str_dict.items():
            result[key] = float(val)
        return result
    except (Exception, KeyboardInterrupt):
        return {}

# x, y 座標をfloatのタプルで入力する関数（正しい入力がされるまで繰り返す）
def get_coordinate(prompt="x, y > "):
    """座標(x, y)をfloatのタプルとして入力する。正しい入力がされるまで繰り返す。

    「x, y」形式でコンマ区切りの2つの浮動小数点数を入力する。
    floatに変換できない文字（空白文字以外）がある場合や、
    要素数が2つでない場合は再入力を促す。

    引数:
        prompt (str): 入力時に表示するプロンプト文字列。

    戻り値:
        tuple[float, float]: 入力されたx, y座標のタプル。
    """
    while True:
        try:
            value = input(prompt)
        except (Exception, KeyboardInterrupt):
            continue

        items = _row_list(value)

        if len(items) != 2:
            continue

        try:
            x = float(items[0])
            y = float(items[1])
        except ValueError:
            continue

        return (x, y)
