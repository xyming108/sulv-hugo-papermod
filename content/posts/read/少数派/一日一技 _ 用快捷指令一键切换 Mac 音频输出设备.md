---
title: '一日一技 | 用快捷指令一键切换 Mac 音频输出设备'
categories: ['少数派']
date: Wed, 21 Feb 2024 07:00:26 GMT
lastmod: Wed, 21 Feb 2024 07:00:26 GMT
author: ["g0f"]
tags:
- read
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
    image: "/hugo-logo-wide.svg"
    alt: 果粉圈
    relative: false
---

<div>

<div> 快捷指令, 音频设备, 切换, Mac, SwitchAudioSource
<br/><br/>总结:
本文介绍了如何在Mac上使用快捷指令和SwitchAudioSource工具来实现一键切换音频输出设备。作者首先解释了在Mac上的环境设置和SwitchAudioSource工具的安装方法，并提供了相应的代码示例。然后，作者详细讲解了如何使用快捷指令创建一个能够切换音频输出设备的自定义脚本，包括设备列表的修改和添加键盘快捷键。最后，作者鼓励读者在评论区提出问题并分享了自己的制作心得。整篇文章清晰地介绍了操作步骤，适合Mac用户进行参考和实践。 <div>
<p>大家好，我是 NowScott。</p><h2>原因</h2><p>之前在使用 Windows 电脑时，由于经常需要把声音输出在音箱和耳机之间频繁切换，就找到了一个软件来实现一键切换（鼠标侧键映射到快捷键上）音频输出设备，但是换到 Mac 上暂时没发现一个好用的实现这个功能的软件，应该有吧，实际上是我没太仔细找，想着用快捷指令也能很好地实现，就自己写了一个快捷指令来实现这个功能。</p><h2>原理部分</h2><p>SwitchAudioSource 是一个在 macOS 系统上运行的命令行工具，用于管理系统的音频输入和输出设备。通过这个工具，用户可以在不打开系统偏好设置的情况下，快速而方便地切换音频设备，这也是本文主要使用的工具。</p><p>Mac 上的快捷指令可以用来调用 shell 脚本，同时支持快捷键对于指令的调用，因此我只需要把音频切换的代码放在快捷指令的 shell 脚本中，就可以实现使用快捷键来切换音频。</p><h2>代码部分</h2><p>代码部分如下，相信学过一些编程的人就可以轻松看懂，如果有什么问题可以评论区指出，大家共同进步！</p><pre class="language-shell"><code>#!/bin/bash

# 设置环境变量
export PATH=/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/opt/homebrew/Cellar/switchaudio-osx/1.2.2:$PATH

# 获取全部音频设备的列表
available_devices=$(SwitchAudioSource -a -t output)

# 定义音频设备列表
devices=("AirPods Max" "Mac mini扬声器")

# 获取当前音频设备
current_device=$(SwitchAudioSource -c)

# 查找当前设备在列表中的索引
current_index=-1
for i in "$&#123;!devices[@]&#125;"; do
    if [ "$&#123;devices[i]&#125;" == "$current_device" ]; then
        current_index=$i
        break
    fi
done

