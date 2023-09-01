---
title: "Redis scan命令学习"
date: 2022-11-30T15:55:23+08:00
lastmod: 2022-11-30T15:55:23+08:00
author: ["Sulv"]
keywords: 
- Redis
categories: 
- Redis
tags: 
- Redis
- tech
description: "scan命令详解"
weight:
slug: ""
draft: false # 是否为草稿
comments: true
reward: true # 打赏
mermaid: false # 是否开启mermaid
showToc: true # 显示目录
TocOpen: true # 自动展开目录
hidemeta: false # 是否隐藏文章的元信息，如发布日期、作者等
disableShare: true # 底部不显示分享栏
showbreadcrumbs: true # 顶部显示路径
cover:
    image: "" # 图片路径：posts/tech/123/123.png
    caption: "" # 图片底部描述
    alt: ""
    relative: false
---



## 1. 介绍

`scan`命令的作用和`keys *`的作用类似，主要用于查找redis中的键，但是在正式的生产环境中一般不会直接使用`keys *`这个命令，因为他会返回所有的键，如果键的数量很多会导致查询时间很长，进而导致服务器阻塞，所以需要scan来进行更细致的查找

`scan`总共有这几种命令：`scan`、`sscan`、`hscan`、`zscan`，分别用于迭代数据库中的：数据库中所有键、集合键、哈希键、有序集合键，命令具体结构如下：

```bash
scan cursor [MATCH pattern] [COUNT count] [TYPE type]
sscan key cursor [MATCH pattern] [COUNT count]
hscan key cursor [MATCH pattern] [COUNT count]
zscan key cursor [MATCH pattern] [COUNT count]
```

## 2. scan

`scan cursor [MATCH pattern] [COUNT count] [TYPE type]`，cursor表示游标，指查询开始的位置，count默认为10，查询完后会返回下一个开始的游标，当返回0的时候表示所有键查询完了

```bash
127.0.0.1:6379[2]> scan 0
1) "3"
2)  1) "mystring"
    2) "myzadd"
    3) "myhset"
    4) "mylist"
    5) "myset2"
    6) "myset1"
    7) "mystring1"
    8) "mystring3"
    9) "mystring4"
   10) "myset"
127.0.0.1:6379[2]> scan 3
1) "0"
2) 1) "myzadd1"
   2) "mystring2"
   3) "mylist2"
   4) "myhset1"
   5) "mylist1"
```

MATCH可以采用模糊匹配找出自己想要查找的键，这里的逻辑是先查出20个，再匹配，而不是先匹配再查询，这里加上count 20是因为默认查出的10个数中可能不能包含所有的相关项，所以把范围扩大到查20个，我这里测试的键总共有15个

```bash
127.0.0.1:6379[2]> scan 0 match mylist* count 20
1) "0"
2) 1) "mylist"
   2) "mylist2"
   3) "mylist1"
```

TYPE可以根据具体的结构类型来匹配该类型的键

```bash
127.0.0.1:6379[2]> scan 0 count 20 type list
1) "0"
2) 1) "mylist"
   2) "mylist2"
   3) "mylist1"
```

## 3. sscan

`sscan key cursor [MATCH pattern] [COUNT count]`，sscan的第一个参数总是集合类型的key

```bash
127.0.0.1:6379[2]> sadd myset1 a b c d
(integer) 4
127.0.0.1:6379[2]> smembers myset1
1) "d"
2) "a"
3) "c"
4) "b"
127.0.0.1:6379[2]> sscan myset1 0
1) "0"
2) 1) "d"
   2) "c"
   3) "b"
   4) "a"
127.0.0.1:6379[2]> sscan myset1 0 match a
1) "0"
2) 1) "a"
```

## 4. hscan

`hscan key cursor [MATCH pattern] [COUNT count]`，sscan的第一个参数总是哈希类型的key

```bash
127.0.0.1:6379[2]> hset myhset1 kk1 vv1 kk2 vv2 kk3 vv3
(integer) 3
127.0.0.1:6379[2]> hgetall myhset1
1) "kk1"
2) "vv1"
3) "kk2"
4) "vv2"
5) "kk3"
6) "vv3"
127.0.0.1:6379[2]> hscan myhset1 0
1) "0"
2) 1) "kk1"
   2) "vv1"
   3) "kk2"
   4) "vv2"
   5) "kk3"
   6) "vv3"
```

## 5. zscan

`zscan key cursor [MATCH pattern] [COUNT count]`，sscan的第一个参数总是有序集合类型的key

```bash
127.0.0.1:6379[2]> zadd myzadd1 1 zz1 2 zz2 3 zz3
(integer) 3
127.0.0.1:6379[2]> zrange myzadd1 0 -1 withscores
1) "zz1"
2) "1"
3) "zz2"
4) "2"
5) "zz3"
6) "3"
127.0.0.1:6379[2]> zscan myzadd1 0
1) "0"
2) 1) "zz1"
   2) "1"
   3) "zz2"
   4) "2"
   5) "zz3"
   6) "3"
```
