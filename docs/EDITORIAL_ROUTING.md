# Choose news or report analysis from the published catalogue

`collection=news` includes both news and research commentary. It is not a
news-only feed. Choose the correct discovery filter, then keep the returned
slug, language and published revision together.

| What the user needs | Discovery command | Follow-up command |
| --- | --- | --- |
| Reported events and possible impact | `research --collection news --view news` | `news` |
| Published institutional views or research commentary | `research --collection news --view research` | `report` |
| AlphaGBM original research | `research --collection research` | `report` |

Add `--lang en` or `--lang zh` to discovery and reading. Before the follow-up,
replace its slug/revision placeholders with values from the selected article.
Never run placeholders literally.

On supporting servers each article includes `workflow`: `id`, `kind`,
`command`, `contractVersion`, a relative `endpoint`, `parameters` (language and
revision), and `access: public_read`. The runner checks the expected route and
identity; it never executes an arbitrary command or URL from the response.
This describes which reader can accept the article, not whether all evidence is
available. It does not open the private report database or start paid analysis.

Older servers may omit `workflow`. Use the category filters above and the
existing versioned readers. Do not infer that every item in `collection=news`
supports `news`, and do not hide an unavailable reader behind generated prose.

## Handle errors without silently changing the task

- `WORKFLOW_MISMATCH` (422): this public item has the wrong type for the chosen
  reader. Explain the validated `details.workflow` hint. Select the indicated
  `news` or `report` command only if it matches the user's intended task; the
  runner does not retry or follow the hint automatically.
- `REVISION_CHANGED` (409): retain `details.currentRevision`, re-read the public
  article and confirm the new evidence before continuing. Do not silently remove
  the revision pin.
- `EVIDENCE_UNAVAILABLE` (422): requested-language evidence is missing or invalid.
  Report the limitation; do not silently substitute another language or a demo.
- `NOT_FOUND` (404): the article is not available publicly. Do not infer whether
  it is missing, private, withdrawn or expired, or attempt archive access.

No error authorizes a paid fallback. Public reads send no API key. Stock/options
analysis and other paid workflows keep their existing user-confirmation,
authentication and allowance requirements.
