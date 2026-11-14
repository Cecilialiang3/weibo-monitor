
import json
import os
from pathlib import Path
from datetime import datetime, timezone

DATA_FILE = Path("seen_posts.json")
CONFIG_FILE = Path("config.json")


def load_seen():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return []


def save_seen(posts):
    DATA_FILE.write_text(
        json.dumps(posts, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def load_config():
    if not CONFIG_FILE.exists():
        print("请先创建 config.json")
        return None

    return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))


def main():
    print("===== Weibo Monitor =====")
    print("启动时间：", datetime.now(timezone.utc).isoformat())

    config = load_config()
    if not config:
        return

    users = config.get("users", [])
    seen = set(load_seen())

    print("监控用户数量：", len(users))

    for user in users:
        uid = str(user.get("uid", "")).strip()
        if not uid:
            continue

        print("等待监控用户：", uid)

    print("当前已记录微博数量：", len(seen))
    print("基础程序运行成功。")
    print("下一步将接入微博公开信息获取。")


if __name__ == "__main__":
    main()
