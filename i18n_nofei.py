"""Removes the federation's name from the site (2026-09-22 decision: no FEI mention anywhere, no licence yet).
Generic token stripping on every string, then hand-written replacements for the FAQ item and the terms sentence."""
import re
FAQ = {
'tr': ("Bunlar resmi testler mi?", "Barn Dressage bağımsız bir antrenman oyunudur; herhangi bir federasyonla bağlantılı değildir. İzler, Children, Pony Riders ve Juniors seviyelerindeki uluslararası test düzenlerini takip eder; uygulamadaki notlar oyun puanıdır, resmi sonuç değildir."),
'en': ("Are these official tests?", "Barn Dressage is an independent training game and is not affiliated with any equestrian federation. The routes follow international test patterns at Children, Pony Riders and Juniors level; marks in the app are game scores, not official results."),
'de': ("Sind das offizielle Aufgaben?", "Barn Dressage ist ein unabhängiges Trainingsspiel und steht in keiner Verbindung zu einem Reitsportverband. Die Wege folgen internationalen Aufgabenmustern der Stufen Children, Pony Riders und Junioren; Noten in der App sind Spielpunkte, keine offiziellen Ergebnisse."),
'fr': ("S’agit-il de reprises officielles ?", "Barn Dressage est un jeu d’entraînement indépendant, sans lien avec aucune fédération équestre. Les tracés suivent les schémas de reprises internationales des niveaux Children, Poneys et Juniors ; les notes de l’app sont des scores de jeu, pas des résultats officiels."),
'es': ("¿Son pruebas oficiales?", "Barn Dressage es un juego de entrenamiento independiente y no está afiliado a ninguna federación ecuestre. Las rutas siguen los esquemas de pruebas internacionales de los niveles Children, Ponis y Juveniles; las notas de la app son puntuaciones de juego, no resultados oficiales."),
'it': ("Sono riprese ufficiali?", "Barn Dressage è un gioco di allenamento indipendente e non è affiliato ad alcuna federazione equestre. I tracciati seguono gli schemi delle riprese internazionali dei livelli Children, Pony e Juniores; i voti nell’app sono punteggi di gioco, non risultati ufficiali."),
'pt': ("São provas oficiais?", "Barn Dressage é um jogo de treino independente e não está afiliado a nenhuma federação equestre. Os traçados seguem os esquemas de provas internacionais dos níveis Children, Póneis e Juniores; as notas na app são pontuações de jogo, não resultados oficiais."),
'nl': ("Zijn dit officiële proeven?", "Barn Dressage is een onafhankelijk trainingsspel en is niet verbonden aan een ruitersportbond. De routes volgen internationale proefpatronen op Children-, Pony- en Junioren-niveau; cijfers in de app zijn spelscores, geen officiële uitslagen."),
'bg': ("Това официални тестове ли са?", "Barn Dressage е независима тренировъчна игра и не е свързана с никоя конна федерация. Трасетата следват международни схеми на тестове за нивата Children, Pony Riders и Juniors; оценките в приложението са игрови точки, не официални резултати."),
'el': ("Είναι επίσημα τεστ;", "Το Barn Dressage είναι ένα ανεξάρτητο παιχνίδι προπόνησης και δεν συνδέεται με καμία ιππική ομοσπονδία. Οι διαδρομές ακολουθούν διεθνή μοτίβα τεστ στα επίπεδα Children, Pony Riders και Juniors· οι βαθμοί στην εφαρμογή είναι βαθμολογίες παιχνιδιού, όχι επίσημα αποτελέσματα."),
'sr': ("Da li su ovo zvanični testovi?", "Barn Dressage je nezavisna igra za trening i nije povezana ni sa jednim konjičkim savezom. Staze prate međunarodne šeme testova na nivoima Children, Pony Riders i Juniors; ocene u aplikaciji su poeni igre, ne zvanični rezultati."),
'hr': ("Jesu li ovo službeni testovi?", "Barn Dressage je neovisna igra za trening i nije povezana ni s jednim konjičkim savezom. Staze slijede međunarodne sheme testova na razinama Children, Pony Riders i Juniors; ocjene u aplikaciji bodovi su igre, ne službeni rezultati."),
'ro': ("Sunt acestea probe oficiale?", "Barn Dressage este un joc de antrenament independent și nu este afiliat niciunei federații ecvestre. Traseele urmează scheme de probe internaționale la nivelurile Children, Pony Riders și Juniori; notele din aplicație sunt scoruri de joc, nu rezultate oficiale."),
}
SCORES = {
'tr': "Uygulamadaki notlar ve skorlar antrenman ve eğlence amaçlı oyun puanlarıdır; resmi dresaj sonucu değildir. Barn Dressage bağımsız bir üründür; herhangi bir federasyonla bağlantılı değildir ve onaylanmamıştır.",
'en': "Marks and scores in the app are game scores for training and fun, not official dressage results. Barn Dressage is an independent product and is not affiliated with or endorsed by any equestrian federation.",
'de': "Noten und Punkte in der App sind Spielpunkte für Training und Spaß, keine offiziellen Dressurergebnisse. Barn Dressage ist ein unabhängiges Produkt und wird von keinem Reitsportverband unterstützt.",
'fr': "Les notes et scores de l’app sont des scores de jeu, pour s’entraîner et s’amuser, pas des résultats officiels de dressage. Barn Dressage est un produit indépendant, sans lien avec aucune fédération équestre et non approuvé par elle.",
'es': "Las notas y puntuaciones de la app son puntuaciones de juego para entrenar y divertirse, no resultados oficiales de doma. Barn Dressage es un producto independiente y no está afiliado ni respaldado por ninguna federación ecuestre.",
'it': "Voti e punteggi nell’app sono punteggi di gioco per allenarsi e divertirsi, non risultati ufficiali di dressage. Barn Dressage è un prodotto indipendente, non affiliato né approvato da alcuna federazione equestre.",
'pt': "As notas e pontuações na app são pontuações de jogo para treino e diversão, não resultados oficiais de dressage. Barn Dressage é um produto independente e não está afiliado nem é aprovado por nenhuma federação equestre.",
'nl': "Cijfers en scores in de app zijn spelscores voor training en plezier, geen officiële dressuuruitslagen. Barn Dressage is een onafhankelijk product en is niet verbonden aan of goedgekeurd door een ruitersportbond.",
'bg': "Оценките и точките в приложението са игрови точки за тренировка и забавление, а не официални резултати по обездка. Barn Dressage е независим продукт и не е свързан с никоя конна федерация, нито одобрен от такава.",
'el': "Οι βαθμοί και τα σκορ στην εφαρμογή είναι βαθμολογίες παιχνιδιού για προπόνηση και διασκέδαση, όχι επίσημα αποτελέσματα ιππικής δεξιοτεχνίας. Το Barn Dressage είναι ανεξάρτητο προϊόν και δεν συνδέεται με ούτε εγκρίνεται από καμία ιππική ομοσπονδία.",
'sr': "Ocene i rezultati u aplikaciji su poeni igre za trening i zabavu, ne zvanični dresurni rezultati. Barn Dressage je nezavisan proizvod i nije povezan ni sa jednim konjičkim savezom niti ga on odobrava.",
'hr': "Ocjene i rezultati u aplikaciji bodovi su igre za trening i zabavu, ne službeni dresurni rezultati. Barn Dressage je neovisan proizvod i nije povezan ni s jednim konjičkim savezom niti ga on odobrava.",
'ro': "Notele și scorurile din aplicație sunt scoruri de joc pentru antrenament și distracție, nu rezultate oficiale de dresaj. Barn Dressage este un produs independent și nu este afiliat sau aprobat de nicio federație ecvestră.",
}
def _strip(s):
    s = re.sub(r"[^.!?]*F[ée]d[ée]ration [ÉE]questre[^.!?]*[.!?]\s*", "", s)  # the trademark sentence
    for a, b in ((" FEI-", " "), ("FEI-", ""), (" FEI ", " "), ("FEI ", ""), (" FEI", "")): s = s.replace(a, b)
    return s[:1].upper() + s[1:] if s else s
def _walk(o):
    if isinstance(o, str): return _strip(o)
    if isinstance(o, dict): return {k: _walk(v) for k, v in o.items()}
    if isinstance(o, list): return [_walk(v) for v in o]
    if isinstance(o, tuple): return tuple(_walk(v) for v in o)
    return o
def apply(T):
    for l, t in T.items():
        idx = [i for i, (q, a) in enumerate(t['faq']) if 'FEI' in q or 'FEI' in a]
        T[l] = _walk(t)
        for i in idx: T[l]['faq'][i] = FAQ[l]
        T[l]['terms']['scores'] = SCORES[l]
