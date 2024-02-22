---
title: 'Generating and Caching Open Graph Images with Eleventy'
categories: ['RobbKnight']
keywords: ['RobbKnight']
date: 2023-12-24T10:09:42.501+00:00
lastmod: 2023-12-24T10:09:42.501+00:00
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
    image: cdn.g0f.cn/?r=https://rknight.me&url=https://rknight.me/assets/ogi/bloggenerating-and-caching-open-graph-images-with-eleventy.png
    alt: "Generating and Caching Open Graph Images with Eleventy"
    relative: false
---

<div>

<div> 自动生成，Open Graph 图像，插件，配置，开发模式，输出目录<br/>
文章介绍了作者如何通过自动生成的方式将Open Graph图像添加到网站上，并解决了生成图像时可能出现的效率和重建时间的问题。作者通过修改插件配置和使用开发模式生成图像，然后将其提交到存储库中。此外，作者还介绍了如何使用环境数据文件和更新基本布局来确定插件在开发模式和生产模式下的使用方式。最后，作者还解决了插件在每次更改时会删除输出目录的问题。通过这些步骤，作者成功地实现了开发模式下的Open Graph图像自动生成。<br/><br/>总结: 该文章介绍了作者如何使用自动生成的方式将Open Graph图像添加到网站上，并解决了生成图像时可能出现的效率和重建时间的问题，最终成功实现了开发模式下的Open Graph图像自动生成。 <div>
<p>I recently added automatically generated open graph images to my site using <a href="https://github.com/KiwiKilian/eleventy-plugin-og-image"><code>eleventy-plugin-og-image</code></a>. Here is the open graph image for this post:</p>
<img alt="Generating, and Caching, Open Graph Images with Eleventy" src="cdn.g0f.cn/?r=https://rknight.me&url=https://rknight.me/assets/ogi/bloggenerating-and-caching-open-graph-images-with-eleventy.png" style="border: 1px solid white;"/>
<p>I won't go over how to use the plugin; the docs on the repo and <a href="https://lewisdale.dev/post/adding-statically-generated-open-graph-images/">this blog post</a> explain that very well. What I didn't like is that these are generated every time the site builds which, aside from being wildly inefficient, added significant time to my builds.</p>
<p>I <a href="https://social.lol/@robb/111574217802419330">posted about this</a> on the 'don and <a href="https://social.lol/@sophie/111574234339127389">Sophie replied with how she is doing it</a>:</p>
<blockquote>
<p>I run it locally when I write a new post, and commit the results [...] basically the dev server will spit out the OG image</p>
</blockquote>
<p>This is exactly what I wanted - generate the images once, and commit them to the repo. To do this I had to modify the plugin config to output the images to my <code>src</code> folder instead of the output folder:</p>
<pre class="language-diff"><code class="language-diff">eleventyConfig.addPlugin(ogImagePlugin, &#123;<br/><span class="token inserted-sign inserted"><span class="token prefix inserted">+</span><span class="token line">    outputDir: 'src/assets/ogi',<br/></span></span><span class="token unchanged"><span class="token prefix unchanged"> </span><span class="token line">   satoriOptions: &#123;</span></span></code></pre>
<p>This will output the image to my <code>assets</code> directory, which in turn gets copied into my built site. This did cause a new issue though - Eleventy watches for changes in source files and rebuilds the site so every time a new image was made, Eleventy would rebuild again. To solve this, I used <code>watchesIgnore</code> in my config file:</p>
<pre class="language-js"><code class="language-js">eleventyConfig<span class="token punctuation">.</span>watchIgnores<span class="token punctuation">.</span><span class="token function">add</span><span class="token punctuation">(</span><span class="token string">'src/assets/ogi/**/*'</span><span class="token punctuation">)</span></code></pre>
<p>I only wanted these to be generated in development mode so I added an <code>env</code> data file to check the mode:</p>
<pre class="language-js"><code class="language-js">module<span class="token punctuation">.</span><span class="token function-variable function">exports</span> <span class="token operator">=</span> <span class="token keyword">function</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token punctuation">&#123;</span><br/>  <span class="token keyword">return</span> <span class="token punctuation">&#123;</span><br/>    <span class="token literal-property property">production</span><span class="token operator">:</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">ELEVENTY_RUN_MODE</span> <span class="token operator">===</span> <span class="token string">'build'</span><br/>  <span class="token punctuation">&#125;</span><br/><span class="token punctuation">&#125;</span></code></pre>
<p>Then I updated my base layout so it only uses the <code>ogImage</code> plugin when in development mode. In production, it uses the full path to the image:</p>
<pre class="language-js"><code class="language-js"><span class="token punctuation">&#123;</span><span class="token operator">%</span> <span class="token keyword">if</span> env<span class="token punctuation">.</span>production <span class="token operator">%</span><span class="token punctuation">&#125;</span><br/>    <span class="token operator">&lt;</span>meta property<span class="token operator">=</span><span class="token string">"og:image"</span> content<span class="token operator">=</span><span class="token string">"https://rknight.me/assets/ogi/&#123;&#123; page.url | slugify &#125;&#125;.png"</span><span class="token operator">&gt;</span><br/><span class="token punctuation">&#123;</span><span class="token operator">%</span> <span class="token keyword">else</span> <span class="token operator">%</span><span class="token punctuation">&#125;</span><br/>    <span class="token punctuation">&#123;</span><span class="token operator">%</span> ogImage <span class="token string">"src/og-image.og.njk"</span><span class="token punctuation">,</span> <span class="token punctuation">&#123;</span> <span class="token literal-property property">title</span><span class="token operator">:</span> title <span class="token operator">|</span> safe <span class="token punctuation">&#125;</span> <span class="token operator">%</span><span class="token punctuation">&#125;</span><br/><span class="token punctuation">&#123;</span><span class="token operator">%</span> endif <span class="token operator">%</span><span class="token punctuation">&#125;</span></code></pre>
<p>The final problem I had is the plugin will wipe the output directory on every change. <a href="https://github.com/KiwiKilian/eleventy-plugin-og-image/pull/74">This pull request</a> added that functionality and originally had an option to pass in for it to happen or not, but that option didn't make it to the final version. Based on the discussion it looked as though this wasn't something wanted in the plugin, so I made a copy of the plugin in my <code>plugins</code> directory and removed the line that deleted the files each time:</p>
<pre class="language-diff"><code class="language-diff"><span class="token deleted-sign deleted"><span class="token prefix deleted">-</span><span class="token line"> eleventyConfig.on('eleventy.before', () =&gt; &#123;<br/></span><span class="token prefix deleted">-</span><span class="token line">    const options = mergeOptions(directoriesConfig, pluginOptions);<br/></span><span class="token prefix deleted">-</span><span class="token line">    fs.rmSync(options.outputDir, &#123; recursive: true, force: true &#125;);<br/></span><span class="token prefix deleted">-</span><span class="token line"> &#125;);</span></span></code></pre>
<p>This process does require me to run <code>--serve</code> at least once each time I added a blog post but there is rarely a time where I wouldn't do that.</p>
</div></div>
</div>

<div>
[原文](https://rknight.me/blog/generating-and-caching-open-graph-images-with-eleventy/)
</div>

