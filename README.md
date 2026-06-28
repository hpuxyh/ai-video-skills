# AI Video Skills

一套面向 **AI 视频自动化创作** 的实战 Skill 集合，基于 `HyperFrames` 工作流。  
目标是把“想法 -> 脚本 -> 画面 -> 音频 -> 成片”的流程沉淀成可复用方法。

## 适合谁用

- 想批量做 AI 视频内容的创作者
- 想把视频生产流程标准化的团队
- 想把 Agent 工作流接入视频制作的开发者

## Skills 导航

| Skill | 说明 | 路径 |
|---|---|---|
| AI 信息差快报 | 新闻检索、素材匹配、口播字幕、视频渲染 | `skills/ai-tech-news-video/SKILL.md` |
| 竖屏 AI 信息差视频 | 9:16 单事件快报、多真实图片卡点轮播、结论优先信息流、无口播 BGM 成片 | `skills/vertical-ai-info-video/SKILL.md` |
| 竖屏 AI 信息差视频-推特版 | 近 2-3 天 X/Twitter AI 热点、核心推文锚点、第二张推文图双倍停留、成品导出到小红/视频/推特专用目录 | `skills/vertical-ai-info-video-推特版/SKILL.md` |
| 产品介绍视频 | 官网信息提炼、叙事结构、成片节奏 | `skills/product-intro-video/SKILL.md` |
| 视频音效工作流 | 音效搜索、下载与合成、时间线接入 | `skills/sound-fx-for-video/SKILL.md` |
| 简笔画动画视频 | 线稿风 + 短画面字；**主动网络搜参考图临摹**；逼真非抽象；GSAP 主时间线 + 可选 Anime.js；抽检闭环 | `skills/sketch-animation-video/SKILL.md` |
| Anime.js（HyperFrames） | seek 驱动适配、`window.__hfAnime` 注册、与 GSAP 分工 | `skills/animejs/SKILL.md` |

## 预览

### ai-tech-news-video
![ai-tech-news-video preview](docs/assets/preview-ai-tech-news-video.gif)

### product-intro-video
![product-intro-video preview](docs/assets/preview-product-intro-video.gif)

### sound-fx-for-video
暂无预览

### sketch-animation-video
![sketch-animation-video preview](docs/assets/preview-sketch-animation-video.gif)

### animejs
暂无预览（配套 `sketch-animation-video` 与 HyperFrames 动效接入）

## 使用方式

1. 进入对应 Skill 目录并阅读 `SKILL.md`
2. 按文档准备素材、音频与脚本
3. 在项目中执行渲染与抽检流程

`vertical-ai-info-video` 的新闻视频成品默认交付到本机：

```text
/Users/xieyahao/Desktop/我自己/小红/视频/新闻视频
```

每条新闻至少包含视频、封面、发布文案三件套，并在 `选题历史.md` 中登记，避免每日自动选题重复。

## 账号信息

- 名称：拓扑同学
- 平台：小红书
- 小红书号：`26431840972`

![小红书二维码](docs/assets/xiaohongshu-profile-qr.png)
