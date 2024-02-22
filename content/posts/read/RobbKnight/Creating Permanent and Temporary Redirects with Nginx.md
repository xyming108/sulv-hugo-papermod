---
title: 'Creating Permanent and Temporary Redirects with Nginx'
categories: ['RobbKnight']
keywords: ['RobbKnight']
date: 2024-01-01T13:16:10Z
lastmod: 2024-01-01T13:16:10Z
author: [['RobbKnight']]
tags: ['RobbKnight']
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
    image: https://www.g0f.cn/img/banner.jpg
    alt: "Creating Permanent and Temporary Redirects with Nginx"
    relative: false
---

<div>

<div> Nginx, redirects, Sublime Text, VSCode, multi-line editing
<br/><br/>总结:
本文介绍了在Nginx配置中设置永久重定向以防止旧博客链接404的方法，作者使用Sublime Text进行多行编辑，提供了针对特定URL和整个域的重定向配置示例。此外，还提到了作者在处理大量重定向时使用Sublime Text的优势。 <div>
<p>As part of a change to move my blog posts from <code>/slug-of-post</code> to <code>/blog/slug-of-post</code> I needed to set permanent redirects in my Nginx config so the old post links wouldn't 404. <a href="https://forge.laravel.com">Forge</a> has a UI for this but it only allows doing one redirect at a time and I had ~130 to do. So I grabbed a list of all my post slugs and formatted them with multi-line edit in Sublime Text<sup class="footnote-ref"><a href="https://rknight.me/feed.xml#fn1" id="fnref1">[1]</a></sup>.</p>
<p>Add the following to your Nginx config to do a redirect for a specific URL. In my case, this lives at <code>/etc/nginx/sites-available/rknight.me</code>.</p>
<pre class="language-nginx"><code class="language-nginx"><span class="token directive"><span class="token keyword">server</span></span> <span class="token punctuation">&#123;</span><br/>    <span class="token comment"># 301 Moved Permanently</span><br/>    <span class="token directive"><span class="token keyword">rewrite</span> ^/slug-of-post /blog/slug-of-post permanent</span><span class="token punctuation">;</span><br/><br/>    <span class="token comment"># 302 Found/Moved Temporarily</span><br/>    <span class="token directive"><span class="token keyword">rewrite</span> ^/slug-of-post /blog/slug-of-post redirect</span><span class="token punctuation">;</span><br/><br/>    <span class="token comment"># the rest of your nginx config here</span><br/><span class="token punctuation">&#125;</span></code></pre>
<p>You can also do this for a whole domain. Although I didn't need to do this, it's worth noting here as well.</p>
<pre class="language-nginx"><code class="language-nginx"><span class="token directive"><span class="token keyword">server</span></span> <span class="token punctuation">&#123;</span><br/>    <span class="token comment"># redirect the root of the domain</span><br/>    <span class="token directive"><span class="token keyword">rewrite</span> ^/$ http://new.example.com permanent</span><span class="token punctuation">;</span><br/><br/>    <span class="token comment"># preserve paths</span><br/>    <span class="token directive"><span class="token keyword">rewrite</span> ^/(.*)$ http://new.example.com/<span class="token variable">$1</span> permanent</span><span class="token punctuation">;</span><br/><br/>    <span class="token comment"># the rest of your nginx config here</span><br/><span class="token punctuation">&#125;</span></code></pre>
<hr class="footnotes-sep"/>
<section class="footnotes">
<ol class="footnotes-list">
<li class="footnote-item" id="fn1"><p>I use VSCode for most things, but Sublime is still the best at handling multi-line editing <a class="footnote-backref" href="https://rknight.me/feed.xml#fnref1">⤾</a></p>
</li>
</ol>
</section>
</div></div>
</div>

<div>
[原文](https://rknight.me/blog/creating-permanent-and-temporary-redirects-with-nginx/)
</div>

