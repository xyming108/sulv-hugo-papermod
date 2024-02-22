
# From https://github.com/MHG-LAB/RSSBOX/

import queue
import sys
import threading
import requests
from bs4 import BeautifulSoup
import time
import re
import os
import yaml
import random

    
def load_config(path):
  f = open(path, 'r', encoding='utf-8')
  ystr = f.read()
  ymllist = yaml.load(ystr, Loader=yaml.FullLoader)
  return ymllist

if os.path.exists('config.api.yml'):
  c=load_config('config.api.yml')
  CORS_API = c['CORS_API']
  RSSHUB_API = c['RSSHUB_API']
else:
  CORS_API = sys.argv[1]
  RSSHUB_API = sys.argv[2]

# 反反爬虫
def getRandUa():
  first_num = random.randint(55, 62)
  third_num = random.randint(0, 3200)
  fourth_num = random.randint(0, 140)
  os_type = [
      '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)', '(X11; Linux x86_64)',
      '(Macintosh; Intel Mac OS X 10_12_6)'
  ]
  chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)

  ua = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
                  '(KHTML, like Gecko)', chrome_version, 'Safari/537.36']
                )
  return ua

proxies = {
    'https': 'https://127.0.0.1:7890',
    'http': 'http://127.0.0.1:7890'
}

def get_data_result(link,rand_ua=False):
  # print('正在获取数据...')
  # print('链接：', link)
  result = ''
  if rand_ua:
    ua = getRandUa()
  else:
    ua = 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
  header = {
    'User-Agent': ua,
    "Connection": "close",
    }
  try:
    requests.adapters.DEFAULT_RETRIES = 55
    s = requests.session()
    s.keep_alive = False # 关闭多余连接
    # r = s.get(link, headers=header, timeout=120,verify=True,proxies=proxies)
    r = s.get(link, headers=header, timeout=120,verify=True)
    s.close()
    r.encoding = 'utf-8'
    result = r.text.encode("utf-8", 'ignore').decode('utf-8', 'ignore')
    print(f"{str(r)}::{link}")
    if str(r) != '<Response [200]>':
      result = ''
  except Exception as e:
    error_line = e.__traceback__.tb_lineno
    error_info = '第{error_line}行发生error为: {e}'.format(error_line=error_line, e=str(e))
    print(error_info)
    result = ''
  return result

def get_data(link):
  result = get_data_result(link,False)
  if result == '':
    result = get_data_result(link,True)
  return result

def dfs_route(route_config, path):
    for key, value in route_config.items():
        if isinstance(value, dict):
            dfs_route(value, path + [key])
        else:
            dir = "/" + "/".join(path + [key])
            try:
              os.makedirs('content/posts/read' + dir + '/')
            except Exception as e:
                print('已存在目录', 'content/posts/read' + dir + '/')
            it = {'path': value, 'cat': path + [key], 'tag': path + [key], 'dir': dir}
            print(it)
            data.append(it)


md_temple = '''---
title: {title}
categories: {cat}
keywords: {tag}
date: {date}
lastmod: {date}
author: [{tag}]
tags: {tag}
draft: false 
comments: true
reward: true 
mermaid: true 
showToc: true 
TocOpen: true 
hidemeta: false 
disableShare: true 
showbreadcrumbs: true 
cover:
    image: {img}
    alt: "{title}"
    relative: false
---

<div>
{text}
</div>

<div>
版权声明：
本文为 {tag} 原创文章，本站仅在原基础上进行总结，受 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) 版权协议保护。未经授权，禁止转载。
如需转载，请务必注明原文出处链接和本声明，且不得用于商业用途。
感谢您的尊重与支持，您的理解和配合对原创作者至关重要。请尊重知识产权，共同维护良好的网络环境。
<!-- tag_link -->
</div>

'''

