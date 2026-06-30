# Source Account Pool

这些账号用于推特版 AI 信息差视频和普通 AI 信息差视频的候选素材发现、热度判断和事实验证。账号池要定期维护，不能把任何一个账号当成唯一事实来源。

普通 AI 信息差视频也复用本账号池，但使用方式略有不同：

- 推特版：X/Twitter 核心推文通常进入最终视频，第二张图优先为推文证据卡。
- 普通版：X/Twitter 用于发现、热度、评论争议和情绪判断；最终成片截图可以优先使用媒体报道、官方页面、数据图、产品页或研究页。

## 官方号 / 创始人号优先

普通版和推特版每天自动选题时都应先看官方号和创始人/核心人物号。官方源不只加分，还决定候选是否具备可信起点。

优先级：

1. 大模型公司官方号 / 产品官方号 / 研究团队官方号。
2. 创始人、CEO、产品负责人、核心研究员、政策/安全负责人。
3. AI 快报号、媒体号、市场号用于验证扩散和争议。
4. 第三方爆料或泛热点号只能作为发现线索，不能单独成为事实锚点。

### 典型大模型公司官方号

| Account | Role | Use |
| --- | --- | --- |
| `@OpenAI` | model company official | OpenAI / ChatGPT / API / Codex / safety / release source. |
| `@AnthropicAI` | model company official | Anthropic / Claude / safety / policy / enterprise source. |
| `@ClaudeAI` | product official | Claude product updates and user-facing changes. |
| `@GoogleDeepMind` | model lab official | Gemini / DeepMind research and model releases. |
| `@GoogleAI` | AI official | Google AI research and product signals. |
| `@Google` | company official | Consumer-facing Google AI product announcements. |
| `@MetaAI` | model/company official | Meta AI product and model signals. |
| `@AIatMeta` | Meta research official | Meta AI research releases and papers. |
| `@Microsoft` | company official | Microsoft AI product and platform announcements. |
| `@MSFTResearch` | research official | Microsoft Research AI work and papers. |
| `@xAI` | model company official | xAI / Grok official source. |
| `@grok` | product official | Grok product and feature signals. |
| `@NVIDIA` | AI hardware/company official | AI hardware, data center, compute, and enterprise AI. |
| `@NVIDIAAI` | AI official | NVIDIA AI models, agents, inference, and developer stack. |
| `@MistralAI` | model company official | Mistral releases and platform changes. |
| `@Cohere` | model company official | Cohere model and enterprise AI updates. |
| `@perplexity_ai` | AI product official | Perplexity search/agent/product updates. |
| `@DeepSeek_AI` | model company official | DeepSeek model/product updates when available. |
| `@Alibaba_Qwen` | model/product official | Qwen model releases and Alibaba model signals. |
| `@TencentCloud` | company/product official | Tencent Cloud / model service and enterprise AI signals. |
| `@MiniMax__AI` | model/product official | MiniMax model and product signals. |
| `@ZhipuAI` | model company official | Zhipu / GLM model updates when available. |

Account names can drift. When an account name is uncertain, verify the current official account before treating it as an official source.

### 典型创始人 / CEO / 核心人物号

| Account | Person / role | Use |
| --- | --- | --- |
| `@sama` | Sam Altman / OpenAI | OpenAI direction, product hints, policy and company response. |
| `@gdb` | Greg Brockman / OpenAI | OpenAI product/research reposts and launch framing. |
| `@ilyasut` | Ilya Sutskever / SSI/OpenAI history | Frontier model and safety signals when active. |
| `@jackclarkSF` | Anthropic cofounder / policy | Anthropic policy, safety, and AI governance signals. |
| `@sundarpichai` | Google CEO | Google AI product/company strategy signals. |
| `@demishassabis` | Google DeepMind | DeepMind/Gemini research and model direction. |
| `@ylecun` | Meta AI | Meta AI research/opinion and controversy signals. |
| `@fchollet` | AI researcher / ARC | Model capability, reasoning, benchmark and research debate. |
| `@elonmusk` | xAI / Tesla / SpaceX | xAI, Grok, compute, AI product, and public controversy. |
| `@mustafasuleyman` | Microsoft AI | Microsoft AI product direction and public framing. |
| `@satyanadella` | Microsoft CEO | Microsoft AI strategy and enterprise adoption. |
| `@AravSrinivas` | Perplexity | Search/answer engine and agent/product signals. |

