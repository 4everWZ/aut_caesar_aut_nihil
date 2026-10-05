#!/usr/bin/env python3
"""Read-only Warband text inventory/export and zh_CN validation (Python 3 stdlib)."""
from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict
import hashlib
import io
import json
from pathlib import Path
import re
import sys
import tokenize

ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / 'Aut_Caesar_Aut_Nihil'
LOCALE = MODULE / 'languages/cns'
DOCS = ROOT / 'docs/localization'


def words(row):
    # NBSP and other Unicode spaces can be literal text, not engine separators.
    return re.findall(r'[^ \t\r\n]+', row)


def skip_operations(tokens, start):
    """Skip WRECK's count, then (opcode, argc, args...) records; never guess text."""
    count = int(tokens[start])
    assert count >= 0
    pos = start + 1
    for _ in range(count):
        int(tokens[pos])
        argc = int(tokens[pos + 1])
        assert argc >= 0
        pos += 2 + argc
        assert pos <= len(tokens)
    return pos


def classification(text):
    if '{!}' in text:
        return 'nontranslatable_marker'
    if re.fullmatch(r'(?:0x)?[0-9a-fA-F]{20,}', text):
        return 'hex_data'
    # Engine interpolation alone is intentionally not a translated sentence.
    stripped = re.sub(r'\{[^{}]*\}', lambda m: m[0] if '?' in m[0] or '/' in m[0] else '', text).strip(' ^_.,:;!?+-/\\()[]0123456789%')
    if not stripped:
        return 'format_only'
    return 'text'


def inventory():
    records = []
    hashes = {}
    def lines(name):
        path = MODULE / name
        data = path.read_bytes()
        hashes[name] = hashlib.sha256(data).hexdigest()
        return data.decode('utf-8-sig').splitlines()
    def add(category, key, text, source, line, runtime=True, decode=True):
        text = text.replace('_', ' ') if decode else text
        records.append(dict(category=category, id=key, text=text,
                            source=source, line=line, runtime=runtime,
                            classification=classification(text)))
    for filename in ('hints.csv', 'ui.csv', 'uimain.csv'):
        name = 'languages/en/' + filename
        for n, row in enumerate(lines(name), 1):
            if row.strip():
                key, text = row.split('|', 1)
                add(filename, key, text, name, n, decode=False)
    specs = [('strings.txt', 'game_strings.csv', 'str_'),
             ('quick_strings.txt', 'quick_strings.csv', 'qstr_'),
             ('factions.txt', 'factions.csv', 'fac_'),
             ('troops.txt', 'troops.csv', 'trp_'),
             ('item_kinds1.txt', 'item_kinds.csv', 'itm_'),
             ('party_templates.txt', 'party_templates.csv', 'pt_'),
             ('parties.txt', 'parties.csv', 'p_'),
             ('quests.txt', 'quests.csv', 'qst_'),
             ('skills.txt', 'skills.csv', 'skl_'),
             ('info_pages.txt', 'info_pages.csv', 'ip_')]
    for source, category, prefix in specs:
        source_lines = lines(source)
        found = 0
        for n, row in enumerate(source_lines, 1):
            t = words(row)
            indexes = [i for i, word in enumerate(t) if word.startswith(prefix)]
            if not indexes:
                continue
            i = indexes[0]
            key = t[i]
            found += 1
            add(category, key, t[i+1], source, n)
            if prefix in ('trp_', 'itm_'):
                add(category, key + '_pl', t[i+2], source, n)
            if prefix == 'qst_':
                add(category, key + '_text', t[i+3], source, n)
            if prefix == 'skl_':
                add(category, key + '_desc', t[i+4], source, n)
            if prefix == 'ip_':
                add(category, key + '_text', t[i+2], source, n)
        expected = int(source_lines[0 if prefix in ('skl_', 'qstr_') else 1].split()[0])
        if found != expected:
            raise ValueError(f'{source}: parsed {found} records; header says {expected}')
    source = 'conversation.txt'
    rows = lines(source)
    found = 0
    for n, row in enumerate(rows[2:], 3):
        if not row.strip():
            continue
        t = words(row)
        assert t[0].startswith('dlga_')
        pos = skip_operations(t, 3)
        add('dialogs.csv', t[0], t[pos], source, n)
        end = skip_operations(t, pos + 2)
        assert end + 1 == len(t), (source, n)
        found += 1
    assert found == int(rows[1])
    source = 'menus.txt'
    rows = lines(source)
    n = 2
    found = 0
    while n < len(rows):
        if not rows[n].strip():
            n += 1
            continue
        t = words(rows[n])
        assert t[0].startswith('menu_')
        add('game_menus.csv', t[0], t[2], source, n+1)
        pos = skip_operations(t, 4)
        assert pos + 1 == len(t)
        options = int(t[pos])
        t = words(rows[n+1])
        pos = 0
        for _ in range(options):
            key = t[pos]
            assert key.startswith('mno_')
            pos = skip_operations(t, pos+1)
            add('game_menus.csv', key, t[pos], source, n+2)
            pos = skip_operations(t, pos+1)
            # Final door-name field is an engine identifier, not menu prose.
            pos += 1
        assert pos == len(t), (source, n+2)
        found += 1
        n += 2
    assert found == int(rows[1])
    source = 'Data/item_modifiers.txt'
    for n, row in enumerate(lines(source), 1):
        t = words(row)
        if t:
            assert len(t) == 4 and t[0].startswith('imod_')
            add('item_modifiers.csv', t[0], t[1], source, n)
    source = 'skins.txt'
    for n, row in enumerate(lines(source), 1):
        for m in re.finditer(r'\b(skinkey_\S+)\s+(?:\S+\s+){4}(\S+)', row):
            add('skins.csv', m[1], m[2], source, n)
    return records, hashes


