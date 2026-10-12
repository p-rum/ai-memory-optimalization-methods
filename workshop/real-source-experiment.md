# Skutečný příklad: importy scikit-learn

Na instalovaném scikit-learn 1.8.0 jsme z AST tří skutečných modulů vytáhli import `normalize`, reexport a definici. Vektorový index pracuje se stejnými texty: 40řádkové chunky i malé důkazové fragmenty. Graf řeší explicitní importy/reexporty; je postaven z AST, nikoli z výsledků vektoru. Startovací modul a symbol jsou zadané.

| Metoda | Pokryté zdroje | Úplné | Kontext B | Medián ms |
|---|---:|---|---:|---:|
| vector@3 | 2/3 | False | 2600 | 0.286748 |
| vector@8 | 3/3 | True | 6904 | 0.261827 |
| graph | 3/3 | True | 1030 | 0.000401 |

100 opakování/dotaz; čas je warm retrieval bez AST extrakce. Jediný diagnostický dotaz nedává statistický závěr. Gold je ručně zvolené tři části importního řetězce. Pokrytí uznává i obyčejný chunk, pokud zahrnuje celý příslušný řádkový interval, nikoli jen shodu ID. Index obsahuje překryvné texty, proto lze vrátit dvě verze téhož důkazu.

Graf AST nerozpoznává dynamické importy, monkeypatching ani runtime dispatch. Vybavení s již známým modulem a symbolem je výhodnější zadání než automatické rozpoznání dotazu; toto měření je názorná ukázka práce se strukturou. Zdrojové fragmenty jsou BSD‑3‑Clause: viz SCIKIT-LEARN-COPYING.txt. Zdrojové hash a řádky v JSON umožňují audit snapshotu.

Spuštění: `python real_source_benchmark.py`; interaktivní odhalování: `source-demo.html`. HTML obsahuje referenční snapshot výsledků. Pro přepočet HTML spusťte `build_source_demo.py`.
