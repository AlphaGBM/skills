# Readable results / 清晰交付

All 28 skills include the same self-contained prose presentation policy. It is an instruction to the host, not a new UI renderer, API response schema or guaranteed client behavior. Existing strict formats take precedence; runner output and original evidence stay unchanged.

## Reading order / 阅读顺序

For research: **question and context → conclusion → up to three findings → counterevidence or reversal condition → verification notes**. Use one language, short paragraphs and at most two heading levels. Bold conclusions and important numbers, not whole paragraphs. Prefer lists on mobile; comparison tables normally have at most three columns. Do not depend on color, HTML or expandable panels.

先让用户看到判断，再看到理由，最后能够核验。每项关键发现就近标明原件位置、单位和期间；保留重要局限，不把「有条件成立」压缩成「确定成立」。找不到反证、尚未检索反证、只提出翻转条件是三种不同状态。

Simple questions get a direct answer, not a full report. Deep research still includes its method-specific evidence trail. A short answer retains compact calculation receipts and source locators; detailed files are optional and require permission to save. Never say “see attachment” or “expand evidence” unless that artifact or interface actually exists.

## Example in Chinese / 中文示意

**以下是虚构的排版示意，不是公司研究、真实来源或脚本运行回执。**

### 示例公司｜利润是否得到现金流支持？

期间：示例年度 · 来源：假设输入，仅示意 · 状态：未验证

**判断：假设数据中的经营现金流低于净利润，但不能仅凭差值判断经营恶化。**

- **差值为30个金额单位。** 假设同口径净利润80、经营现金流50；算式为80−50。输入仅用于展示，不是已核验财报。
- **原因尚不清楚。** 缺少营运资本与非现金项目资料，不能把差额全部归因于存货或回款。

### 什么会改变判断？

若原件显示差异来自可兑现的正常备货，担忧可能减轻。这是待验证条件，不是已经找到的反证；本示意未执行检索。

### 核验底稿

- 原件位置、脚本回执：无；本段只演示阅读层次。
- 下一项材料：同期间现金流补充资料。
- 被推翻的结论：无。

## Example in English

**Fictional layout example, not company research, a real source or an execution receipt.**

### Example company | Is profit supported by operating cash flow?

Period: illustrative year · Source: assumed inputs only · Status: unverified

**Finding: assumed operating cash flow is below net income; the gap alone does not establish deterioration.**

- **The gap is 30 monetary units.** Assumed comparable net income of 80 less operating cash flow of 50. These are not verified filing figures.
- **The cause is unresolved.** Working-capital and non-cash adjustments are missing; do not attribute the entire gap to inventory or collections.

### What would change the finding?

Evidence of normal inventory building with subsequent sales could weaken the concern. This is a hypothetical reversal condition, not observed counterevidence; no search was performed in this illustration.

### Verification notes

- Original locators and execution receipts: none; this is a layout example only.
- Next useful input: the cash-flow reconciliation for the same period.
- Retracted conclusions: none.

## First useful task / 首次有用任务

The Causal Research package supports the natural-language entry “Check earnings quality” / 「查利润质量」. It uses its existing financial-basis checks, demand/funding/timing questions, calculation tool and counterevidence process. This is not an additional API, professional certification or claim of superiority over other products.

已有授权材料就开始；缺资料时只问最影响结论的一项，或沿资料入口确认公开检索权限。已获授权的范围不重复确认，不要求重新安装，不默认改跑合成演示。区分宿主可用工具与本次实际读取的来源；插件市场中存在某服务，不等于已接入或调用成功。新费用、私有数据访问、上传和保存文件仍按原有权限规则处理。

## Maintainer checks

- Policy source: `scripts/build_catalog.py`; regenerate, then run `python3 -m unittest discover -s scripts -p 'test_*.py' -v` and `python3 scripts/build_catalog.py --check`.
- The standalone causal ZIP retains seven files; presentation is inline, not a dependency on this website/document. Its calculator and JSON contract are unchanged.
- Forward tests should include short Chinese/English reports, a strict JSON request, incomplete evidence, a simple question and a request that opts out of branding. Simulations are not fresh Doubao/WorkBuddy client acceptance tests.
- Previously installed copies and immutable release assets do not update automatically.
