# Tahák: struktury paměti LLM agenta

Paměť navrhujte ve třech krocích: **co zapisovat → jak vybavovat → co poslat modelu**. Znalost v databázi nepomůže, pokud se nenajde, nevejde do promptu nebo nemá jasnou platnost.

| Struktura | Vhodné otázky | Výhoda | Typické selhání | Kontrola |
|---|---|---|---|---|
| Poslední N zpráv | Co jsme právě domluvili? | Přesné znění | Staré rozhodnutí vypadne | Pin důležitých rozhodnutí |
| Rekurzivní summary | Jaký je cíl a dosavadní postup? | Malý kontext | Ztracená výjimka, postupný drift | Zdrojové odkazy, občasný rebuild |
| JSON / SQL stav | Jaký jazyk uživatel preferuje? | Přesný filtr, změny | Tichý overwrite, zastaralá hodnota | Verze, validita, audit |
| Epizodický log + lexical / vector index | Zažili jsme podobný incident? | Vyhledání textových zkušeností | Podobný text bez správného faktu | Metadata, reranking, zdroje |
| Knowledge Graph | Které týmy zasáhne změna této služby? | Cesty, spojování entit | Chybějící / chybná hrana | Typy hran, entity resolution, provenance |
| Ověřený runbook / procedura | Jak bezpečně zopakovat postup? | Stabilní návod | Neplatná verze postupu | Verze, podmínky, ověřování |

## Knowledge Graph versus vektorová databáze

| Aspekt | Knowledge Graph | Vektorová databáze |
|---|---|---|
| Reprezentace | Entity, typované hrany, atributy | Embeddingy chunků + text + metadata |
| Dotaz | Traversal, join, grafový pattern | Similarity / nearest neighbors, často metadata filter |
| Přirozený vstup | Vyžaduje mapování dotazu na entity a vztahy | Embedding dotazu; parafráze dle modelu |
| Více kroků | Explicitní návaznost hran | Obvykle další retrieval nebo orchestrace |
| Čas a konflikt | Musí být navržené v modelu | Musí být navržené v metadatech a filtrech |
| Zápis | Extrakce vztahů, deduplikace entit | Chunking, embedding, indexace |
| Cena chyby | Špatná hrana může propojit nesouvisející fakta | Podobný chunk může obsahovat chybný či starý fakt |
| Provoz | Indexy, transakce, kontrola schématu | RAM/index, ANN recall, refresh embeddingů |

Vektory nejsou synonymem sémantiky: TF‑IDF je také vektorová reprezentace. Neuronové embeddingy jsou vhodnější k ověření parafrází; jejich výsledky závisí na jazyku, modelu a korpusu. Graf není automaticky pravdivý. Obě struktury mohou číst stejné původní zdroje a fungovat v jednom databázovém produktu.

## Minimální záznam a cyklus aktualizace

```json
{
  "id": "claim-42",
  "subject": "svc-0",
  "predicate": "owned_by",
  "object": "platform-0",
  "source_id": "migration-ticket-42",
  "valid_from": "2026-10-01T00:00:00Z",
  "valid_to": null,
  "recorded_at": "2026-10-02T10:00:00Z",
  "tenant_id": "example",
  "authority": "service-catalog"
}
```

`valid_from/to` vyjadřuje platnost v doméně; `recorded_at` čas zjištění. Změna vlastníka uzavírá platnost starého tvrzení, zachovává historii a invaliduje cache. Dedup klíč může být `(tenant, subject, predicate, source, version)`; konfliktní zdroje se musí vyhodnotit podle autority a času, ne podle embedding similarity.

```text
write(event):
  uložit originál + source_id + tenant
  validovat entity, typy a časovou platnost
  aktualizovat materializovaný stav a vztahy
  indexovat epizody; zachovat link na originál

retrieve(question, as_of, tenant, budget):
  určit intent a entity (s možností nejistoty)
  aplikovat tenant a validitu před retrieval
  textový intent → lexical / neural retrieval + reranking
  vztahový intent → traversal s omezením hloubky
  aktuální fakt → verzovaný SQL / JSON stav
  deduplikovat a vybrat důkazy do token budgetu
  vrátit text + zdroj + platnost; při chybě abstain
```

## Co měřit při produkčním pilotu

1. Připravit skutečné dotazy zvlášť pro podobnost, vztahy, aktuální a historický stav.
2. Gold důkazy a gold odpovědi určit nezávisle na retrievalu; rozdělit train/dev/test.
3. Srovnat stejné zdroje a stejný token budget; zvlášť měřit retrieval bez a s routerem.
4. Recall důkazů, úplnost cest, správnost citací, odpovědí a abstence; chyby aktualizací a tenant filtrů.
5. Tokeny skutečným tokenizerem modelu, p50/p95 celého řetězce, ingest/extraction, disk, peak RSS a cenu.
6. Přidat parapráze, šum, konflikty, přejmenování entit, chybějící hrany a změny v čase.

## Další čtení

Primární technické reference pro navazující experimenty (nejde o zdroj našich čísel):

- TF‑IDF a cosine similarity: https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction
- GraphRAG: https://microsoft.github.io/graphrag/
- Vektorové indexy a exact/approximate retrieval: https://github.com/pgvector/pgvector
- Typy a práce s grafovými vztahy: https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/
- Lost in the Middle (pozice důkazů v kontextu): https://arxiv.org/abs/2307.03172
