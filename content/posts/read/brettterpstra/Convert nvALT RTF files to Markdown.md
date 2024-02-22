---
title: 'Convert nvALT RTF files to Markdown'
categories: ['brettterpstra']
date: 2024-02-08T11:23:00-06:00
lastmod: 2024-02-08T11:23:00-06:00
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

<div> nvALT, RTF, Markdown, Shortcut, Conversion<br/>
这篇文章介绍了一个将RTF文件转换为Markdown的快捷方式，帮助那些想从nvALT转移到其他应用的用户。作者提到了从nvALT转移到nvUltra或Obsidian等Markdown应用的情况，并分享了一个使用Shortcuts的解决方案。他还提到了对Shortcuts的使用方法和可能的问题，并鼓励读者提出改进建议或疑问。总的来说，这篇文章是一个为nvALT用户提供帮助的实用指南。<br/><br/>总结: 这篇文章介绍了如何使用Shortcuts将RTF文件转换为Markdown，以帮助nvALT用户迁移到其他应用。提供了详细的使用方法和可能的问题，并鼓励读者参与讨论。 <div>
<p>I’ve been working with a former nvALT user who stored all of their files in RTF format. Ideally, people switching from nvALT to another app — be it nvUltra, Obsidian, or anything Markdown-based — would already be storing their notes as individual text files. If nvALT is still working for you, make that change now and give it a chance to write all the new files to disk. However, if the conversion isn’t what you hoped for, or nvALT is no longer working on your machine and you’re stuck with a bunch of RTF files, I’ve pulled together a solution.</p>
<h3 id="thanks-for-the-assist">Thanks for the assist</h3>
<p>A big thanks to those on <a href="https://forum.brettterpstra.com">the forum</a> and some help from Mastodon, especially @atnbueno and @jackwellborn, for helping me get a grasp on some more advanced Shortcuts implementations. The following solution should work with zero extra dependencies, i.e. you don’t have to install Pandoc or anything like that.</p>
<h3 id="usage">Usage</h3>
<p>To use the Shortcut, just <a href="https://brettterpstra.com#dl">download below</a>, double click to unzip, and then double click the resulting <code class="language-plaintext highlighter-rouge">.shortcut</code> file to add it to the Shortcuts app. Then just run it from the main screen (click the Play icon). It will first ask you for a source folder, at which point you’ll select the folder containing all of the RTF files. You may be presented with some permissions dialogs as it parses and converts the files, mostly around allowing access to web domains. Don’t worry, the Shortcut isn’t actually accessing those domains or sending any information to them. Once the conversion has run, you’ll get another file dialog at which point you’ll create or select an output folder for the Markdown files.</p>
<p>I’ve tested this on a collection of about 500 notes and it works pretty well. There are some things that don’t convert quite right, especially when lists are created in RTF using individual bullet markers. Those aren’t recognized as lists and will not be converted to Markdown lists. They still look correct in the output, though.</p>
<h3 id="dl">Download</h3>
<div class="download" id="dlbox"><h4>nvALT RTF to Markdown Shortcut v1.0.0</h4><p class="dl-icon"><a href="https://cdn3.brettterpstra.com/downloads/nvalt2markdown1.0.0.zip" title="Download nvALT RTF to Markdown Shortcut v1.0.0"><img height="100" src="https://cdn3.brettterpstra.com/images/shortcutsicon.png" width="100"/></a></p><div class="dl-body"><p class="dl-link"><a href="https://cdn3.brettterpstra.com/downloads/nvalt2markdown1.0.0.zip" title="Download nvALT RTF to Markdown Shortcut v1.0.0">Download nvALT RTF to Markdown Shortcut v1.0.0</a></p><p class="dl-description">A Shortcut to convert a folder of RTF files into Markdown for use in apps like Obsidian or nvUltra.</p><p class="dl-published">Published 02/08/24.</p><p class="dl-updated">Updated 02/08/24. <a class="changelog" href="https://brettterpstra.com">Changelog</a></p><p class="dl-info"><a href="https://brettterpstra.com//donate/">Donate</a> • <a href="https://brettterpstra.com//2024/02/08/convert-nvalt-rtf-files-to-markdown" title="More information on nvALT RTF to Markdown Shortcut">More info…</a></p></div></div>
<p>Give it a shot. If you’re a Shortcuts pro and have suggestions for improving it, let me know. If you’re new to this stuff (like I am) and run into problems, leave a comment or join <a href="https://forum.brettterpstra.com">the forum</a> and let me know. We’ll figure it out together.</p>
<p>Like or share this post <a class="twitter" href="https://twitter.com/intent/tweet?original_referer=https%3A%2F%2Fbrettterpstra.com%2F2024%2F02%2F08%2Fconvert-nvalt-rtf-files-to-markdown%2F&amp;text=Convert+nvALT+RTF+files+to+Markdown&amp;url=https%3A%2F%2Fbrettterpstra.com%2F2024%2F02%2F08%2Fconvert-nvalt-rtf-files-to-markdown%2F&amp;via=ttscoff" rel="nofollow" target="_blank" title="Tweet this post">Twitter</a>.</p>
<hr style="margin: 40px 0;"/>
<p>BrettTerpstra.com is supported by readers like you. <a href="https://brettterpstra.com/support/">Click here if you'd like to help out.</a></p>
<p class="copyright">All materials ©2024 Brett Terpstra</p>
<p><a href="https://twitter.com/ttscoff" rel="me">Twitter</a> | <a href="https://nojack.easydns.ca/@ttscoff" rel="me">Mastodon</a> | <a href="https://github.com/ttscoff">GitHub</a> | <a href="https://brettterpstra.com/legal/privacy.html">Privacy Policy</a></p><img height="1" src="https://brett.trpstra.net/link/535/16565808.gif" width="1"/>
</div></div>
</div>

<div>
[原文](https://brett.trpstra.net/link/535/16565808/convert-nvalt-rtf-files-to-markdown)
</div>