def signatures(text):
    """Preserve register multiplicity, branching shape, printf, breaks and escapes.

    Branch prose can change; branch selectors and order cannot. Nested braces are
    parsed recursively. Plain brace tokens remain byte-for-byte stable.
    """
    tokens = []
    def split_branches(value, delimiter):
        branches, start, depth = [], 0, 0
        for pos, char in enumerate(value):
            depth += (char == '{') - (char == '}')
            if char == delimiter and depth == 0:
                branches.append(value[start:pos])
                start = pos + 1
        branches.append(value[start:])
        return branches

    def scan(value):
        pos = 0
        while pos < len(value):
            if value[pos] == '}':
                raise ValueError('unmatched closing brace')
            if value[pos] != '{':
                pos += 1
                continue
            end, depth = pos + 1, 1
            while end < len(value) and depth:
                depth += (value[end] == '{') - (value[end] == '}')
                end += 1
            if depth:
                raise ValueError('unclosed brace')
            body = value[pos+1:end-1]
            conditional = re.match(r'^(reg\d+)\?(.*)$', body, re.S)
            if conditional:
                branches = split_branches(conditional[2], ':')
                tokens.append(('condition', conditional[1], len(branches)))
                for index, branch in enumerate(branches):
                    before = len(tokens)
                    scan(branch)
                    tokens[before:] = [('branch', conditional[1], index, t) for t in tokens[before:]]
            elif '/' in body and not re.match(r'^(s|reg)\d', body):
                branches = split_branches(body, '/')
                tokens.append(('gender', len(branches)))
                for index, branch in enumerate(branches):
                    before = len(tokens)
                    scan(branch)
                    tokens[before:] = [('gender_branch', index, t) for t in tokens[before:]]
            else:
                tokens.append(('brace', body))
            pos = end
    scan(text)
    # A percentage after a number/register followed by prose (e.g. {reg1}% from)
    # is not sprintf's space-flag conversion '% f'. Keep real '% f' elsewhere.
    matches = re.finditer(r'%%|%(?:\d+\$)?[-+#0 ]*\d*(?:\.\d+)?[diuoxXfFeEgGcs]', text)
    printf = [m[0] for m in matches if not (m[0].startswith('% ') and m.start() > 0
              and (text[m.start()-1].isdigit() or text[m.start()-1] == '}'))]
    tokens.append(('percent_count', text.count('%')))
    tokens += [('printf', x) for x in printf]
    tokens.append(('printf_order', tuple(x for x in printf if x != '%%')))
    tokens += [('break', x) for x in re.findall(r'\^+', text)]
    tokens += [('escape', x) for x in re.findall(r'\\[nrt\\]', text)]
    tokens += [('ampersand_escape', x) for x in re.findall(r'&&', text)]
    return Counter(tokens)


