from i18n_a import A
from i18n_b import B
T = {**A, **B}
ORDER = ['tr', 'en', 'de', 'fr', 'es', 'it', 'pt', 'nl', 'bg', 'el', 'sr', 'hr', 'ro']
assert set(ORDER) == set(T), set(ORDER) ^ set(T)
# single-test subscriptions: a sentence in the first FAQ answer and a bullet after the first terms item
from i18n_single import SINGLE
for _l, (_faq, _term) in SINGLE.items():
    _q, _a = T[_l]['faq'][0]
    T[_l]['faq'][0] = (_q, _a + ' ' + _faq)
    T[_l]['terms']['sub'] = [T[_l]['terms']['sub'][0], _term, *T[_l]['terms']['sub'][1:]]
# no federation name anywhere (see i18n_nofei.py)
from i18n_nofei import apply as _nofei
_nofei(T)
# anonymous usage statistics (TelemetryDeck) since 2026-09-22
from i18n_telemetry import apply as _telemetry
_telemetry(T)
