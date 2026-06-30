# Candidate Card Template

用于每天筛选推特版 AI 信息差视频和普通 AI 信息差视频候选素材。

推特版通常把核心 X/Twitter 推文作为最终视频证据。普通版使用同一套热点/争议筛选逻辑，但最终视频截图可优先使用媒体报道、官方页面、数据图、产品页或研究页。

```yaml
topic:
working_title:
source_type:
source_accounts:
official_source:
founder_or_core_person_source:
core_tweet_url:
core_tweet_author:
discovery_account:
discovery_post_url:
visible_reply_count:
visible_repost_count:
visible_quote_signal:
visible_like_count:
visible_view_count:
visible_engagement_notes:
comment_emotion_samples:
  - sample:
    source: reply | quote | repost | search_result
    emotion: anxiety | anger | sarcasm | disagreement | excitement | distrust | fairness | safety
    why_it_matters:
  - sample:
    source: reply | quote | repost | search_result
    emotion:
    why_it_matters:
controversy_summary:
verification_url:
supporting_urls:
media_confirmation_url:
official_confirmation_url:
final_screenshot_source:
final_screenshot_type: official_page | media_report | data_chart | product_page | research_page | x_tweet | filing | other
public_theme:
  - 饭碗变化
  - 钱和市场
  - 造假和安全
  - 版权和创作者冲突
  - 大厂战争
  - 普通人马上能用的新工具
  - 孩子和教育
  - 规则变化
information_gap:
public_emotion:
  - 焦虑
  - 兴奋
  - 愤怒
  - 好奇
  - 想收藏
viral_reason:
credible_anchor:
visual_assets:
duplicate_check:
  ordinary_ai_info_video:
  twitter_ai_info_video:
score:
  official_source_credibility: 0
  visible_comment_quote_controversy: 0
  visible_repost_quote_spread: 0
  public_relevance: 0
  information_gap: 0
  media_data_evidence_quality: 0
  visual_assets: 0
  total: 0
decision:
notes:
```

## Review Questions

筛选时按顺序问：

1. 这是不是 AI 相关，而且最近 2-3 天正在发酵？
2. 它是否优先来自官方号、创始人号、产品/研究负责人号，或至少能被官方页面/可信媒体确认？
3. 它是否属于饭碗、钱、安全、版权、大厂战争、工具变化、教育、规则变化这些大众主题？
4. 它是否被 AI 快报号、媒体号、市场号、爆点号二次传播，或者可见转发/引用/浏览明显高于一般水平？
5. 可见评论/引用样本里是否存在真实争议：焦虑、愤怒、嘲讽、质疑、站队、隐私/安全/预算/饭碗担忧？
6. 是否有一句普通人能懂的反差？
7. 是否有可截图、可展示、可做封面的真实素材？
8. 普通版最终截图应该用什么最清楚：媒体报道、官方页面、数据图、产品页、研究页，还是 X/Twitter 推文？
9. 是否和普通版历史或推特版历史重复？

## Scoring For Ordinary AI Info Videos

普通 AI 信息差视频使用官方源优先的 100 分制：

| Dimension | Points | What to check |
| --- | ---: | --- |
| Official/source credibility | 25 | 官方号、创始人/核心人物号、官方页面、产品页、研究页或可信媒体确认。 |
| Visible comment/quote controversy | 20 | 可见评论/引用是否有站队、质疑、恐惧、嘲讽、愤怒、预算/饭碗/隐私/安全争论。 |
| Visible repost/quote spread | 15 | 是否被 AI 快报号、媒体号、市场号、爆点号二次传播，或核心帖可见互动明显高。 |
| Public relevance | 15 | 是否能落到工作、钱、隐私、安全、孩子、版权、医疗、工具入口、日常使用。 |
| Information gap | 10 | 是否有清晰的“大家以为 A，其实 B”。 |
| Media/data evidence quality | 10 | 是否有清楚可读的媒体、官方、数据、产品、研究或文件截图。 |
| Visual assets | 5 | 是否有可做封面的真人/公司/产品/图表/截图素材。 |

Decision bands:

- `85+`: 当天优先。
- `75-84`: 可进入前 5。
- `65-74`: 备选。
- `<65`: 默认删除，除非用户指定。

只有硬门槛过关并且分数达到当天前 5，才进入最终候选。不要把仅有 `wow/cool/amazing` 这类正向评论的帖子当作强争议选题。
