import json
import re
import sys
from decimal import Decimal, localcontext


def calculate(payload):
    if not isinstance(payload, dict) or set(payload) != {'operation', 'values', 'unit', 'evidenceIds'}:
        raise ValueError('Expected operation, values, unit and evidenceIds only')
    operation = payload['operation']
    if operation not in ('sum', 'difference', 'ratio', 'percent_change'):
        raise ValueError('Unsupported operation')
    values = payload['values']
    if not isinstance(values, list) or not 1 <= len(values) <= 32:
        raise ValueError('Expected 1-32 decimal strings')
    if any(not isinstance(value, str) or not re.fullmatch(r'-?\d{1,15}(?:\.\d{1,8})?', value) for value in values):
        raise ValueError('Invalid or oversized decimal string')
    if operation != 'sum' and len(values) != 2:
        raise ValueError('This operation requires exactly two values')
    unit = payload['unit']
    evidence_ids = payload['evidenceIds']
    if not isinstance(unit, str) or not 1 <= len(unit.strip()) <= 80:
        raise ValueError('Expected a unit')
    if not isinstance(evidence_ids, list) or len(evidence_ids) != len(values):
        raise ValueError('Each input needs an evidence or assumption ID')
    if any(not isinstance(identifier, str) or not re.fullmatch(r'[EA][A-Za-z0-9_-]{1,39}', identifier) for identifier in evidence_ids):
        raise ValueError('Invalid evidence or assumption ID')
    with localcontext() as context:
        context.prec = 28
        numbers = [Decimal(value) for value in values]
        if operation == 'sum':
            result = sum(numbers, Decimal(0))
        elif operation == 'difference':
            result = numbers[0] - numbers[1]
        else:
            if numbers[1] == 0 or (operation == 'percent_change' and numbers[1] < 0):
                raise ValueError('Invalid denominator or non-positive growth baseline')
            result = numbers[0] / numbers[1]
            if operation == 'percent_change':
                result = (result - 1) * 100
        return {
            'status': 'executed', 'methodVersion': 'causal-research.v1.0.0',
            'inputs': payload, 'result': format(result, 'f'),
            'outputUnit': '%' if operation == 'percent_change' else 'ratio' if operation == 'ratio' else unit,
            'precisionDigits': 28, 'inputFactsVerified': False,
        }


def main():
    try:
        raw = sys.stdin.buffer.read(16385)
        if len(raw) > 16384:
            raise ValueError('Input exceeds 16KB')
        print(json.dumps(calculate(json.loads(raw)), ensure_ascii=False, allow_nan=False))
    except (ValueError, TypeError, ArithmeticError) as error:
        print(json.dumps({'status': 'error', 'error': str(error)}), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
