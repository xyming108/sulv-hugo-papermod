---
title: '随时收听、更省流量，用 HLS 搭建私有音乐电台'
categories: ['少数派']
date: Thu, 22 Feb 2024 07:00:00 GMT
lastmod: Thu, 22 Feb 2024 07:00:00 GMT
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

<div> 流媒体协议, HLS, FFmpeg, Windows Media Player, 应用流媏服务
总结：<br/><br/>本文介绍了使用HLS流媒体协议和FFmpeg工具在Windows系统上制作音乐串流服务的过程。通过在Windows Media Player上创建播放列表，使用PowerShell脚本和FFmpeg工具制作HLS流媒体文件，再通过HTTP服务器提供播放服务。最后，作者还介绍了如何将不同来源的HLS串流整合到一个电台服务中。整个方案实现了自由播放音乐的目的，同时尽可能降低了性能需求，可以在低功耗平台上运行。文章内容详实，操作步骤清晰，为有相似需求的读者提供了很好的参考价值。 <div>
<p>在各种云音乐大行其道、本地音乐日渐消亡的今天，用户似乎不再像以前一样，可以完整地拥有曲目的播放权，以至于有时你似乎只能接受各种云音乐的安排，这既有当下现实盈利模式的无奈也有大众版权意识的提高，但对于那一部分想拥有自由播放权的人来说，以自己的方式播放音乐始终是一个绕不开的课题，虽然自由的成本它总是高昂。</p><p>总的来看，它最好能支持以下这些特性：</p><ul><li>不需要第三方客户端 / 插件，即可对流媒体进行解码、播放</li><li>节约流量：只加载当前需要的部分，而不是把所有内容都预加载到本地</li><li>能与本地 PC 音乐播放器的播放列表进行同步，这样我只需要维护一份歌曲列表</li></ul><p>经过一番搜索和查找，我决定试一试由 Apple 在 2009 年提出的 HLS 流媒体协议，这和我在用的 iPhone 和 iPad 设备应该会比较配。</p><h2>HLS</h2><p>全称 HTTP Live Streaming，是众多流媒体传输协议中的一种，基本原理是通过播放列表 + 媒体片段的模式对流媒体进行切分，通过 HTTP 协议由客户端一点点地下载，可实现流媒体的点播和直播。</p><p>以一段 60s 的短视频为例，如果我们以 HLS 的形式发布它，可以把这段 60s 的视频切分为 6 个 10 秒的无间隔小片段 .ts，这 6 个片段信息会被记录在媒体列表 .m3u8 文件中，终端通过 URL 先读取播放列表 .m3u8，按播放列表的顺序预加载这些片段 .ts 并播放，给用户的感觉就像是一段连续而完整的视频，但实际上这是由 6 个片段按顺序组合而成的流媒体。</p><p>利用 HLS 协议的分片特性，可以做到仅加载一部分片段而非整个媒体文件的效果，节省流量和带宽消耗，另因该协议最早由 Apple 发起推动，在 Apple 一众设备上均有系统级的原生支持，不需要额外安装第三方插件/App 即可解码播放，完美解决了我的前两个需求。</p><p>至于第三个需求，情况则要复杂一些：我主力使用 Windows 系统，自带 Windows Media Player 播放器「简称 WMP」，Apple 官方提供的 HLS 流媒体制作工具只适用于自家 macOS 系统，要准备 HLS 流媒体需要使用第三方工具来完成，比如大名鼎鼎的 FFmpeg，它支持输出 HLS 标准的流媒体格式，但喂给它的原始媒体需要用户自己准备，好在 FFmpeg 还支持通过简单列表的方式，可以将多个音乐文件合并为一个，即可以用脚本把 WMP 播放列表转换为 FFmpeg 支持的格式，FFmpeg 将整个播放列表涉及的曲目合并为一个媒体文件，再启动负责 HLS 串流的 FFmpeg 进程循环读取这一个文件即可。</p><p>让我们来大致梳理一下整个流程：</p><ul><li>wpl 播放列表 -&gt; PowerShell 脚本 -&gt;  给 FFmpeg 的列表 -&gt; FFmpeg 打包 -&gt;  音乐合集</li><li>音乐合集 -&gt; FFmpeg 串流 -&gt; HLS 流媒体 -&gt; HTTP 服务器</li><li>HTTP 服务器 -&gt; 终端播放</li></ul><h2>准备</h2><p>Windows Media Player 播放列表 .wpl</p><pre class="language-shell"><code>&lt;?wpl version="1.0"?&gt;
&lt;smil&gt;
    &lt;head&gt;
        &lt;meta name="Generator" content="Microsoft Windows Media Player -- 12.0.17763.1821"/&gt;
        &lt;meta name="ItemCount" content="0"/&gt;
        &lt;meta name="IsFavorite"/&gt;
        &lt;meta name="ContentPartnerListID"/&gt;
        &lt;meta name="ContentPartnerNameType"/&gt;
        &lt;meta name="ContentPartnerName"/&gt;
        &lt;meta name="Subtitle"/&gt;
        &lt;author/&gt;
        &lt;title&gt;sax&lt;/title&gt;
    &lt;/head&gt;
    &lt;body&gt;
        &lt;seq&gt;
            &lt;media src="..\Sax\Sentimental.mp3" tid="&#123;2145ECDB...&#125;"/&gt;
            &lt;media src="..\Sax\Silhouette.mp3" tid="&#123;5FE8D8A1...&#125;"/&gt;
            &lt;media src="..\Sax\Songbird.mp3" tid="&#123;EEA17777...&#125;"/&gt;
            &lt;media src="..\Sax\Spring Breeze.mp3" tid="&#123;708DFC49...&#125;"/&gt;
            &lt;media src="..\Sax\The Look Of Love.mp3" tid="&#123;C49AB7BB...&#125;"/&gt;
            &lt;media src="..\Sax\The Moment.mp3" tid="&#123;917AF6EB...&#125;"/&gt;