# 切换到下一个设备
next_index=$(( (current_index + 1) % $&#123;#devices[@]&#125; ))
next_device="$&#123;devices[next_index]&#125;"

# 循环直到找到一个可用的设备
while true; do
    # 检查下一个设备是否在可用设备列表中
    if echo "$available_devices" | grep -q "$next_device"; then
        # 检查是否已经循环到了当前设备
        if [ "$next_device" != "$current_device" ]; then
            # 切换设备
            SwitchAudioSource -s "$next_device" &gt;/dev/null
            echo "已切换设备到 $next_device"
            break
        else
            echo "切换失败，暂无其他可用设备"
            break
        fi
    fi
    
    # 尝试下一个设备
    next_index=$(( (next_index + 1) % $&#123;#devices[@]&#125; ))
    next_device="$&#123;devices[next_index]&#125;"
done</code></pre><p>其中 <code>devices=("AirPods Max" "Mac mini扬声器")</code> 要将括号中的内容换成你的音频设备，可以在终端中输入如下代码来获取</p><pre class="language-shell"><code>SwitchAudioSource -a -t output</code></pre><p>当然在此之前要确保你已经安装了 SwitchAudioSource。</p><p>要安装 SwitchAudioSource，您可以使用 Homebrew 工具来进行安装。</p><p>首先，确保您已经安装了 Homebrew。如果您还没有安装 Homebrew，可以在终端中输入以下命令进行安装：</p><pre class="language-shell"><code>/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" </code></pre><p>安装完成后，可以使用以下命令来安装 SwitchAudioSource：</p><pre class="language-bash"><code> brew install switchaudio-osx</code></pre><h2>使用</h2><p>下面是我分享的快捷指令 iCloud 链接，你可以点击链接获取捷径或者跟着我用以下几个步骤来创建一个自己的切换音频的快捷指令</p><p>🔗 链接：<a href="https://www.icloud.com/shortcuts/2d1a8f9c4b054775906e6374436156cd">https://www.icloud.com/shortcuts/2d1a8f9c4b054775906e6374436156cd</a></p><p>⚠️ 注意：使用链接添加是不会自动添加快捷键的，同时还需要修改自己的音频设备名称到代码中。</p><h2>创建步骤</h2><p>1. 点击 + 创建新的快捷指令：</p><figure class="image ss-img-wrapper"><img src="https://cdn.sspai.com/2024/02/19/13217c8a06a0d0ee0a4b3b6eb31d9ff6.png?imageView2/2/w/1120/q/90/interlace/1/ignore-error/1"/></figure><p>2. 搜索shell，将运行shell脚本拖进来，接着修改一下快捷指令的名称：</p><figure class="image ss-img-wrapper"><img src="https://cdn.sspai.com/2024/02/19/fdaee40f3fd648b98e081b39474713e2.png?imageView2/2/w/1120/q/90/interlace/1/ignore-error/1"/></figure><p>3. 复制前文代码到其中，并将下面的 shell 改为 bash：</p><figure class="image ss-img-wrapper"><img src="https://cdn.sspai.com/2024/02/19/756a3d657a05ad37ff19ce79608a199d.png?imageView2/2/w/1120/q/90/interlace/1/ignore-error/1"/></figure><p>4. 修改设备列表为你的音频输出设备：</p><figure class="image ss-img-wrapper"><img src="https://cdn.sspai.com/2024/02/19/12fd309ac90edb59744ea46a58b9e321.png?imageView2/2/w/1120/q/90/interlace/1/ignore-error/1"/></figure><p>5. 接下来添加键盘快捷键，我这里设置的是 Fn + control + F10：</p><figure class="image ss-img-wrapper"><img src="https://cdn.sspai.com/2024/02/19/2961ca61dfcfeb8e0868c522d128fc50.png?imageView2/2/w/1120/q/90/interlace/1/ignore-error/1"/></figure><p>6. 如果你需要切换后通知一下，那么可以在后面添加一个通知或者提醒（管理员身份运行并不重要，我只是顺手点上了）：</p><figure class="image ss-img-wrapper"><img src="https://cdn.sspai.com/2024/02/19/b125f6c0cb1e631db3d1fd7ce3fc102f.png?imageView2/2/w/1120/q/90/interlace/1/ignore-error/1"/></figure><p>这样就实现了这个快捷指令的制作，如果有需要可以把鼠标侧键绑定为刚才设置的快捷键，就能实现一键切换音频输出了。</p><h2 style="margin-left: 0px;">结尾</h2><p style="margin-left: 0px;">如果你通过我的文章有多学到一点知识，那我的目的就达成了。</p><p style="margin-left: 0px;">如果发现本文有什么错误可以在评论区发出来，我会虚心接受并及时改正。</p><p style="margin-left: 0px;">&gt; 关注 <a href="https://sspai.com/s/J71e">少数派公众号</a>，解锁全新阅读体验 📰</p><p style="margin-left: 0px;">&gt; 实用、好用的 <a href="https://sspai.com/mall">正版软件</a>，少数派为你呈现 🚀</p>
</div></div>
</div>

<div>
[原文](https://sspai.com/post/86520)
</div>

