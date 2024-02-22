---
title: 'Checking for a VPN connection from the command line'
categories: ['brettterpstra']
keywords: ['brettterpstra']
date: 2024-01-29T13:55:00-06:00
lastmod: 2024-01-29T13:55:00-06:00
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
    image: cdn.g0f.cn/?r=https://brett.trpstra.net&url=https://brett.trpstra.net/link/535/16552042.gif
    alt: "'Checking for a VPN connection from the command line'"
    relative: false
---

<div>

<div> ifconfig，VPN连接，shell脚本，Mac，自动化<br/>
总结：<br/>
本文介绍了如何使用ifconfig和shell脚本来检测VPN连接是否处于活动状态，并在连接断开时终止应用程序。通过查找特定的网络接口来确定VPN连接状态，并使用grep命令来测试连接是否处于活动状态。作者提出了使用循环的Bash脚本来监测VPN连接状态，并在连接断开时执行特定命令。同时，还提到了可以将这些方法应用于自动化工具，如BetterTouchTool。 <div>
<p>I got a question from a reader about how to test if a VPN connection is active and terminate an app if it isn’t. There’s probably a way to do this with Keyboard Maestro or BetterTouchTool or something, but to keep things interesting, I wanted to find a way to do it with just shell scripts.</p>
<h3 id="vpn-connection-indicators">VPN connection indicators</h3>
<p>I think the easiest, most universal way to determine if a VPN is connected is by searching for a specific interface that changes when connected. When I connect Nord, for example, I get a new network interface called <code class="language-plaintext highlighter-rouge">utun4</code>. I don’t know how universal this is, but you can figure out what changes happen in interfaces by comparing the output of <code class="language-plaintext highlighter-rouge">ifconfig</code> when the VPN is connected vs. disconnected.</p>
<p>The following instructions are Mac-specific, using the tools <code class="language-plaintext highlighter-rouge">pbcopy</code> and <code class="language-plaintext highlighter-rouge">pbpaste</code> to access the system clipboard rather than creating multiple files. In fact, I’m not even positive <code class="language-plaintext highlighter-rouge">ifconfig</code> is available on all systems, so if anyone wants to contribute instructions for other platforms, please do.</p>
<blockquote class="warn">
<p>Caveat: I do not understand the <code class="language-plaintext highlighter-rouge">ifconfig</code> command at all and have never used it for anything but listing network interfaces. There may be a far more succinct way to do the following.</p>
</blockquote>
<p>To determine the interface changes on a Mac:</p>
<p>In Bash:</p>
<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight fixed"><code><span class="c"># Disconnect VPN</span>
<span class="nv">$ </span>ifconfig <span class="nt">-a</span> | pbcopy
<span class="c"># Connect VPN</span>
<span class="nv">$ </span>diff &lt;<span class="o">(</span>ifconfig <span class="nt">-a</span><span class="o">)</span> &lt;<span class="o">(</span>pbpaste<span class="o">)</span></code></pre></div></div>
<p>In Zsh:</p>
<div class="language-zsh highlighter-rouge"><div class="highlight"><pre class="highlight fixed"><code><span class="c"># Disconnect VPN</span>
<span class="nv">$ </span>ifconfig <span class="nt">-a</span> | pbcopy
<span class="c"># Connect VPN</span>
<span class="nv">$ </span>diff <span class="o">=(</span>ifconfig <span class="nt">-a</span><span class="o">)</span> <span class="o">=(</span>pbpaste<span class="o">)</span></code></pre></div></div>
<p>In Fish:</p>
<pre><code class="language-fish"># Disconnect VPN
$ ifconfig -a | pbcopy
# Connect VPN
$ diff (ifconfig -a|psub) (pbpaste|psub)
</code></pre>
<p>The result should look something like:</p>
<div class="language-console highlighter-rouge"><div class="highlight"><pre class="highlight fixed"><code><span class="go">142a143,146
</span><span class="gp">&gt;</span><span class="w"> </span>utun4: <span class="nv">flags</span><span class="o">=</span>8051&lt;UP,POINTOPOINT,RUNNING,MULTICAST&gt; mtu 1420
<span class="gp">&gt;</span><span class="w">       </span><span class="nv">options</span><span class="o">=</span>6460&lt;TSO4,TSO6,CHANNEL_IO,PARTIAL_CSUM,ZEROINVERT_CSUM&gt;
<span class="gp">&gt;</span><span class="w">       </span>inet 10.5.0.2 <span class="nt">--</span><span class="o">&gt;</span> 10.5.0.2 netmask 0xffff0000
<span class="gp">&gt;</span><span class="w">       </span>nd6 <span class="nv">options</span><span class="o">=</span>201&lt;PERFORMNUD,DAD&gt;</code></pre></div></div>
<h3 id="testing-for-connection">Testing for connection</h3>
<p>Now you have an interface name (<code class="language-plaintext highlighter-rouge">utun4</code> above) that you can grep for to test whether the VPN is active. A simple loop in a Bash script will allow you to take action when the connection is disconnected. This little script assumes the VPN is connected when it starts, loops until the network interface we’re looking for disappears (<code class="language-plaintext highlighter-rouge">grep --count</code> returns 0), then executes the command after the loop.</p>
<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight fixed"><code><span class="c">#!/bin/bash</span>