......</code></pre><p>FFmpeg 打包列表 .txt</p><pre class="language-null"><code>file 'D:\music\Sax\Sentimental.mp3'
file 'D:\music\Sax\Silhouette.mp3'
file 'D:\music\Sax\Songbird.mp3'</code></pre><p>如果 wpl 播放列表有更新，根据前述流程，直接调用脚本读取并重新制作一个最新的媒体文件</p><ul><li>FFmpeg Essential <a href="https://www.gyan.dev/ffmpeg/builds" target="_blank">下载地址</a></li><li>dos2unix <a href="https://dos2unix.sourceforge.io/" target="_blank">下载地址</a></li></ul><pre class="language-shell"><code># PowerShell

$music_folder = 'D:\music'
$source_list  = 'D:\music\playlists\sax.wpl'
$playlist_for_ffmpeg = 'D:\music\playlists\plfff\sax.txt'
$music_hls = 'D:\music\hls\sax_bundle.mp3'

# Playlist Transform
[xml]$wpl = Get-Content -Encoding utf8 $source_list
$wpl.smil.body.seq.media | ForEach-Object &#123;$src = $_.src -replace"\.\.","file '$music_folder"
    $pl = $src -replace "mp3", "mp3'"
    $pl | Out-File -Append $playlist_for_ffmpeg
&#125;
# Powershell Version &lt; 7.2
.\dos2unix.exe $playlist_for_ffmpeg $playlist_for_ffmpeg
# Combine
.\ffmpeg.exe -f concat -safe 0 -i $playlist_for_ffmpeg -c copy $music_hls</code></pre><h3>注意</h3><ul><li>如果你的音频文件不是 MP3 格式，而是其它什么格式，需要修改一下上面这个脚本</li><li>因为 Powershell 5.1 版本的问题，我无法直接在 <code>Out-File</code> 输出时直接把文本转为 FFmpeg 需要的 UTF8NoBom 字符编码，转由 dos2unix.exe 代劳。自 Powershell 7.2 版本后已解决此问题，通过 Encoding 参数</li></ul><pre class="language-shell"><code>...
    $pl = $src -replace "mp3", "mp3'"
    $playlist | Out-File -Encoding utf8NoBOM -Append $playlist_for_ffmpeg
&#125;
.\ffmpeg.exe -f concat -safe 0 -i $playlist_for_ffmpeg -c copy $music_hls</code></pre><h2>串流</h2><pre class="language-shell"><code># CMD

