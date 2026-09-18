from i18n_a import A
from i18n_b import B
T = {**A, **B}
ORDER = ['tr', 'en', 'de', 'fr', 'es', 'it', 'pt', 'nl', 'bg', 'el', 'sr', 'hr', 'ro']
assert set(ORDER) == set(T), set(ORDER) ^ set(T)
