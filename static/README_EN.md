Language：English | [中文](https://github.com/xyming108/sulv-hugo-papermod)

## 1. Git clone pull code

① Use `git clone` to pull the code to the desktop. At this time, the sulv Hugo papermod directory will be generated on the desktop

② Enter the sulv Hugo papermod directory and enter `git submodule update --init` to pull the submodule under themes / Hugo papermod / and put the official theme inside

## 2. Startup interface

③ Return the directory to sulv Hugo papermod, enter `hugo server -d` in the terminal, and enter: localhost:1313 in the browser to see the ready-made blog template.

## 3. Modify information

There are many personal information in the template that need to be configured by yourself. Please be patient to modify it. You can refer to the blogger's website building tutorial:[ https://www.sulvblog.cn/posts/blog/ ]( https://www.sulvblog.cn/posts/blog/ )

## 4. Hugo blog exchange group

🎉🎉 787018782 🎉🎉

## 5. How to use shortcodes

`bilibili: {{< bilibili BV1Fh411e7ZH(填 bvid) >}}`

`youtube: {{< youtube w7Ft2ymGmfc >}}`

`ppt: {{< ppt src="网址" >}}`

`douban: {{< douban src="网址" >}}`

```
#Intra article link card
#To add md at the end, you can only fill in the relative path, as shown below
{{< innerlink src="posts/tech/mysql_1.md" >}}
```

```
gallery:

{{< gallery >}}
{{< figure src="https://www.sulvblog.cn/posts/read/structural_thinking/0.png" >}}
{{< figure src="https://www.sulvblog.cn/posts/read/structural_thinking/0.png" >}}
{{< /gallery >}}
```

## 5. Possible problems


1. Some users will deploy to GitHub and may encounter cross system problems, such as the prompt `lf will be replaced by CRLF in *******`, and then enter the command: `git config core.autocrlf false`, which solves the problem of automatic conversion of line breaks。

## Using Github Pages with Github Action

If you want to deploy this template to github pages with github action please use this workflow.

```yaml
name: Deploy Hugo PaperMod Demo to Pages

on:
  push:
    paths-ignore:
      - "images/**"
      - "LICENSE"
      - "README.md"
    branches:
      - main
  workflow_dispatch:
    # manual run
    inputs:
      hugoVersion:
        description: "Hugo Version"
        required: false
        default: "0.83.0"

# Allow one concurrent deployment
concurrency:
  group: "pages"
  cancel-in-progress: true

# Default to bash
defaults:
  run:
    shell: bash

# Sets permissions of the GITHUB_TOKEN to allow deployment to GitHub Pages
permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  # Build job
  build:
    runs-on: ubuntu-latest
    env:
      HUGO_VERSION: "0.83.0"
    steps:
      - name: Check version
        if: ${{ github.event.inputs.hugoVersion }}
        run: export HUGO_VERSION="${{ github.event.inputs.hugoVersion }}"
      - name: Install Hugo CLI
        run: |
          wget -O ${{ runner.temp }}/hugo.deb https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_${HUGO_VERSION}_Linux-64bit.deb \
          && sudo dpkg -i ${{ runner.temp }}/hugo.deb
      - name: Checkout
        uses: actions/checkout@v1
      - name: Setup Pages
        id: pages
        uses: actions/configure-pages@v1
      - name: Get Theme
        run: git submodule update --init --recursive
      - name: Update theme to Latest commit
        run: git submodule update --remote --merge
      - name: Build with Hugo
        run: |
          hugo \
            --buildDrafts --gc --verbose \
            --baseURL ${{ steps.pages.outputs.base_url }}
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v1
        with:
          path: ./public
  # Deployment job
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v1
 ```