<span class="k">while </span><span class="nb">true</span><span class="p">;</span> <span class="k">do
  </span><span class="nv">RES</span><span class="o">=</span><span class="sb">`</span>ifconfig <span class="nt">-a</span> | <span class="nb">grep</span> <span class="nt">-c</span> utun4<span class="sb">`</span>
  <span class="o">[[</span> <span class="nv">$RES</span> <span class="o">==</span> 0 <span class="o">]]</span> <span class="o">&amp;&amp;</span> <span class="nb">break
  sleep </span>1
<span class="k">done

</span>say <span class="s2">"VPN disconnected"</span></code></pre></div></div>
<p>Perfect if you wanted to, say, stop a torrent client if the VPN wasn’t active. You could embelish it into a launch script that checked for the VPN first, launching an app when the VPN is connected, then polled for the VPN to be disconnected, terminating the app if it is.</p>
<p>Of course, the simple <code class="language-plaintext highlighter-rouge">ifconfig -a | grep -c utun4</code> line could be used as part of a BetterTouchTool widget to display an alert on your Stream Deck when the VPN was connected, or to run any kind of automations on a polling basis. If I had more complex applications for this, I’d switch over to using <a href="https://folivora.ai/" title="BetterTouchTool">BetterTouchTool</a>.</p>
<p>Like or share this post <a href="https://nojack.easydns.ca/users/ttscoff/statuses/111841049707062712" target="_blank" title="This post on Mastodon">on Mastodon</a> or <a class="twitter" href="https://twitter.com/intent/tweet?original_referer=https%3A%2F%2Fbrettterpstra.com%2F2024%2F01%2F29%2Fchecking-for-a-vpn-connection-from-the-command-line%2F&amp;text=Checking+for+a+VPN+connection+from+the+command+line&amp;url=https%3A%2F%2Fbrettterpstra.com%2F2024%2F01%2F29%2Fchecking-for-a-vpn-connection-from-the-command-line%2F&amp;via=ttscoff" rel="nofollow" target="_blank" title="Tweet this post">Twitter</a>.</p>
<hr style="margin: 40px 0;"/>
<p>BrettTerpstra.com is supported by readers like you. <a href="https://brettterpstra.com/support/">Click here if you'd like to help out.</a></p>
<p class="copyright">All materials ©2024 Brett Terpstra</p>
<p><a href="https://twitter.com/ttscoff" rel="me">Twitter</a> | <a href="https://nojack.easydns.ca/@ttscoff" rel="me">Mastodon</a> | <a href="https://github.com/ttscoff">GitHub</a> | <a href="https://brettterpstra.com/legal/privacy.html">Privacy Policy</a></p><img height="1" src="cdn.g0f.cn/?r=https://brett.trpstra.net&url=https://brett.trpstra.net/link/535/16552042.gif" width="1"/>
</div></div>
</div>

<div>
[原文](https://brett.trpstra.net/link/535/16552042/checking-for-a-vpn-connection-from-the-command-line)
</div>

