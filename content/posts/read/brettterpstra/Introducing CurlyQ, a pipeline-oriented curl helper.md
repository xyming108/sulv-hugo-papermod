---
title: 'Introducing CurlyQ, a pipeline-oriented curl helper'
categories: ['brettterpstra']
date: 2024-01-10T10:48:00-06:00
lastmod: 2024-01-10T10:48:00-06:00
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

<div> 工具, 网页抓取, 元数据, 图像, 功能

这个工具叫做CurlyQ，是一个网页抓取助手，不仅可以获取网页内容，还可以提供元数据、页面图像、页面链接等内容，并且可以处理动态页面和截取截图。它设计成为脚本管道的一部分，可以轻松实现获取页面标题、找到页面上最大的图像或检查并验证页面上的所有链接等功能。CurlyQ还具有多种用户代理字符串配置以及元数据处理功能。它还支持JSON响应处理、页面元素检索以及截图功能。未来版本将支持POST请求功能。如果你对这个工具有任何需求或意见，请在GitHub上的讨论中提出。希望这个工具能成为一个通用的网页抓取工具。

<br/><br/>总结: 这个工具叫CurlyQ，是一个网页抓取助手，支持获取网页内容、元数据处理、页面元素检索、截图等功能。希望能成为一个通用的网页抓取工具。 <div>
<noscript class="loading-lazy">
<source media="(max-width: 640px)"/>
<source type="image/webp"/>
<source/>
<img alt="curlyq_header-rb.jpg" class="aligncenter" height="226" src="https://cdn3.brettterpstra.com/uploads/2024/01/curlyq_header-rb.jpg" title="curlyq_header-rb.jpg" width="800"/>
</noscript>
<p>Today I’m releasing an initial version of my latest tool, <a href="https://brettterpstra.com/projects/curlyq">CurlyQ</a>. It’s a work in progress, though should be immediately useful to those who need it. I need your input on where it goes next, what’s missing, and what you’d like to do with it that it can’t handle yet. Join me <a href="https://forum.brettterpstra.com">in the forum</a> to discuss<sup id="fnref:comment"><a class="footnote" href="https://brettterpstra.com#fn:comment" rel="footnote">1</a></sup>!</p>
<p>CurlyQ is a helper for the <a href="https://www.man7.org/linux/man-pages/man1/curl.1.html">curl</a> command, with some extra functionality. Sure, it can grab the contents of a web page, but it can also provide a breakdown of all of the metadata, page images, page links, and can work with dynamic pages (where the page is loaded by a JavaScript call and the raw source is empty except for script tags). It will even do screenshots. It’s designed to alleviate some of the chores when scraping web pages or getting JSON responses.</p>
<!--more-->
<h3 id="a-scripters-tool">A Scripter’s Tool</h3>
<p>CurlyQ is designed to be part of a scripting pipeline, making it as simple as possible to do something like get a page’s title, find the largest image on the page, or examine and validate all the links on a page. You can query the results based on any attribute of the returned tag, showing, for example, only links with a <code class="language-plaintext highlighter-rouge">rel=me</code> attribute or a paragraph with a certain class. The <code class="language-plaintext highlighter-rouge">tags</code> subcommand can output a hierarchy of all tags on the page, with each parent tag containing a <code class="language-plaintext highlighter-rouge">tags</code> key with its immediate children, on down the line. This can be queried and filtered using command line flags.</p>
<h3 id="failure-prevention">Failure Prevention</h3>
<p>This tool has multiple User Agent strings configured and can accept custom headers. If a request fails, it will try again with various User Agent strings. This is because some sites block pages with certain (or missing) User Agents, and some don’t, so it has a built-in retry. It can also handle pages that respond with gzipped data using <code class="language-plaintext highlighter-rouge">--compressed</code> on the command line. If you don’t use <code class="language-plaintext highlighter-rouge">--compressed</code> and it detects gzipped data, it will quietly fail and notify you that you need to add the flag. I may make this an automatic fallback in the future. You can also specify a browser as a fallback (Chrome or Firefox), so if regular curling fails or is blocked, it can actually load the page in a web browser and retrieve/process the source from the window.</p>
<h3 id="retrieving-page-elements">Retrieving Page Elements</h3>
<p>CurlyQ also incorporates Nokogiri, allowing it to perform element selection using CSS selectors or XPaths. For example, the <code class="language-plaintext highlighter-rouge">html</code> command accepts <code class="language-plaintext highlighter-rouge">--search 'article header h3'</code> to return an array of all h3s contained in a header tag inside an article tag on the page. It can output as JSON or YAML, and for queries that target a specific element or key in the response, you can output raw strings.</p>
<p>There are also tools for extracting content between two strings, returning an array of all matches on the page. The idea is that in cases where you need to extract content that might not be easily located with tags, you can provide before/after strings to extract the necessary information.</p>
<h3 id="ready-set-shoot">Ready, Set, Shoot</h3>
<p>CurlyQ can take several types of screenshots: full page (one long PNG), visible page (just the part of the page initially visible in the browser), or the print output, applying <code class="language-plaintext highlighter-rouge">@media print</code> stylesheets. It doesn’t currently offer any type of image manipulation, but it might someday at least be able to create miniature versions (thumbnails) automatically.</p>
<p>The screenshot capability works best with Firefox. You can shoot the visible part of pages using Chrome, but to get full-page screenshots, Firefox is required. CurlyQ uses <a href="https://www.selenium.dev/" title="Selenium">Selenium</a> to load up an instance of the selected browser and grab the rendered source or take a screenshot. The source is fed through the same processor as a regular curl call, so most aspects remain the same. The result is missing response header info, though. CurlyQ does not aim to be a full web automation tool, for that you’ll want to get accustomed to using a headless browser in your scripting language of choice.</p>
<h3 id="json-handling">JSON Handling</h3>
<p>There’s very limited support for handling JSON responses. It currently only handles GET requests and allows you to specify request headers, returning response headers as well as the pretty-printed (optional) results of parsing the JSON, all as one JSON or YAML blob. It’s assumed that you’ll do any handling of the results using something like <a href="https://github.com/jqlang/jq">jq</a> or <a href="https://github.com/mikefarah/yq">yq</a>. It can cycle through User Agent strings to find one that works and elegantly return a response code and headers on errors.</p>
<h3 id="whats-next">What’s Next</h3>
<p>One major area that’s missing right now is the ability to make requests other than GET. I would like to add POST capabilities, accepting data from command line flags or just passing it a JSON blob on STDIN or from a file. That’s for the next version, though.</p>
<p>I would greatly appreciate feedback on this tool. If you have a use for something like it, but it doesn’t do quite what you need, please list your use cases and expectations in the <a href="https://github.com/ttscoff/curlyq/issues">Issues</a> on GitHub. I’d love to flesh this out into an all-purpose web scraping tool.</p>
<p>See the <a href="https://brettterpstra.com/projects/curlyq">CurlyQ</a> project page for more details on installation and usage. I look forward to your feedback (in <a href="https://forum.brettterpstra.com">the forum</a> or <a href="https://github.com/ttscoff/curlyq/issues">on GitHub</a>), positive or negative!</p>
<div class="footnotes">
<ol>
<li id="fn:comment">
<p>Leaving a comment on this page will automatically create a new forum topic if there isn’t one, or add to an existing topic. <a class="reversefootnote" href="https://brettterpstra.com#fnref:comment">↩</a></p>
</li>
</ol>
</div>
<p>Like or share this post <a class="twitter" href="https://twitter.com/intent/tweet?original_referer=https%3A%2F%2Fbrettterpstra.com%2F2024%2F01%2F10%2Fintroducing-curlyq-a-pipeline-oriented-curl-helper%2F&amp;text=Introducing+CurlyQ%2C+a+pipeline-oriented+curl+helper&amp;url=https%3A%2F%2Fbrettterpstra.com%2F2024%2F01%2F10%2Fintroducing-curlyq-a-pipeline-oriented-curl-helper%2F&amp;via=ttscoff" rel="nofollow" target="_blank" title="Tweet this post">Twitter</a>.</p>
<hr style="margin: 40px 0;"/>
<p>BrettTerpstra.com is supported by readers like you. <a href="https://brettterpstra.com/support/">Click here if you'd like to help out.</a></p>
<p class="copyright">All materials ©2024 Brett Terpstra</p>
<p><a href="https://twitter.com/ttscoff" rel="me">Twitter</a> | <a href="https://nojack.easydns.ca/@ttscoff" rel="me">Mastodon</a> | <a href="https://github.com/ttscoff">GitHub</a> | <a href="https://brettterpstra.com/legal/privacy.html">Privacy Policy</a></p><img height="1" src="https://brett.trpstra.net/link/535/16526283.gif" width="1"/>
</div></div>
</div>

<div>
[原文](https://brett.trpstra.net/link/535/16526283/introducing-curlyq-a-pipeline-oriented-curl-helper)
</div>

