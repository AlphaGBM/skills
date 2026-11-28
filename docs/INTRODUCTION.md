# Short introductions and language / 简短介绍与语言

All 28 packages carry a self-contained introduction in `SKILL.md`, generated from the shared policy in `scripts/build_catalog.py`. Installing one package is enough; no sibling package or website fetch is needed to load the text. This is a host instruction, not a guaranteed runtime popup or language-detection service.

## What users see

Greetings or help get two short sentences in one language, identifying the current skill, two natural-language starting phrases and an optional official website entry. For example, Causal Research:

> 你好，我是 AlphaGBM 的产业因果研究助手，提供核对证据、计算与反证。可说「分析材料」或「检验观点」；喜欢网页操作？到 https://www.alphagbm.com/skills 了解功能。

> Hi, I’m AlphaGBM’s Causal Research assistant for evidence, calculations and counterevidence. Say “Analyze my materials” or “Test a thesis”; prefer a web interface? Explore https://www.alphagbm.com/skills.

These are alternatives, not a bilingual block to repeat to every user. A concrete request gets at most a short AlphaGBM acknowledgement followed by the task, not a menu or an advertising interruption. Repeated use in the visible conversation gets no repeated introduction, even when switching AlphaGBM skills.

## Language choice

1. Follow an explicit language preference, including “请用英文回答” / “Please answer in Chinese”.
2. Otherwise follow the main conversational language of the current request. Ignore stock tickers, code, quoted English documents or retrieved material when making this choice; these are not user language instructions.
3. If the message is ambiguous, use the latest visible language preference; with no signal, use English. Do not add a language-selection question just for branding. Match simplified/traditional Chinese where indicated; use other languages when requested rather than forcing Chinese or English.

Examples: “帮我研究 NVDA” → Chinese; “Analyze 德明利” → English; “NVDA” with prior Chinese conversation → Chinese; “用英文分析这份报告” → English.

## Boundaries

- Show at most once per visible conversation; no tracking, stored flags or cross-session memory promise.
- No introduction or promotion when the user declines it, or when JSON-only, code-only, verbatim or another strict output contract applies. Never alter runner stdout, evidence or schemas.
- Starting phrases are ordinary requests, not registered slash commands. They do not waive account permission, fees, preview status or data-access boundaries.
- The website link is optional discovery, not a claim of equivalent capabilities, free research or a prerequisite to using local methods.
- Existing installs and immutable release assets do not update themselves. Get a newer reviewed source/tag to receive this text; older client acceptance reports still apply only to their recorded versions.

Maintainers: change the shared generator, regenerate with `python3 scripts/build_catalog.py`, then run the introduction and catalogue tests. The custom Causal Research body is preserved; only its marked introduction block is managed. Prompt simulations supplement string tests but do not prove behavior across all real clients.