def source_audit():
    """Tokenize source, without executing the mod or fabricating compiled IDs."""
    report = {}
    for path in sorted((ROOT / 'module_system').rglob('*.py')):
        if not (path.name.startswith('module_') or 'systems' in path.parts or
                'strings_character_names' in path.parts):
            continue
        data = path.read_bytes()
        count = quick = 0
        try:
            for tok in tokenize.tokenize(io.BytesIO(data).readline):
                if tok.type == tokenize.STRING:
                    count += 1
                    try:
                        value = ast.literal_eval(tok.string)
                        quick += isinstance(value, str) and value.startswith('@')
                    except (ValueError, SyntaxError):
                        pass
            report[str(path.relative_to(ROOT))] = dict(string_literals=count,
                quick_string_literals=quick, sha256=hashlib.sha256(data).hexdigest())
        except (tokenize.TokenError, SyntaxError) as err:
            raise ValueError(f'Cannot inventory {path}: {err}') from err
    return report


def grouped(records):
    groups = defaultdict(lambda: defaultdict(list))
    for record in records:
        groups[record['category']][record['id']].append(record)
    return groups


def validate(groups):
    errors, translated, unchanged, delivered = [], defaultdict(set), defaultdict(set), {}
    for path in sorted(LOCALE.glob('*.csv')):
        seen = set()
        delivered[path.name] = []
        data = path.read_bytes()
        if not data.startswith(b'\xef\xbb\xbf'):
            errors.append(f'{path.name}: expected UTF-8 BOM (project convention)')
        try:
            content = data.decode('utf-8-sig')
        except UnicodeDecodeError as err:
            errors.append(f'{path.name}: not UTF-8: {err}')
            continue
        for number, row in enumerate(content.splitlines(), 1):
            label = f'{path.name}:{number}'
            if not row.strip():
                continue
            if row.count('|') != 1 or '\x00' in row or '\ufeff' in row:
                errors.append(f'{label}: malformed delimiter/control character')
                continue
            key, text = row.split('|')
            if key in seen:
                errors.append(f'{label}: duplicate ID {key}')
            seen.add(key)
            delivered[path.name].append(key)
            sources = groups.get(path.name, {}).get(key)
            if not sources or not all(r['runtime'] for r in sources):
                errors.append(f'{label}: unknown/unverified ID {key}')
                continue
            if not text.strip() and any(r['text'].strip() for r in sources):
                errors.append(f'{label}: empty translation')
            variants = {r['text'] for r in sources}
            try:
                sig = signatures(text)
                if any(sig != signatures(source) for source in variants):
                    errors.append(f'{label}: formatting/placeholder mismatch {key}')
            except ValueError as err:
                errors.append(f'{label}: {key}: {err}')
            if any('{!}' in source for source in variants) and text not in variants:
                errors.append(f'{label}: translated nontranslatable marker {key}')
            if text in variants:
                unchanged[path.name].add(key)
            else:
                translated[path.name].add(key)
    return errors, translated, unchanged, delivered


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path, help='Write summary JSON')
    parser.add_argument('--missing', type=Path, help='Write untranslated ID/English/location JSON')
    parser.add_argument('--export-dir', type=Path, help='Export unique eligible source IDs as English CSV; never overwrites cns')
    parser.add_argument('--check', action='store_true', help='Check pinned source hashes and milestone IDs')
    parser.add_argument('--pin', action='store_true', help='Explicitly refresh source/milestone baseline after review')
    args = parser.parse_args()
    records, hashes = inventory()
    groups = grouped(records)
    errors, translated, unchanged, delivered = validate(groups)
    source_format_issues = []
    for record in records:
        try:
            signatures(record['text'])
            if '|' in record['text']:
                source_format_issues.append(dict(id=record['id'], source=record['source'], line=record['line'], issue='literal pipe in source; engine escaping requires review'))
        except ValueError as err:
            source_format_issues.append(dict(id=record['id'], source=record['source'], line=record['line'], issue=str(err)))
    audit = source_audit()
    baseline = {'compiled_sha256': hashes, 'module_source': audit, 'milestone_ids': delivered}
    baseline_path = DOCS / 'baseline.json'
    if args.pin:
        if errors:
            parser.error('cannot pin invalid localization')
        baseline_path.write_text(json.dumps(baseline, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if args.check:
        old = json.loads(baseline_path.read_text(encoding='utf-8'))
        for field in ('compiled_sha256', 'module_source'):
            if old[field] != baseline[field]:
                errors.append(f'{field}: source drift; re-inventory and review before --pin')
        for category, ids in old['milestone_ids'].items():
            missing = set(ids) - set(delivered.get(category, []))
            if missing:
                errors.append(f'{category}: missing {len(missing)} milestone IDs: {sorted(missing)[:10]}')
    categories = {}
    missing_records, collisions = [], {}
    for category, entries in sorted(groups.items()):
        eligible = {key for key, variants in entries.items() if any(r['classification'] == 'text' for r in variants)}
        ambiguous = {key: sorted({r['text'] for r in variants}) for key, variants in entries.items()
                     if len({r['text'] for r in variants}) > 1}
        collisions[category] = ambiguous
        done = eligible & translated[category]
        categories[category] = dict(occurrences=sum(map(len, entries.values())), unique_ids=len(entries),
            text_ids=len(eligible), translated_text_ids=len(done),
            untranslated_text_ids=len(eligible - done), unchanged_entries=len(unchanged[category]),
            conflicting_ids=len(ambiguous), runtime_id_convention_verified=all(r['runtime'] for v in entries.values() for r in v),
            exact_build_engine_export_compared=False, player_visibility_verified=False)
        missing_records += [entries[key][0] for key in sorted(eligible - done)]
        if args.export_dir and category.endswith('.csv'):
            target = args.export_dir.resolve()
            if target == MODULE.resolve() or MODULE.resolve() in target.parents:
                parser.error('English export must not target the runtime module (including source/translated languages)')
            target.mkdir(parents=True, exist_ok=True)
            rows = [f"{key}|{entries[key][0]['text']}" for key in entries if key in eligible and key not in ambiguous and '|' not in entries[key][0]['text']]
            (target / category).write_text('\n'.join(rows) + '\n', encoding='utf-8-sig')
    result = dict(categories=categories, source_files=len(audit),
                  source_quick_string_literals=sum(v['quick_string_literals'] for v in audit.values()),
                  errors=errors, conflicting_source_ids=collisions, source_format_issues=source_format_issues)
    if args.report:
        args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if args.missing:
        args.missing.write_text(json.dumps(missing_records, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for category, stats in categories.items():
        print(f"{category:22} {stats['translated_text_ids']:5}/{stats['text_ids']:5} text IDs translated; "
              f"{stats['conflicting_ids']} source collisions")
    for error in errors:
        print('ERROR:', error, file=sys.stderr)
    print(f'{len(source_format_issues)} pre-existing source formatting issue(s) (see --report)')
    print(f'{len(errors)} error(s); {len(missing_records)} text IDs remain untranslated; {len(audit)} source files audited')
    return bool(errors)


if __name__ == '__main__':
    sys.exit(main())
