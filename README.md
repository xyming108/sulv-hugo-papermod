## 1. git clone 拉取代码

用`git clone`的方式拉取代码至桌面，进入到sulv-hugo-papermod目录，在该目录打开终端，输入`hugo server -D`，在浏览器输入：localhost:1313即可看到现成的博客模板

## 2. themes代码和官方保持一致

定位到themes/PaperMod/下，打开终端，输入`git pull`，从PaperMod的官方主题中拉取最新代码，PaperMod主题官方地址：[https://github.com/adityatelange/hugo-PaperMod](https://github.com/adityatelange/hugo-PaperMod)

## 3. 修改信息

模板内部有许多个人信息需要自己配置，请耐心修改完，可以参考博主的建站教程：[https://www.sulvblog.cn/posts/blog/](https://www.sulvblog.cn/posts/blog/)

## 4. shortcodes使用方法

`bilibili: {{< bilibili BV1Fh411e7ZH(填 bvid) >}}`

`youtube: {{< youtube w7Ft2ymGmfc >}}`

`ppt: {{< ppt src="网址" >}}`

`douban: {{< douban src="网址" >}}`

```
gallery:

{{< gallery >}}
{{< figure src="https://www.sulvblog.cn/posts/read/structural_thinking/0.png" >}}
{{< figure src="https://www.sulvblog.cn/posts/read/structural_thinking/0.png" >}}
{{< /gallery >}}
```