set music_hls=D:\music\hls\sax_bundle.mp3
set www_hls=E:\hls\sax.m3u8
ffmpeg -stream_loop -1 -re -i %music_hls% -codec copy -hls_time 10 -hls_list_size 3 -hls_flags delete_segments %www_hls%</code></pre><p> </p><figure class="table"><table><thead><tr><th>参数</th><th>含义</th><th>备注</th></tr></thead><tbody><tr><td>-stream_loop -1</td><td>开启循环播放</td><td> </td></tr><tr><td>-re</td><td>正常播放速度</td><td> </td></tr><tr><td>-i</td><td>流媒体源</td><td> </td></tr><tr><td>-codec copy</td><td>只拷贝不转码</td><td>节省 CPU 资源</td></tr><tr><td>-hls_time 10</td><td>每个分片大小，10 秒</td><td>默认 10 秒</td></tr><tr><td>-hls_list_size 3</td><td>播放列表内片段数</td><td>3 个 ts 分片</td></tr><tr><td>-hls_flags delete_segments</td><td>自动清理旧分片</td><td> </td></tr><tr><td>www_hls</td><td>播放列表名称</td><td>分片的前缀</td></tr><tr><td>-v quiet</td><td>静默模式</td><td>可选</td></tr></tbody></table></figure><p>FFmpeg 在运行过程中会动态地创建、删除 ts 媒体片段并更新 m3u8 播放列表，考虑到长时间这么干这可能不利于硬盘寿命，这里再加一个 <a href="http://memory.dataram.com/products-and-services/software/ramdisk" target="_blank">RAMDisk</a> 虚拟磁盘服务，它可以将一部分运行内存映射为支持文件系统的基本磁盘，把 FFmpeg 生成的这部分动态文件放在运存。</p><figure class="image ss-img-wrapper"><img src="https://cdn.sspai.com/2024/02/08/37fdea016492695ba6b9c286f5e2df3a.png?imageView2/2/w/1120/q/90/interlace/1/ignore-error/1"/><figcaption>RAMDisk 配置、效果</figcaption></figure><figure class="image ss-img-wrapper"><img src="https://cdn.sspai.com/2024/02/08/dc39dc5e56eac9541470bcc982963047.png?imageView2/2/w/1120/q/90/interlace/1/ignore-error/1"/><figcaption>FFmpeg 运行中</figcaption></figure><p>现在，流媒体内容已经有了，还需要一个 Web 中间件提供 HTTP 下载服务，我想起了用于创建个人网盘的 <a href="https://github.com/sigoden/dufs" target="_blank">dufs</a> 程序，这是一个轻量级 Web 服务器，可以方便地把整个文件夹映射出去。</p><pre class="language-shell"><code># CMD

dufs.exe E:\hls\ -b 0.0.0.0 -p 8081
Listening on:
  http://127.0.0.1:8081/
  http://192.168.1.6:8081/
  http://192.168.29.1:8081/
  http://192.168.244.1:8081/</code></pre><h2>试播</h2><p>启动内网穿透，启动 Safari，输入 dufs 列出的地址，点击 sax.m3u8，熟悉的声音从扬声器响起，HLS 媒体流没有问题，它可以。</p><figure class="image ss-img-wrapper"><img src="https://cdn.sspai.com/2024/02/09/c60415d5e86b84dd2e35bfe8b0fafdea.png?imageView2/2/w/1120/q/90/interlace/1/ignore-error/1"/></figure><p>从 dufs 的输出可以直观地理解 HLS 是如何工作的</p><pre class="language-null"><code>2024-02-08T19:50:09+08:00 INFO - 192.168.1.10 "GET /" 200
2024-02-08T19:50:33+08:00 INFO - 192.168.1.10 "GET /sax.m3u8" 200
2024-02-08T19:50:33+08:00 INFO - 192.168.1.10 "GET /sax1.ts" 200
2024-02-08T19:50:33+08:00 INFO - 192.168.1.10 "GET /sax2.ts" 200
2024-02-08T19:50:33+08:00 INFO - 192.168.1.10 "GET /sax3.ts" 200
2024-02-08T19:50:43+08:00 INFO - 192.168.1.10 "GET /sax.m3u8" 200
2024-02-08T19:50:43+08:00 INFO - 192.168.1.10 "GET /sax4.ts" 200
2024-02-08T19:50:53+08:00 INFO - 192.168.1.10 "GET /sax.m3u8" 200
2024-02-08T19:50:53+08:00 INFO - 192.168.1.10 "GET /sax5.ts" 200</code></pre><p>按照 Apple 的介绍，每次下载多少分片、怎么播放，均由 Safari 的算法决定（黑盒），用户目前能控制的是：</p><ul><li>定义流媒体类型「直播 or 点播」</li><li>每个片段的长度</li><li>m3u8 列表内至多存放几个片段</li></ul><p>因为我多数使用场景是在通勤的途中，我会侧重于如何节约流量，这其中：Safari 在点播和直播的下载策略完全不同，Safari 会把点播的内容全部预加载「不能省」，遇到直播则是追着下「能省」，m3u8 列表有更新就下载分片，但点播的好处在于：你可以自由地拖进度条，直播则似乎需要更多的设计和调整才能做到，也可能完全不行「目前」。</p><hr/><p>那么事情到这里算结束了吗？答案是：并没有</p><p>原因在于，这界面实在是有点丑，我只愿称它为 My Broadcast 0.1，它应该可以套个更好的壳，有标题，有说明，能同时展示多个播放列表那种。</p><pre class="language-htmlembedded"><code>&lt;html&gt;
&lt;head&gt;
&lt;title&gt;My Radio Stream&lt;/title&gt;
&lt;meta name="viewport" content="width=device-width, initial-scale=1" /&gt;
&lt;meta http-equiv="Content-Type" content="text/html;charset=UTF-8" /&gt;

