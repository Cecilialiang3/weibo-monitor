
import json
import re
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

CONFIG_FILE = "config.json"


def main():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = json.load(f)

    user = config["users"][0]
    uid = str(user["uid"])

    url = f"https://weibo.com/u/{uid}"

    print("===== 微博公开主页访问测试 =====")
    print("监控 UID:", uid)
    print("正在访问:", url)

    request = Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 "
                "like Mac OS X) AppleWebKit/605.1.15 "
                "Version/17.0 Mobile/15E148 Safari/604.1"
            ),
            "Accept-Language": "zh-CN,zh;q=0.9"
        }
    )

    try:
        with urlopen(request, timeout=20) as response:
            html = response.read(1000000).decode(
                "utf-8", errors="ignore"
            )

            title = re.search(
                r"<title[^>]*>(.*?)</title>",
                html,
                re.I | re.S
            )

            print("HTTP状态:", response.status)
            print("最终地址:", response.url)
            print("网页标题:", title.group(1).strip() if title else "未找到")
            print("页面长度:", len(html))
            print("是否包含目标UID:", uid in html)

            if response.status == 200:
                print("公开页面访问成功，等待进一步检查数据。")

    except HTTPError as e:
        print("HTTP错误:", e.code)
        print("微博可能限制了当前访问。")

    except URLError as e:
        print("网络访问失败:", e.reason)

    except Exception as e:
        print("程序错误:", str(e))


if __name__ == "__main__":
    main()
