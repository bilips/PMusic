# 导入
import eel
import json
from requests_html import HTMLSession

# 暴露函数
@eel.expose
def search(music_name):
    session = HTMLSession()
    url = "https://cn.bing.com/search?q=site:music.163.com %s 单曲" % music_name
    headers= {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-Hans-CN,zh-Hans;q=0.8,en-US;q=0.5,en;q=0.3",
        "Host": "cn.bing.com",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    html = session.get(url=url, headers=headers).html
    links = html.find("a")
    urls = []
    for link in links:
        if "href" in link.attrs:
            if "song?id=" in link.attrs["href"]:
                urls.append(link.attrs["href"])
    return urls

@eel.expose
def get_data(urls):
    audio = []
    for url in urls:
        info = {
            "name": '',
            "artist": '',
            "url": '',
            "cover": '',
            "lrc": ''
        }
        id = url.replace("https://music.163.com/song?id=", "")
        session = HTMLSession()
        headers= {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-Hans-CN,zh-Hans;q=0.8,en-US;q=0.5,en;q=0.3",
            "Host": "music.163.com",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0"
        }
        try:
            html = session.get(url=url, headers=headers).html
            # 歌曲名称&歌手
            title = html.find("title")[0].text.split(" - ")
            info["name"] = title[0]
            info["artist"] = title[1]
            # 下载地址
            info["url"] = "http://music.163.com/song/media/outer/url?id=%s.mp3" % id
            # 歌词
            try:
                lrc = session.get(url="http://music.163.com/api/song/media?id=%s" % id, headers=headers).html.html
                js = json.loads(lrc)
                if "lyric" in js:
                    info["lrc"] = js["lyric"]
                else:
                    info["lrc"] = "[00:00.00]纯音乐，请欣赏"
            except:
                print("ID为:%s的歌曲歌词获取失败!" % id)
            # 图片
            img = html.find("img")[0]
            info["cover"] = img.attrs["src"]
            # 载入
            audio.append(info)
        except:
            print("Url为%s的歌曲获取错误!" % url)
    return audio

# 初始化
eel.init("web")
eel.start("index.html", size=(800, 450))