# 获取最长的text
def get_long_text(list_text):
  max_len = 0
  max_text = ''
  for text in list_text:
    if text in [None,'', ' ', '\n', '\r\n', '\r', '\t']:
      text = ""
    if len(text) > max_len:
      max_len = len(text)
      max_text = text
  return max_text

def get_post(res,item):
  cat = item['cat']
  tag = item['tag']
  dir = item['dir']
  soup = BeautifulSoup(res, "lxml-xml")
  for i in soup.find_all(['item','entry'])[0:15]:
    title = ''
    text = ''
    pubdate = ''
    img = ''
    link = ''
    # description
    description=""
    encoded=""
    content=""
    summary=""
    
    for child in i.children:
      childName = child.name
      if str(type(childName)) == "<class 'str'>":
        childName = str.lower(childName)
      if (childName == 'title'):
        title = child.string or str(time.time()) 
      
      if (childName == 'description'):
        description= child.string
      if (childName == 'encoded'):
        encoded = child.string
      if (childName == 'content'):
        content = child.string
      if (childName == 'summary'):
        summary = child.string

      if (childName == 'link'):
        if "href" in child.attrs:
          link = child["href"]
        else:
          link = child.string

      if pubdate == '' and (childName == 'published'):
        pubdate = child.string
      if pubdate == '' and (childName == 'lastbuilddate'):
        pubdate = child.string
      if pubdate == '' and (childName == 'pubdate'):
        pubdate = child.string
      if pubdate == '' and (childName == 'updated'):
        pubdate = child.string

    if (pubdate == ''):
      pubdate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    text = get_long_text([description,encoded,content,summary])
    if text not in ["",None]:
      soup_item = BeautifulSoup(text, 'html.parser')
      if soup_item.find('img'):
        if 'data-lazy-src' in soup_item.find('img').attrs:
          img = soup_item.find('img')['data-lazy-src'].strip()
        else:
          img = soup_item.find('img')['src'].strip()
    text = TEXT的特殊处理(text)
    try:
      filename = re.sub(r'[:/\\?\*“”\'"<>\.|\[\]]', '_', title)
    except:
      filename = str(time.time())
    #title = re.sub(r'[\'"]', '_', title)
    filename = filename.replace('\n', '').replace('#', '').replace('.','')
    
    print(link)
    if link:
      from urllib.parse import urlparse
      url = urlparse(link)
      loc = url.scheme+"://"+url.netloc
      # 反防盗链 cors
      text = text.replace('src="https://','src="'+CORS_API+'/?r='+loc+'&url=https://')
      text = text.replace('src="http://','src="'+CORS_API+'/?r='+loc+'&url=http://')
      text = text.replace('="/','="'+CORS_API+'/?r='+loc+'&url='+loc+'/')
      text = text.replace('="../','="'+CORS_API+'/?r='+loc+'&url='+loc+'/../')
      if img:
        print(img)
        img = img.replace('https://',CORS_API+'/?r='+loc+'&url=https://')
        img = img.replace('http://',CORS_API+'/?r='+loc+'&url=http://')
        img = re.compile(r'^\/').sub(CORS_API+'/?r='+loc+'&url='+loc+'/', img, 1)
        img = img.replace('../',CORS_API+'/?r='+loc+'&url='+loc+'/../',1)
    elif img:
      img = img.replace('http://',CORS_API+'/?url=http://')
    if not img:
      img = "https://www.g0f.cn/img/banner.jpg"

    
    md_content = md_temple
    try:
      with open('content/posts/read' + dir + '/' + filename + '.md',
        mode='w',
        encoding='utf-8') as f:
        if "'" in title:
          title = '"' + title + '"'
        else:
          title = "'" + title + "'"
        md_content = md_content.format(title=title, cat=cat, tag=tag, date=pubdate, text=text, img=img)
        md_content = md_content.replace('{', '&#123;')
        md_content = md_content.replace('}', '&#125;')
        # print(link)
        md_content = md_content.replace('<!-- tag_link -->', '{% link '+str(link)+' '+str(title)+' %}')
        print('---------------------------')
        print('发布时间：', pubdate)
        print('标题：', title)
        print('描述：', '已获取内容'+text[0:20])
        print('图片：', img)
        print('---------------------------')
        f.write(md_content)
        f.close()
    except Exception as e:
      error_line = e.__traceback__.tb_lineno
      error_info = '第{error_line}行发生error为: {e}'.format(error_line=error_line, e=str(e))
      print(error_info)