&lt;style&gt;
@media (prefers-color-scheme: dark) &#123;
    body &#123;
        background-color: black;
        color: white;
    &#125;
&#125;
main &#123;
    width: auto;
    font-family: "MicrosoftYaHei";
&#125;
section &#123;padding: 0.5em;&#125;
h1 &#123;
    padding-top: 0.5em;
    text-align: center;
&#125;
audio &#123;width: 70%;&#125;
&lt;/style&gt;
&lt;/head&gt;

&lt;body&gt;
    &lt;main&gt;
        &lt;h1&gt;My Broadcast&lt;/h1&gt;
        &lt;section&gt;
            &lt;h2&gt;Playlist - Sax&lt;/h2&gt;
            &lt;audio controls&gt;
              &lt;source src="http://192.168.1.6:8081/hls/sax.m3u8" type="audio/mpeg"&gt;
              Your browser does not support the audio element.
            &lt;/audio&gt;
      &lt;h2&gt;Playlist - Disco&lt;/h2&gt;
            &lt;audio controls&gt;
              &lt;source src="http://192.168.1.6:8081/hls/disco.m3u8" type="audio/mpeg"&gt;
              Your browser does not support the audio element.
            &lt;/audio&gt;
            &lt;h2&gt;VOA English Global Format: international&lt;/h2&gt;
            &lt;audio controls&gt;
              &lt;source src="https://voa-ingest.akamaized.net/hls/live/2035200/161_352R/playlist.m3u8" type="audio/mpeg"&gt;
              Your browser does not support the audio element.
            &lt;/audio&gt;
        &lt;/section&gt;
    &lt;/main&gt;
&lt;/body&gt;
&lt;/html&gt;</code></pre><p>把其它来源的 HLS 串流整合进来，一起来看看效果</p><figure class="image ss-img-wrapper image_resized" style="width: 329px;"><img src="https://cdn.sspai.com/2024/02/09/56677af13b7d550d158d20959be793fb.png?imageView2/2/w/1120/q/90/interlace/1/ignore-error/1"/><figcaption>现在是不是好多了</figcaption></figure><p>经测试，这个电台服务效果还是很不错的，整套方案已尽可能将性能需求压至最低，这样的好处是你可以把它跑在一些低功耗平台中，就算日夜运行，也不至于电费大幅上涨。</p><p>最后，祝大家在新的一年，都能依自己的心意，听歌，听好歌。</p><h2>延伸阅读</h2><ul><li><a href="https://developer.apple.com/documentation/http-live-streaming" target="_blank">HTTP Live Streaming Overview</a></li><li><a href="https://github.com/CharonChui/AndroidNote/blob/master/VideoDevelopment/%E6%B5%81%E5%AA%92%E4%BD%93%E5%8D%8F%E8%AE%AE/HLS.md" target="_blank">HLS 协议笔记</a></li><li><a href="https://developer.apple.com/cn/news/?id=lve6alo6" target="_blank">了解 HLS 流媒体</a></li><li><a href="https://developer.apple.com/documentation/http-live-streaming/preparing-audio-for-http-live-streaming" target="_blank">Preparing Audio for HTTP Live Streaming</a></li><li><a href="https://developer.apple.com/streaming/examples/" target="_blank">Streaming Examples</a></li><li><a href="https://get233.com/archives/support-macOS-dark-mode-in-safari-web.html" target="_blank">如何使网页自动适配 Dark Mode</a></li></ul><p style="margin-left: 0px;">&gt; 关注 <a href="https://sspai.com/s/J71e">少数派公众号</a>，解锁全新阅读体验 📰</p><p style="margin-left: 0px;">&gt; 实用、好用的 <a href="https://sspai.com/mall">正版软件</a>，少数派为你呈现 🚀</p>
</div></div>
</div>

<div>
[原文](https://sspai.com/post/86398)
</div>

