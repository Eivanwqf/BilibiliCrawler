import requests
import time

import os
os.environ['NO_PROXY'] = '*' #这个部分是要跳过代理（如果有科学上网）

def monitor_bili_season(aid):
    # 简化版的 URL，去掉那些乱七八糟的指纹
    url = "https://api.bilibili.com/x/web-interface/view/detail" #调用bilibili的API
    params = {
        "aid": aid,
        "need_view": 1 #这个我也不知道为什么需要挂上，貌似不挂也没问题？谁知道当时是怎么想的。
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
        'Cookie': "buvid3=47EF8E79-1830-3F30-D2FC-D333846664BB72668infoc; b_nut=1770867872; _uuid=484CEEEA-52310-F49A-1047C-ACD2CF4B286E77712infoc; buvid_fp=b19f2b28de3a901e23b0cf8bb4284484; buvid4=9844F7A5-3ED4-0D88-FE95-3BB5CF8844D674860-026021211-QsI0/kvCbWc/WDw76R1qRg%3D%3D; SESSDATA=d62253e4%2C1786420001%2C77544%2A21CjBGYpM0CB08g3BjVm-s8k8f02wqpN8wK3KdWKqBk2p7-fKnUyRogr7KUE-jVUusKucSVjduSXFvcE5GMmZyZHFoaDI4YnRUaFJaUEZKTTJWOGdKMnhpTzM5MG04US1zVEVwa1B6VlA2M19HaFpOQ0JhNzQ5X2Q3ZkZ4YV92eDhtUlhoMGhBdmpBIIEC; bili_jct=5c17822fd3c84c19b6dae9c702bc7ee6; DedeUserID=44931775; DedeUserID__ckMd5=f731a2071ba2042a; theme-tip-show=SHOWED; rpdid=|(u~J~|mRmYl0J'u~~|)~YJYk; theme-avatar-tip-show=SHOWED; CURRENT_QUALITY=80; hit-dyn-v2=1; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzI4MTU2MTUsImlhdCI6MTc3MjU1NjM1NSwicGx0IjotMX0.zZvA21YHi76DSkRBi7ql9hkmOGdOX5gszNz_F3HZYAw; bili_ticket_expires=1772815555; home_feed_column=5; sid=8cj3v28r; browser_resolution=1920-911; bp_t_offset_44931775=1176182952992702464; CURRENT_FNVAL=2000; b_lsid=557B6809_19CBCF12A54",
        'Accept': 'application/json, text/plain, */*',
        "Referer": f"https://www.bilibili.com/video/av{aid}"
    } #欺骗性行为

    try:
        response = requests.get(url, params=params, headers=headers) #拿到response
        res_json = response.json() #解析为json

        if res_json['code'] == 0:
            # 数据在 data -> View -> ugc_season 里
            view_data = res_json['data']['View']
            season = view_data.get('ugc_season')

            if not season:
                print("该视频不属于合集。")
                return

            print(f"合集名称：{season['title']}")
            # 遍历合集中的所有视频
            episodes = season['sections'][0]['episodes']

            for ep in episodes:
                title = ep['title']
                stat = ep['arc']['stat']  # 这里包含了实时播放量、收藏等
                print(f"视频: {title} (av号: {aid})")
                print(f"  └─ 播放: {stat['view']} | 弹幕：{stat['danmaku']} | 回复：{stat['reply']} | 收藏: {stat['fav']} | 投币: {stat['coin']} | 点赞: {stat['like']} | 分享：{stat['share']}")
        else:
            print(f"请求失败，错误码: {res_json['code']}, 消息: {res_json['message']}")

    except Exception as e:
        print(f"发生异常: {e}")


# 测试运行
monitor_bili_season(114233496901063)