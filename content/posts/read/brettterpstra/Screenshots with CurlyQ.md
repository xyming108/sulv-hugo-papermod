---
title: 'Screenshots with CurlyQ'
categories: ['brettterpstra']
keywords: ['brettterpstra']
date: 2024-01-17T14:26:00-06:00
lastmod: 2024-01-17T14:26:00-06:00
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
    image: cdn.g0f.cn/?r=https://brett.trpstra.net&url=https://cdn3.brettterpstra.com/uploads/2024/01/curlyq_screenshot_header-rb.jpg
    alt: "'Screenshots with CurlyQ'"
    relative: false
---

<div>

<div> 截图功能, 动态网页, Selenium, CurlyQ, 改进
总结:
本文介绍了CurlyQ工具的新功能和改进。首先是返回结果的格式统一为数组，即使只有一个结果。其次是添加了--query功能，可以使用jq-like语法查询多个项目，进行属性比较等。最后介绍了CurlyQ的截图功能，通过Selenium可以对动态网页进行截图，并提供了详细的命令行参数说明。文章强调了CurlyQ仍在持续改进，并欢迎读者的反馈和建议。 <div>
<noscript class="loading-lazy">
<source media="(max-width: 640px)"/>
<source type="image/webp"/>
<source/>
<img alt="CurlyQ Screenshot banner image" class="aligncenter" height="226" src="cdn.g0f.cn/?r=https://brett.trpstra.net&url=https://cdn3.brettterpstra.com/uploads/2024/01/curlyq_screenshot_header-rb.jpg" title="CurlyQ Screenshot banner image" width="800"/>
</noscript>
<p>I’ve been putting a little more time into <a href="https://brettterpstra.com/projects/curlyq/" title="CurlyQ">CurlyQ</a> this week, as I’m able.</p>
<p>First thing to note is a breaking change: it will always return an array now, even if there’s only one result. I had waffled on this a little, but for predictability in scripting it really always needs to be a consistent format. So even a single-string result, e.g. a command that targets a single element with <code class="language-plaintext highlighter-rouge">--search</code> and then uses <code class="language-plaintext highlighter-rouge">.source</code> in the query (which previously would have just returned the source string for the matched tag) will now return an array containing a single string.</p>
<p>Secondly, I’ve put a considerable amount of effort into the <code class="language-plaintext highlighter-rouge">--query</code> feature. You can now use <code class="language-plaintext highlighter-rouge">jq</code>-like syntax to query multiple items in an array, use dot-syntax for attribute comparisons, and use comparisons (like <code class="language-plaintext highlighter-rouge">^=</code>) on hashes, returning true if any value in the hash matches the query. Still, if you want the full power of something like <code class="language-plaintext highlighter-rouge">jq</code> or <code class="language-plaintext highlighter-rouge">yq</code>, you can just pipe the output to either and work with more familiar tools.</p>
<p>But on to a cool thing. I mentioned CurlyQ’s screenshot capability in the intro post, but it’s received some improvements, and I thought it deserved a little more detail.</p>
<!--more-->
<p>I incorporated <a href="https://www.selenium.dev/" title="Selenium">Selenium</a> to allow scraping of dynamic web pages. One of the features Selenium provides is screenshots saved from the browser of choice. Thus CurlyQ has a screenshot feature:</p>
<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight fixed"><code>curlyq screenshot -b 'firefox' -t 'full' -o 'screenshot_name' URL</code></pre></div></div>
<p>The <code class="language-plaintext highlighter-rouge">--browser</code> flag (<code class="language-plaintext highlighter-rouge">-b</code>) determines whether it uses Chrome or Firefox, and the selected browser must be installed on your system. The full-page capture (<code class="language-plaintext highlighter-rouge">-t full</code>) is only available with Firefox. Chrome can only output <code class="language-plaintext highlighter-rouge">visible</code> (the visible part of the page on first load) and <code class="language-plaintext highlighter-rouge">print</code>, a print version of the page with <code class="language-plaintext highlighter-rouge">@media print</code> styling applied. Firefox can output all types.</p>
<p>The <code class="language-plaintext highlighter-rouge">--type</code> flag (<code class="language-plaintext highlighter-rouge">-t</code>) accepts <code class="language-plaintext highlighter-rouge">full</code>, <code class="language-plaintext highlighter-rouge">visible</code>, and <code class="language-plaintext highlighter-rouge">print</code>. With <code class="language-plaintext highlighter-rouge">-t full</code> and <code class="language-plaintext highlighter-rouge">-b firefox</code>, you get a full-length version of the rendered page, including offscreen elements. All of these can be abbreviated to their first letter, e.g. <code class="language-plaintext highlighter-rouge">-t f</code> or <code class="language-plaintext highlighter-rouge">-b c</code>.</p>
<p>The <code class="language-plaintext highlighter-rouge">--output</code> flag (<code class="language-plaintext highlighter-rouge">-o</code>) is required and determines the path/name of the output file. Providing just a name will save the file to the current directory. Extensions can be provided but will be changed depending on output type, <code class="language-plaintext highlighter-rouge">.png</code> for <code class="language-plaintext highlighter-rouge">full</code> and <code class="language-plaintext highlighter-rouge">visible</code>, <code class="language-plaintext highlighter-rouge">.pdf</code> for <code class="language-plaintext highlighter-rouge">print</code>. So you can just provide a name without extension and CurlyQ will apply the appropriate extension.</p>
<p>As a side note, saving a screenshot with <code class="language-plaintext highlighter-rouge">-t print</code> will output a PDF with actual text that can be searched by Spotlight (and other tools). So you could ostensibly use CurlyQ to crawl an entire site (by parsing the <code class="language-plaintext highlighter-rouge">links</code> subcommand output and spidering) and save every page to a searchable PDF. I don’t know offhand why you’d do that, but it’s possible.</p>
<p>CurlyQ is still being refined and your input is welcome. Join me on the <a href="https://forum.brettterpstra.com">Forum</a>, or just message me on <a href="https://nojack.easydns.ca/@ttscoff/">Mastodon</a> with suggestions and bug reports.</p>
<p>See the <a href="https://brettterpstra.com/projects/curlyq/" title="CurlyQ">project page</a> for full details.</p>
<p>Like or share this post <a href="https://nojack.easydns.ca/users/ttscoff/statuses/111773247408751942" target="_blank" title="This post on Mastodon">on Mastodon</a> or <a class="twitter" href="https://twitter.com/intent/tweet?original_referer=https%3A%2F%2Fbrettterpstra.com%2F2024%2F01%2F17%2Fscreenshots-with-curlyq%2F&amp;text=Screenshots+with+CurlyQ&amp;url=https%3A%2F%2Fbrettterpstra.com%2F2024%2F01%2F17%2Fscreenshots-with-curlyq%2F&amp;via=ttscoff" rel="nofollow" target="_blank" title="Tweet this post">Twitter</a>.</p>
<hr style="margin: 40px 0;"/>
<p>BrettTerpstra.com is supported by readers like you. <a href="https://brettterpstra.com/support/">Click here if you'd like to help out.</a></p>
<p class="copyright">All materials ©2024 Brett Terpstra</p>
<p><a href="https://twitter.com/ttscoff" rel="me">Twitter</a> | <a href="https://nojack.easydns.ca/@ttscoff" rel="me">Mastodon</a> | <a href="https://github.com/ttscoff">GitHub</a> | <a href="https://brettterpstra.com/legal/privacy.html">Privacy Policy</a></p><img height="1" src="cdn.g0f.cn/?r=https://brett.trpstra.net&url=https://brett.trpstra.net/link/535/16537593.gif" width="1"/>
</div></div>
</div>

<div>
[原文](https://brett.trpstra.net/link/535/16537593/screenshots-with-curlyq)
</div>

