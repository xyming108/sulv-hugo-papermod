---
title: 'Project Planning Framework'
categories: ['byte']
keywords: ['byte']
date: 2024-01-27T00:00:00+00:00
lastmod: 2024-01-27T00:00:00+00:00
author: [['byte']]
tags: ['byte']
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
    image: cdn.g0f.cn/?r=http://lopespm.github.io&url=http://lopespm.github.io/files/project_planning_framework/compliance.png
    alt: "'Project Planning Framework'"
    relative: false
---

<div>

<div> 关键词: 框架, 目标, 时间敏感性, 项目依赖, 不确定性

总结:<br/><br/>本文介绍了一个简单的框架，用于将目标确定在三个轴定义的光谱中，从而确定实现目标的方法。作者提出的框架包括时间敏感性、目标/项目之间的依赖程度和步骤不确定性。接着作者分别用三个场景说明了如何应用该框架。第一个场景是合规性，时间敏感性高，依赖程度低，步骤不确定性低。第二个场景是增加用户流程效率，时间敏感性低，依赖程度低，步骤不确定性高。第三个场景是将多个系统统一为一个，时间敏感性低，依赖程度高，步骤不确定性中等。最后，作者强调了框架的简单性，并鼓励读者在使用框架时考虑可能的缺失参数。 <div>
<p>Different goals require different roadmapping and planning techniques.</p>
<p>In this post, a simple framework is proposed to pin a goal into a spectrum defined by three axes, the combination of which informing the approach taken to reach the goal. The three axes of this framework are:</p>
<ul>
<li><strong>Timeline sensitivity</strong>: how much leeway is there to extend the deadline to deliver a goal?</li>
<li><strong>Dependency level between goals / projects</strong>: how many steps are needed to reach the goal?</li>
<li><strong>Uncertainty of which steps will drive the goal forward</strong>: how sure are we that a given step will move us toward the goal?</li>
</ul>
<h2 id="example-of-how-to-apply-the-framework">Example of how to apply the Framework</h2>
<h3 id="scenario-1-compliance">Scenario 1: Compliance</h3>
<h4 id="goaling-statement">Goaling Statement</h4>
<p>An external entity (let’s say, government or partner company), has made a set of requirements for which your team must provide compliance for on a fixed, non-negotiable timeline, with limited team capacity. The “definition of done” is well defined by this entity, and there is a low amount of unknowns of how to reach the goals.</p>
<h4 id="axes">Axes</h4>
<ul>
<li><strong>Timeline sensitivity</strong>: High</li>
<li><strong>Dependency level between goals / projects</strong>: Low</li>
<li><strong>Uncertainty of which steps will drive the goal forward</strong>: Low</li>
</ul>
<h4 id="approach">Approach</h4>
<p>This goal has sensitive timelines and is archetypal top-down. The deadline will be reached in one way or the other, so all hands are needed on deck to tackle this goal.</p>
<p>Useful approaches could be:</p>
<ul>
<li>Use a Gant-style chart, where there is a heavy emphasis on the timeline</li>
<li>Stricter project management, more process driven</li>
</ul>
<center>
<source type="image/webp"/>
<source type="image/png"/>
<img src="cdn.g0f.cn/?r=http://lopespm.github.io&url=http://lopespm.github.io/files/project_planning_framework/compliance.png"/>
</center>
<h3 id="scenario-2-increase-effectiveness-of-a-user-flow">Scenario 2: Increase Effectiveness of a User Flow</h3>
<h4 id="goaling-statement-1">Goaling Statement</h4>
<p>Your team supports a user flow, such as a check-out flow, for which the goal is the increase the conversion amount by <em>X</em>. There are known levers you have available to drive this metric, but also many others which are unbeknownst and would need experimentation and research. This increase is not business critical, so there is an underlying lenience in case the goal is not hit.</p>
<h4 id="axes-1">Axes</h4>
<ul>
<li><strong>Timeline sensitivity</strong>: Low</li>
<li><strong>Dependency level between goals / projects</strong>: Low</li>
<li><strong>Uncertainty of which steps will drive the goal forward</strong>: High</li>
</ul>
<h4 id="approach-1">Approach</h4>
<p>Unlike Scenario 1, which is exploitation heavy, this scenario favors an approach which is exploration heavy, due to the high amount of uncertainty of which projects will be able to move the needle towards the successful completion of the goal. To de-risk and address this goal, a high level of adaptability will be needed, and several opportunities will need to be created to discover which levers can be used.</p>
<p>Useful approaches could be:</p>
<ul>
<li>Have open ended brainstorming sessions</li>
<li>User research and focus groups</li>
<li>Looser project management, to allow for quick and less trashier pivots</li>
</ul>
<center>
<source type="image/webp"/>
<source type="image/png"/>
<img src="cdn.g0f.cn/?r=http://lopespm.github.io&url=http://lopespm.github.io/files/project_planning_framework/effectiveness.png"/>
</center>
<h3 id="scenario-3-unification-of-several-systems-into-one">Scenario 3: Unification of Several Systems into One</h3>
<h4 id="goaling-statement-2">Goaling Statement</h4>
<p>Your team is tasked to unify several internal systems into a single one, where several dependencies between different projects exist, and the time each project will take ranges from certain to unknown.</p>
<h4 id="axes-2">Axes</h4>
<ul>
<li><strong>Timeline sensitivity</strong>: Low</li>
<li><strong>Dependency level between goals / projects</strong>: High</li>
<li><strong>Uncertainty of which steps will drive the goal forward</strong>: Low / Medium</li>
</ul>
<h4 id="approach-2">Approach</h4>
<p>The focus here should be on making clear which are the dependencies between different projects, and allow some leniency towards the completion of each of the projects, while actively managing the team’s capacity to focus on the projects which are discovered to require a heavier lift</p>
<p>Useful approaches could be:</p>
<ul>
<li>A full dependency graph, allowing for each of the projects timelines to have some leeway where needed</li>
<li>Incentivize highly structured systems design documents and discussions, making sure that all involved parties are aligned on a given approach, and engineers are able to explain not only the system they own, but also the other systems involved in their unification</li>
</ul>
<center>
<source type="image/webp"/>
<source type="image/png"/>
<img src="cdn.g0f.cn/?r=http://lopespm.github.io&url=http://lopespm.github.io/files/project_planning_framework/unification.png"/>
</center>
<h2 id="closing-thoughts">Closing Thoughts</h2>
<p>The framework above is quite simple and could potentially be used for several other different use cases. It might also be missing some essential parameters that are missing for your specific goal. If you do find such, I would be happy to know. Regardless, hope the above can be useful on your next roadmapping cycle</p>
</div></div>
</div>

<div>
[原文](http://lopespm.github.io/notes/2024/01/27/project_planning_framework.html)
</div>

