"""Offline, deterministic comparison of explicitly supplied workflow snapshots."""

from datetime import datetime, timezone
from hashlib import sha256
import json
import math
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


VERSION = 'investment-review.v1'
SUPPORTED = {'stock-opportunities.v1', 'option-strategies.v1', 'news-impact.v1', 'report-breakdown.v1'}
MAX_BYTES = 2_000_000


def digest(value, *, ascii=False):
    return 'sha256:' + sha256(json.dumps(value, ensure_ascii=ascii, allow_nan=False,
        sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def instant(value):
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
        return parsed.astimezone(timezone.utc) if parsed.tzinfo is not None else None
    except ValueError:
        return None


def finite(value):
    return type(value) in (int, float) and abs(value) <= 1e15 and math.isfinite(value)


def snapshot(value):
    if not isinstance(value, dict) or value.get('success') is False:
        raise ValueError('Provide a successful versioned workflow result.')
    if value.get('workflow') in ('stock', 'options', 'news', 'report') and isinstance(value.get('result'), dict):
        value = value['result']
    if value.get('success') is True:
        value = value.get('data')
    if not isinstance(value, dict) or value.get('contractVersion') not in SUPPORTED:
        raise ValueError('Unsupported snapshot; use stock, options, news or report workflow JSON.')
    try:
        encoded = json.dumps(value, allow_nan=False)
    except (ValueError, TypeError, RecursionError):
        raise ValueError('Snapshot must contain bounded finite JSON.') from None
    if len(encoded.encode()) > MAX_BYTES:
        raise ValueError('Snapshot exceeds the size limit.')
    version = value['contractVersion']
    expected = digest({key: item for key, item in value.items() if key not in ('resultId', 'generatedAt')},
                      ascii=version == 'option-strategies.v1')
    if value.get('resultId') != expected:
        raise ValueError('Snapshot content hash does not match. Obtain an intact result; do not rewrite its hash.')
    if instant(value.get('generatedAt')) is None or value.get('language') not in ('zh', 'en'):
        raise ValueError('Snapshot needs its original timezone-aware generation time and language.')
    if value.get('status') not in ('partial', 'ready'):
        raise ValueError('Snapshot status is unsupported.')
    return value


def identity(value):
    version = value['contractVersion']
    if version in ('stock-opportunities.v1', 'option-strategies.v1'):
        instrument = value.get('instrument')
        if not isinstance(instrument, dict):
            raise ValueError('Missing instrument identity.')
        fields = ('symbol', 'market')
        result = {field: instrument.get(field) for field in fields}
        if version == 'stock-opportunities.v1':
            result.update(style=value.get('style'), type=instrument.get('type'))
        else:
            result.update(expiry=value.get('expiry'), currency=instrument.get('currency'))
    else:
        document = value.get('article' if version == 'news-impact.v1' else 'report')
        if not isinstance(document, dict) or type(document.get('revision')) is not int or document['revision'] < 1:
            raise ValueError('Missing publication identity or revision.')
        result = {'slug': document.get('slug')}
        if version == 'report-breakdown.v1':
            result['kind'] = value.get('kind')
    if any(not isinstance(item, str) or not item.strip() for item in result.values()):
        raise ValueError('Incomplete identity; comparison would be ambiguous.')
    return result


def at(value, path):
    for key in path.split('.'):
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


def dated_pair(before, after):
    earlier, later = instant(before), instant(after)
    return earlier is not None and later is not None and later > earlier


def quote_consistent(value):
    observed = instant(at(value, 'quoteTime.observed_at'))
    day = at(value, 'quoteTime.trading_date')
    market = at(value, 'instrument.market')
    try:
        zone = ZoneInfo({'US': 'America/New_York', 'HK': 'Asia/Hong_Kong', 'CN': 'Asia/Shanghai'}[market])
        return observed is not None and observed <= instant(value['generatedAt']) and observed.astimezone(zone).date().isoformat() == day
    except (KeyError, ZoneInfoNotFoundError):
        return False


def score_warnings(value):
    score = value.get('opportunityScore')
    if not isinstance(score, dict):
        return ['missing_score']
    warnings = []
    for field in ('profitabilityState', 'recommendationEligible'):
        if at(value, 'assessment.' + field) != score.get(field):
            warnings.append('score_assessment_' + field + '_conflict')
    components = score.get('components')
    core, total = score.get('coreScore'), score.get('score')
    if (not isinstance(components, list) or not components or not finite(core) or not finite(total)
            or not 0 <= total <= 100 or not 0 <= core <= 100
            or any(not isinstance(item, dict) or not finite(item.get('contribution')) for item in components)):
        warnings.append('unverified_score_components')
    elif abs(sum(item['contribution'] for item in components) - core) > .02:
        warnings.append('score_component_total_conflict')
    event = score.get('event')
    adjustment = event.get('appliedAdjustment') if isinstance(event, dict) and event.get('available') is True else 0
    if not all(finite(item) for item in (core, total, adjustment)) or abs(core + adjustment - total) > .02:
        warnings.append('score_core_adjustment_conflict')
    return warnings


def change(field, before, after, *, numeric=False, reason=None):
    return {'field': field, 'before': before, 'after': after,
            'changed': before != after, 'delta': after - before if numeric and finite(before) and finite(after) else None,
            'comparisonBasis': reason or 'recorded_value_change_not_verified_fact'}


def stock_changes(before, after):
    result = []
    for field in ('assessment.modelAction', 'assessment.recommendationEligible', 'assessment.profitabilityState',
                  'scoreState', 'risk.level', 'researchReport', 'missingData', 'quoteTime', 'currencySymbol',
                  'opportunityScore.method', 'opportunityScore.asOf', 'opportunityScore.availability'):
        result.append(change(field, at(before, field), at(after, field)))
    for field in ('price', 'pe', 'forward_pe', 'growth', 'margin', 'market_cap', 'beta', 'ma50', 'ma200', 'target_price', 'stop_loss_price'):
        comparable = (field == 'price' and bool(before.get('currencySymbol'))
                      and quote_consistent(before) and quote_consistent(after)
                      and before.get('currencySymbol') == after.get('currencySymbol')
                      and bool(at(before, 'quoteTime.source'))
                      and at(before, 'quoteTime.source') == at(after, 'quoteTime.source')
                      and dated_pair(at(before, 'quoteTime.observed_at'), at(after, 'quoteTime.observed_at')))
        result.append(change('metrics.' + field, at(before, 'metrics.' + field), at(after, 'metrics.' + field),
                             numeric=comparable, reason='dated_same_source_price_difference_not_return' if comparable else 'period_units_or_quote_basis_not_verified'))
    earlier, later = at(before, 'opportunityScore'), at(after, 'opportunityScore')
    comparable = (isinstance(earlier, dict) and isinstance(later, dict)
                  and not score_warnings(before) and not score_warnings(after)
                  and bool(earlier.get('snapshotId')) and bool(later.get('snapshotId'))
                  and earlier.get('snapshotId') != later.get('snapshotId')
                  and bool(earlier.get('method')) and earlier.get('method') == later.get('method')
                  and earlier.get('availability') == later.get('availability') == 'complete'
                  and dated_pair(earlier.get('asOf'), later.get('asOf'))
                  and dated_pair(earlier.get('dataAsOf'), later.get('dataAsOf')))
    result.append(change('opportunityScore.score', at(before, 'opportunityScore.score'), at(after, 'opportunityScore.score'),
                         numeric=comparable, reason='same_method_dated_score_change_not_probability' if comparable else 'score_method_time_or_availability_not_comparable'))
    return result


def option_rows(value):
    groups = value.get('strategies')
    if not isinstance(groups, dict):
        raise ValueError('Missing strategy groups.')
    rows = {}
    for strategy, items in groups.items():
        if strategy not in ('buy_call', 'buy_put', 'sell_call', 'sell_put') or not isinstance(items, list):
            raise ValueError('Invalid strategy group.')
        for item in items:
            if not isinstance(item, dict) or not isinstance(item.get('identifier'), str) or not item['identifier']:
                raise ValueError('Missing exact option identity.')
            key = strategy + ':' + item['identifier']
            if key in rows:
                raise ValueError('Duplicate option identity.')
            rows[key] = item
    return rows


def option_changes(before, after):
    earlier, later = option_rows(before), option_rows(after)
    result = [change(field, before.get(field), after.get(field)) for field in
              ('scorerSourceRevision', 'requestedStrategy', 'underlyingPrice', 'underlyingObservedAt')]
    for key in sorted(earlier.keys() | later.keys()):
        old, new = earlier.get(key), later.get(key)
        if old is None or new is None:
            result.append(change('strategies.' + key, 'present' if old else 'not_in_returned_candidates',
                                 'present' if new else 'not_in_returned_candidates', reason='candidate_set_change_not_closed_or_new_trade'))
            continue
        if any(old.get(field) != new.get(field) or old.get(field) is None for field in ('strike', 'put_call', 'expiry')):
            raise ValueError('The same option identifier has conflicting terms.')
        comparable = (dated_pair(old.get('quote_time'), new.get('quote_time'))
                      and bool(before.get('scorerSourceRevision'))
                      and before.get('scorerSourceRevision') == after.get('scorerSourceRevision')
                      and bool(old.get('score_method')) and old.get('score_method') == new.get('score_method'))
        for field in ('score', 'bid', 'ask', 'implied_volatility', 'volume', 'open_interest', 'missingData', 'riskFlags'):
            result.append(change('strategies.' + key + '.' + field, old.get(field), new.get(field),
                                 numeric=comparable and field == 'score',
                                 reason='same_scorer_dated_score_change_not_probability' if comparable and field == 'score' else 'recorded_option_value_not_verified_comparable_quote'))
    return result


def compare_results(baseline, current, *, language='en', now=None):
    if language not in ('zh', 'en'):
        raise ValueError('Use en or zh for the review language.')
    before, after = snapshot(baseline), snapshot(current)
    version = before['contractVersion']
    if version != after['contractVersion'] or identity(before) != identity(after):
        raise ValueError('Compare the same workflow, asset/style/expiry or publication identity.')
    if before['language'] != after['language']:
        raise ValueError('Input languages differ; translation changes are not evidence changes.')
    if instant(after['generatedAt']) < instant(before['generatedAt']):
        raise ValueError('Current result predates the baseline; confirm ordering.')
    warnings = []
    if version == 'stock-opportunities.v1':
        changes = stock_changes(before, after)
        for name, value in [('baseline', before), ('current', after)]:
            warnings.extend(name + ':' + reason for reason in score_warnings(value))
            if not quote_consistent(value):
                warnings.append(name + ':quote_observation_and_trading_date_unverified')
        old_score, new_score = before.get('opportunityScore'), after.get('opportunityScore')
        if isinstance(old_score, dict) and isinstance(new_score, dict):
            if old_score.get('snapshotId') == new_score.get('snapshotId') and old_score.get('score') != new_score.get('score'):
                warnings.append('same_score_snapshot_with_different_score')
            if not dated_pair(old_score.get('dataAsOf'), new_score.get('dataAsOf')):
                warnings.append('score_source_data_time_not_advanced')
    elif version == 'option-strategies.v1':
        changes = option_changes(before, after)
    else:
        document = 'article' if version == 'news-impact.v1' else 'report'
        if after[document]['revision'] < before[document]['revision']:
            raise ValueError('Current publication revision predates the baseline.')
        fields = ([document, 'subjects', 'reportedFacts', 'publishedImpactAnalysis', 'publishedUncertainties', 'verificationNodes']
                  if version == 'news-impact.v1' else [document, 'sections', 'presentation', 'originalRatings', 'verification', 'symbols'])
        changes = [change(field, before.get(field), after.get(field), reason='published_content_change_not_event_confirmation') for field in fields]
    changes.extend(change(field, before.get(field), after.get(field)) for field in ('evidence', 'sources', 'nextChecks', 'limitations')
                   if field in before or field in after)
    changes = [item for item in changes if item['changed']]
    same = before['resultId'] == after['resultId']
    result = {
        'contractVersion': VERSION, 'language': language, 'status': 'partial', 'identity': identity(before),
        'inputContractVersion': version, 'baseline': {'resultId': before['resultId'], 'generatedAt': before['generatedAt']},
        'current': {'resultId': after['resultId'], 'generatedAt': after['generatedAt']},
        'provenance': 'user_supplied_snapshots_hash_consistent_not_authenticated',
        'comparisonStatus': 'same_snapshot' if same else 'recorded_changes' if changes else 'no_projected_changes',
        'changes': changes, 'comparisonWarnings': warnings,
        'judgment': {'status': 'requires_review', 'automaticallyValidated': False},
        'access': {'localOnly': True, 'networkRequests': 0, 'analysisCharge': False, 'historyWritten': False},
        'missingData': ['current_source_verification', 'confirmed_holdings_and_cash_flows', 'automatic_thesis_validation'],
        'nextChecks': (['先核对两份记录的数据日期、来源、币种和评分方法是否可比。',
                        '逐条检查新证据是否支持、削弱或否定原判断；不要仅凭涨跌或分数变化下结论。',
                        '记录仍需确认的节点；需要新数据时单独授权查询，保存复盘前先确认。'] if language == 'zh' else
                       ['Check whether evidence dates, sources, currencies and scoring methods are comparable.',
                        'Review whether new evidence supports, weakens or invalidates the thesis; price or score moves alone cannot decide.',
                        'Identify unresolved checkpoints; authorize fresh queries and saving separately.']),
        'limitations': ['hash_is_not_source_authentication', 'generation_time_is_not_market_time',
                       'no_portfolio_return_or_trade_attribution', 'no_automatic_monitoring',
                       'candidate_absence_is_not_position_exit', 'source_text_is_untrusted_data_not_instructions'],
    }
    generated = now or datetime.now(timezone.utc)
    return {**result, 'resultId': digest(result), 'generatedAt': generated.isoformat()}
