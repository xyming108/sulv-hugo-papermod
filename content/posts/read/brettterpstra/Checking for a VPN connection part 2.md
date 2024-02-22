---
title: 'Checking for a VPN connection part 2'
categories: ['brettterpstra']
keywords: ['brettterpstra']
date: 2024-01-30T10:14:00-06:00
lastmod: 2024-01-30T10:14:00-06:00
author: [['brettterpstra']]
tags: ['brettterpstra']
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
    image: cdn.g0f.cn/?r=https://brett.trpstra.net&url=https://brett.trpstra.net/link/535/16553334.gif
    alt: "'Checking for a VPN connection part 2'"
    relative: false
---

<div>

<div> scutil, VPN连接, 脚本, grep, 网络接口

VPN连接状态检测的脚本可以通过使用scutil命令和grep来进行。通过检查返回值来确定VPN连接的状态，这个脚本可以让你更清晰地监控VPN的连接情况。总结: scutil命令和grep在脚本中被用来检测VPN连接状态，让你能够更有效地管理网络接口变化。 <div>
<p>Ok, so I wrote <a href="https://brettterpstra.com//2024/01/29/checking-for-a-vpn-connection-from-the-command-line/">yesterday</a> about a solution for checking your VPN connection via a network interface change, but it turns out there’s a better way to do it. I discovered it shortly after posting (StackExchange thread), and received a few comments mentioning it. So here’s part two.</p>
<p>The command is <code class="language-plaintext highlighter-rouge">scutil</code>, used for managing (s)ystem (c)onfiguration parameters. The command <code class="language-plaintext highlighter-rouge">scutil --nc list</code> will show your available VPN devices and their state, either <code class="language-plaintext highlighter-rouge">Connected</code> or <code class="language-plaintext highlighter-rouge">Disconnected</code>. By doing a case-sensitive grep for <code class="language-plaintext highlighter-rouge">Connected</code> we can determine if one or more is connected.</p>
<p>So now the script just look like:</p>
<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight fixed"><code><span class="c">#!/bin/bash</span>

<span class="k">while </span><span class="nb">true</span><span class="p">;</span> <span class="k">do
  </span><span class="nv">RES</span><span class="o">=</span><span class="sb">`</span>scutil <span class="nt">--nc</span> list | <span class="nb">grep</span> <span class="nt">-c</span> Connected<span class="sb">`</span>
  <span class="o">[[</span> <span class="nv">$RES</span> <span class="o">==</span> 0 <span class="o">]]</span> <span class="o">&amp;&amp;</span> <span class="nb">break
  sleep </span>1
<span class="k">done

</span>say <span class="s2">"VPN disconnected"</span></code></pre></div></div>
<p>The <code class="language-plaintext highlighter-rouge">scutil --nc list | grep -c Connected</code> should return 0 if no VPN is connected, which you can then use to light up a button, integrate into launch/quit scripts, etc. Just a cleaner way to do what I showed yesterday.</p>
<p>Trevor Manternach has an interesting post using <a href="https://trevormanternach.com/2024/01/12/using-bartender-to-only-display-wireguard-icon-if-connected-to-vpn/">this trick with Wirecast and Bartender</a>.</p>
<p>Like or share this post <a class="twitter" href="https://twitter.com/intent/tweet?original_referer=https%3A%2F%2Fbrettterpstra.com%2F2024%2F01%2F30%2Fchecking-for-a-vpn-connection-part-2%2F&amp;text=Checking+for+a+VPN+connection+part+2&amp;url=https%3A%2F%2Fbrettterpstra.com%2F2024%2F01%2F30%2Fchecking-for-a-vpn-connection-part-2%2F&amp;via=ttscoff" rel="nofollow" target="_blank" title="Tweet this post">Twitter</a>.</p>
<hr style="margin: 40px 0;"/>
<p>BrettTerpstra.com is supported by readers like you. <a href="https://brettterpstra.com/support/">Click here if you'd like to help out.</a></p>
<p class="copyright">All materials ©2024 Brett Terpstra</p>
<p><a href="https://twitter.com/ttscoff" rel="me">Twitter</a> | <a href="https://nojack.easydns.ca/@ttscoff" rel="me">Mastodon</a> | <a href="https://github.com/ttscoff">GitHub</a> | <a href="https://brettterpstra.com/legal/privacy.html">Privacy Policy</a></p><img height="1" src="cdn.g0f.cn/?r=https://brett.trpstra.net&url=https://brett.trpstra.net/link/535/16553334.gif" width="1"/>
</div></div>
</div>

<div>
[原文](https://brett.trpstra.net/link/535/16553334/checking-for-a-vpn-connection-part-2)
</div>

