# -*- coding:utf-8 -*-
# @Time : 2021/3/1 16:38
# @Author: xinxu
# @File : google_translate.py

import re
import urllib.parse
import urllib.request

import execjs

"""
source from https://www.pythonf.cn/read/150400
"""
# 谷歌翻译
class Py4Js():
    def __init__(self):
        self.ctx = execjs.compile("""
        function TL(a) {
        var k = "";
        
        
        var b = 406644;
        var b1 = 3293161072;
        var jd = ".";
        var $b = "+-a^+6";
        var Zb = "+-3^+b+-f";
        for (var e = [], f = 0, g = 0; g < a.length; g++) {
            var m = a.charCodeAt(g);
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023),
            e[f++] = m >> 18 | 240,
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224,
            e[f++] = m >> 6 & 63 | 128),
            e[f++] = m & 63 | 128)
        }
        a = b;
        for (f = 0; f < e.length; f++) a += e[f],
        a = RL(a, $b);
        a = RL(a, Zb);
        a ^= b1 || 0;
        0 > a && (a = (a & 2147483647) + 2147483648);
        a %= 1E6;
        return a.toString() + jd + (a ^ b)
    };
    function RL(a, b) {
        var t = "a";
        var Yb = "+";
        for (var c = 0; c < b.length - 2; c += 3) {
            var d = b.charAt(c + 2),
            d = d >= t ? d.charCodeAt(0) - 87 : Number(d),
            d = b.charAt(c + 1) == Yb ? a >>> d: a << d;
            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d
        }
        return a
    }
    """)

    def getTk(self, text):
        """获取tk值"""
        return self.ctx.call("TL", text)


# 获取要翻译的文字
key = input("请输入你的文字>>")
print('输入你文字类型>>')
print("\t0:日语\n\t1:法语\n\t2:韩语\n\t3:英语\n\t4:中文")
j = int(input(">>"))
languages = ['ja', 'fr', 'ug', 'en', 'zh-CN']
print("请输入你想翻译成的语言>>")
print("\t0:日语\n\t1:法语\n\t2:韩语\n\t3:英语\n\t4:中文")
i = langugage_choose = int(input('>>'))

# 获取Py4Js实例
py = Py4Js()
# print(py.getTk(key))  # 打印tk值
# 对中文进行处理
data = urllib.parse.urlencode({"q": key})
# 请求的URL
url = "https://translate.google.cn/translate_a/single?client=webapp&sl=" + languages[j] + "&tl=" + languages[
    i] + "&hl=zh-CN" \
         "&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ssel=6&tsel=3&kc=1&tk=" + py.getTk(
    key) + "&" + data
# print(url)  # 打印URL
# 请求头
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
}

# 获取request对象
req = urllib.request.Request(url, headers=header)
# 响应的数据是通过Ajax返回的JSON格式数据，注意编码问题
resp = urllib.request.urlopen(req).read().decode("utf-8")
# 打印
# print(resp)
eng = re.findall(r'\[\[\["(.*?)"', resp)[0]
end1 = re.findall(r'\[\["(.*?)"', resp)
print('翻译结果:', eng, '\n其他结果:', end1[0])
for item in end1:
    print(item)
print("翻译结束，谢谢使用！")
