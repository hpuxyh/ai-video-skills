# Twitter/X 版 AI 信息差视频记录

这里存放 `vertical-ai-info-video-推特版` 每次成功产出的同步记录。

选题筛选逻辑维护在：

- `projects/twitter-viral-topic-screening/`

使用规则：

- 有用户给定选题时，只记录该选题产出。
- 没有给定选题时，默认按 `projects/twitter-viral-topic-screening/` 的爆款主题筛选逻辑，记录当天 5 个 X/Twitter AI 信息差选题。
- 每次成功调用后，都要同步 GitHub。
- 新一次选题前，先检查这里的历史，避免产生完全重复的选题。

推荐结构：

```text
records/twitter-ai-info-video/
  topic-history.md
  YYYY-MM-DD/
    batch-summary.md
    01-中文话题名/
      来源记录.md
      config.json
      output-index.md
    final-delivery/
      01-中文话题名/
        视频.mp4
        封面.jpg
        文案.md
      整体描述.md
      _记录/
        contact sheets
        渲染校验
        素材与来源/
```

每条历史至少记录：日期、话题、公司/产品/人物、核心推文 URL、推文作者、热度信号、信息差角度、最终导出目录。

每日任务完成后要把最终导出的成片、封面、文案、整体描述和最终素材复查包同步到 GitHub 的当日 `final-delivery/` 目录。不要上传本地 BGM 原文件、失败下载图、浏览器缓存、临时目录或重复中间产物。