Some founders or CEOs may not have active or verified X accounts. Treat uncertain accounts as leads until verified.

## 可见互动和评论情绪

When using X/Twitter data, rely on what is visible in the user's logged-in Chrome page:

- visible replies
- visible reposts
- visible quote/spread signal
- visible likes
- visible views
- visible comment/reply samples

Do not claim API-level totals. For source notes, use wording such as `可见评论样本显示`.

Strong controversy/comment signals include:

- job anxiety, replacement, skill devaluation, or rehiring humans after AI failure
- privacy or surveillance concern, especially brain/health/child data
- medical safety or responsibility boundaries
- education and children, especially budget or teacher-replacement tension
- copyright/fairness/payment disputes
- market bubble, financial crisis, compute spending, or stock-risk arguments
- big-tech access limits, government adoption, or platform lock-in

## 爆点雷达型

作用：发现正在被押注、转发、争议化的话题。

| Account | Role | Use |
| --- | --- | --- |
| `@Polymarket` | prediction market | 看市场正在押注的 AI 发布、政策、公司事件、宏观影响。 |
| `@Kalshi` | prediction market | 补充美国合规预测市场的押注信号。 |
| `@ManifoldMarkets` | community prediction market | 找 AI 圈早期、小众但可能发酵的话题。 |
| `@unusual_whales` | market/news amplifier | 找 AI 股票、芯片、监管、公司动作的传播苗头。 |
| `@WatcherGuru` | fast news amplifier | 观察泛科技/财经快讯的扩散信号。 |

注意：这类账号是爆点雷达，不是最终事实源。必须再找官方、当事人或可信媒体验证。

## AI 快报包装型

作用：发现更适合普通人理解和短视频包装的 AI 话题。

| Account | Role | Use |
| --- | --- | --- |
| `@TheRundownAI` | AI news digest | 找普通人可理解的 AI 新闻入口。 |
| `@rowancheung` | AI creator/news curator | 看更强的个人号传播包装和标题角度。 |
| `@ArtificialAnlys` | model benchmark and pricing | 找模型价格、速度、能力、排行榜变化。 |
| `@AiBreakfast` | AI newsletter | 找产品、传闻、工具、项目更新。 |
| `@tldrnewsletter` | tech digest | 补充工程、产品、平台侧变化。 |

## 可信媒体验证型

作用：确认事实、补商业背景、补监管背景。

| Account | Role | Use |
| --- | --- | --- |
| `@ReutersTech` | wire/news verification | 高可信事实确认。 |
| `@technology` | Bloomberg Technology | 大厂、资本、芯片、监管背景。 |
| `@theinformation` | tech business reporting | 大厂内幕、商业模式和组织变化。 |
| `@TechCrunch` | startup/product news | 创业公司、融资、产品发布。 |
| `@verge` | consumer tech | 消费产品、平台入口、大众科技话题。 |
| `@WIRED` | society/security/ethics | 安全、伦理、监管、社会影响。 |
| `@VentureBeat` | enterprise AI | 企业 AI、Agent、安全、数据、开发者工具。 |

## 官方/当事人锚点型

作用：最终确认事件，并优先作为视频第二张图的核心推文来源。

优先级：

1. 事件当事人：创始人、CEO、产品负责人、研究员、政府官员、创作者本人。
2. 官方账号：公司、产品、实验室、开源项目、会议、政府机构。
3. 可信媒体报道：当官方没有清晰推文时作为备选。
4. 第三方爆款帖：只做发现线索，不做最终锚点。

常见官方/当事人方向：

- OpenAI、Anthropic、Google DeepMind、Meta AI、Microsoft、xAI、Apple。
- NVIDIA、AMD、TSMC、Broadcom、Oracle、CoreWeave 等算力链公司。
- Runway、Pika、Midjourney、ElevenLabs、Perplexity、Cursor、Lovable、Replit 等 AI 产品。
- 导演、演员、音乐人、作家、YouTuber、游戏公司、教育机构等受 AI 影响主体。
