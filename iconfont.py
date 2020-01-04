# -*- coding:utf-8 -*-

import os
import re
import json
from requests import get
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM


def download(cid, num):
    res = get(f'https://www.iconfont.cn/api/collection/detail.json?id={cid}').text
    data = json.loads(res)

    if data.get('code', 0) != 200:
        exit(0)

    cwd = os.getcwd()

    lis = data['data']['icons']
    name = data['data']['collection']['name']

    if not os.path.exists(os.path.join(cwd, name)):
        os.makedirs(os.path.join(cwd, name))
    for v in lis:
        cname = v['name']
        svg_path = os.path.join(cwd, name, cname + '.svg')
        png_path = os.path.join(cwd, name, cname + '.png')
        width, height = v['width'], v['height']
        svg_data = v['show_svg']
        style = re.findall(r'(style=".*?")', svg_data)[0]
        svg_data = svg_data.replace(style, f'height="{num}" width="{width / height * num}"')
        with open(svg_path, 'wb+') as svg_file:
            svg_file.write(svg_data.encode('utf8'))
        drawing = svg2rlg(svg_path)
        renderPM.drawToFile(drawing, png_path, fmt='png')
    return name


if __name__ == '__main__':
    num = input('请输入需要设置矢量图的高度(默认200)：')
    try:
        num = int(num)
    except:
        print('输入错误，选择默认参数200')
        num = 200
    while True:
        res = input('请输入需要提取矢量图的网址：')
        fi = re.findall(r'^https?://www\.iconfont\.cn/collections/detail\?.*cid=(\d+)', res)
        if len(fi) <= 0:
            print('您输入的网址不正确')
            continue
        name = download(fi[0], num)
        print(f'下载({name})完成')