# 解析线程类
class Parse(threading.Thread):
  def __init__(self, number, data_list, req_thread):
    super(Parse, self).__init__()
    self.number = number
    self.data_list = data_list
    self.req_thread = req_thread
    self.is_parse = True  # 判断是否从数据队列里提取数据

  def run(self):
    print('启动%d号解析线程' % self.number)
    while True:
      # 如何判断解析线程的结束条件
      for t in self.req_thread:
        if t.is_alive():
          break
      else:
        if self.data_list.qsize() == 0:
          self.is_parse = False

      if self.is_parse:  # 解析
        try:
          data = self.data_list.get(timeout=3)
        except Exception as e:
          data = None
        if data is not None:
          self.parse(data)
      else:
        break
    print('退出%d号解析线程' % self.number)

  # 页面解析函数
  def parse(self, data):
    get_post(data[0], data[1]) # [response,item]


# 采集线程类
class Crawl(threading.Thread):
  def __init__(self, number, req_list, data_list):
    super(Crawl, self).__init__()
    self.number = number
    self.req_list = req_list
    self.data_list = data_list

  def run(self):
    print('启动采集线程%d号' % self.number)
    while self.req_list.qsize() > 0:
      item = self.req_list.get()
      print('%d号线程采集：%s' % (self.number, item['path']))
      requests_url =  item['path']
      if requests_url.startswith('/'):
        requests_url = RSSHUB_API + requests_url + "?time=%s" % int(time.time()) + "&rand=%s" % str(random.randint(0,10000))
        print("====== "+RSSHUB_API+" ========> " + requests_url + " ======")
      else:
        print("====== " + requests_url + " ======")
      response = get_data(requests_url)
      if response.strip() == "" and item['path'].startswith('/'):
        requests_url = "https://rsshub.app" + item['path'] + "?time=%s" % int(time.time()) + "&rand=%s" % str(random.randint(0,10000))
        print("====== https://rsshub.app ========> " + requests_url + " ======")
        response = get_data(requests_url)
      # time.sleep(random.randint(1, 3))
      self.data_list.put([response,item])  # 向数据队列里追加


def 解析文章():
  concurrent = 10
  conparse = 10

  # 生成请求队列
  req_list = queue.Queue()
  # 生成数据队列
  data_list = queue.Queue()

  # 填充请求数据
  for item in data:
    req_list.put(item)

  # 生成N个采集线程
  req_thread = []
  for i in range(concurrent):
    t = Crawl(i + 1, req_list, data_list)  # 创造线程
    t.start()
    req_thread.append(t)

  # 生成N个解析线程
  parse_thread = []
  for i in range(conparse):
    t = Parse(i + 1, data_list, req_thread)  # 创造解析线程
    t.start()
    parse_thread.append(t)

  for t in req_thread:
    t.join()
  for t in parse_thread:
    t.join()

def TEXT的特殊处理(text):
  soup = BeautifulSoup(text, 'html.parser')
  # 反图片懒加载
  for img in soup.find_all('img'):
    if "srcset" in img.attrs:
      img["data-src"] = "data:image/gif;base64,R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="
      img.attrs.pop('srcset')
      img.wrap(soup.new_tag('img'))
  text = str(soup)
  return text



route_config = load_config('config.route.yml')
path=[]
data=[]

print("--------- 解析路由配置文件 begin ---------")
dfs_route(route_config, path)
print("--------- 解析路由配置文件 end ---------")
print("--------- 解析文章 begin ---------")
解析文章()
print("--------- 解析文章 end ---------")
