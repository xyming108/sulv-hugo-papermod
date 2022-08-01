Language：English | [中文](https://github.com/xyming108/sulv-hugo-papermod)

## 1. Git clone pull code

① Use `git clone` to pull the code to the desktop. At this time, the sulv Hugo papermod directory will be generated on the desktop

② Enter the sulv Hugo papermod directory and enter `git submodule update --init` to pull the submodule under themes / Hugo papermod / and put the official theme inside

## 2. Startup interface

③ Return the directory to sulv Hugo papermod, enter `hugo server -d` in the terminal, and enter: localhost:1313 in the browser to see the ready-made blog template.

## 3. Modify information

There are many personal information in the template that need to be configured by yourself. Please be patient to modify it. You can refer to the blogger's website building tutorial:[ https://www.sulvblog.cn/posts/blog/ ]( https://www.sulvblog.cn/posts/blog/ )

## 4. Hugo blog exchange group

🎉🎉 787018782 🎉🎉

## 5. How to use shortcodes

`bilibili: {{< bilibili BV1Fh411e7ZH(填 bvid) >}}`

`youtube: {{< youtube w7Ft2ymGmfc >}}`

`ppt: {{< ppt src="网址" >}}`

`douban: {{< douban src="网址" >}}`

```
# Links in SRC must not be added with https:// or http://, and you can choose not to add WWW; If desc is written, the value of desc will be displayed in the browser
link: {{< link src="www.sulvblog.cn" desc="https://www.sulvblog.cn" >}}
```

```
gallery:

{{< gallery >}}
{{< figure src="https://www.sulvblog.cn/posts/read/structural_thinking/0.png" >}}
{{< figure src="https://www.sulvblog.cn/posts/read/structural_thinking/0.png" >}}
{{< /gallery >}}
```

## 5. Possible problems


1. Some users will deploy to GitHub and may encounter cross system problems, such as the prompt `lf will be replaced by CRLF in *******`, and then enter the command: `git config core.autocrlf false`, which solves the problem of automatic conversion of line breaks。