"""Run only the bundled synthetic split example, without network or account access."""

import argparse
from decimal import Decimal, DecimalException
import json
from pathlib import Path


def positive_decimal(value):
    if not isinstance(value, str):
        raise ValueError('Expected a decimal string')
    number = Decimal(value)
    if not number.is_finite() or number <= 0:
        raise ValueError('Expected a finite positive value')
    return number


def decimal_text(value):
    return format(value.normalize(), 'f')


def evaluate(payload, language='en'):
    markers = payload['demo']
    for flag in ('synthetic', 'notForTrading', 'notLiveQuote',
                 'notInvestmentRecommendation', 'notPaidWorkflowEvidence'):
        if markers.get(flag) is not True:
            raise ValueError('Only the labelled synthetic fixture is supported')
    if payload['company']['fictional'] is not True or payload['company']['symbol'] is not None:
        raise ValueError('The demo cannot contain a real ticker')
    ratio = positive_decimal(payload['split']['newSharesPerOldShare'])
    earlier, later = payload['targets']
    if earlier['basis'] != 'pre_split' or later['basis'] != 'post_split':
        raise ValueError('Expected explicit pre-split and post-split bases')
    original = positive_decimal(earlier['value'])
    current = positive_decimal(later['value'])
    normalized = original / ratio
    change = (current - normalized) / normalized * Decimal('100')
    missing = payload['missingSplitInformation']
    if missing['basis'] != 'unknown' or missing['newSharesPerOldShare'] is not None:
        raise ValueError('Expected the missing-basis example to remain unknown')
    positive_decimal(missing['value'])
    normalized_text = decimal_text(normalized)
    current_text = decimal_text(current)
    change_text = decimal_text(change)
    if language == 'zh':
        summary = f'合成演示：统一拆股口径后，早期目标价为 {normalized_text}，后期为 {current_text}，变化 {change_text}%。口径未知项不比较。这不是真实研究或投资建议。'
    else:
        summary = f'Synthetic demo: on the same split basis, the earlier target is {normalized_text}, the later target is {current_text}, a {change_text}% change. Unknown bases remain incomparable. Not live research or investment advice.'
    return {
        'schemaVersion': 'alphagbm-split-demo.v1',
        'mode': 'synthetic_demo',
        'synthetic': True,
        'notForTrading': True,
        'notLiveQuote': True,
        'notInvestmentRecommendation': True,
        'notPaidWorkflowEvidence': True,
        'source': 'assets/stock-split-basis.json',
        'splitRatio': decimal_text(ratio),
        'currency': payload['currency'],
        'normalizedBasis': 'post_split',
        'earlierNormalizedTarget': normalized_text,
        'laterTarget': current_text,
        'splitOnlyChangePercent': decimal_text((normalized * ratio - original) / original * Decimal('100')),
        'laterChangePercent': change_text,
        'incorrectMixedBasisChangePercent': decimal_text((current - original) / original * Decimal('100')),
        'unknownTarget': {'value': missing['value'], 'status': 'unknown',
                          'normalizedValue': None, 'sameBasisChangePercent': None},
        'summary': summary,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lang', choices=('en', 'zh'), default='en')
    arguments = parser.parse_args()
    fixture = Path(__file__).resolve().parents[1] / 'assets/stock-split-basis.json'
    try:
        result = evaluate(json.loads(fixture.read_text()), arguments.lang)
    except (OSError, ValueError, KeyError, TypeError, DecimalException):
        print(json.dumps({'error': 'DEMO_UNAVAILABLE',
                          'message': 'Bundled synthetic fixture missing or invalid. Reinstall the package; no research request was made.'}))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
