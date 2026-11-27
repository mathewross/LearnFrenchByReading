# Spanish A1/A2/B1 review (9 stories)

Stories: es-el-autobus, es-mi-dia, es-en-la-tienda-de-ropa (A1); es-viaje-a-sevilla, es-el-nuevo-compañero, es-la-receta-de-la-abuela, es-un-dia-de-lluvia (A2); es-la-carta-de-mi-abuelo, es-un-pueblo-en-la-montana (B1). All pass `build.py --check` (clean). `cover` fields and JSON indent preserved.

Overall: Spanish is natural and level-appropriate; translations accurate. Main problems were story-logic slips, names missing from the text, and per-occurrence POS/gloss overrides.

## Fixed
- es-viaje-a-sevilla: timeline. Train leaves at nine, journey 2.5 h, yet Lucas ate a sandwich "a mediodía" before arriving. Now "A media mañana, Lucas comió un bocadillo" and "El tren llegó a Sevilla a las once y media" (added `once` NUM).
- es-viaje-a-sevilla: "rió" -> "rio" (RAE: no tilde on monosyllables; matches `se rio` in es-un-pueblo-en-la-montana); F line updated. Other stories keep "ríe/río" etc., unaffected.
- es-viaje-a-sevilla: `junto a` made a P line (PREP "next to") instead of ADJ + "a"; "visitar a su amiga" personal `a` ov; "una calle que no conocía" `que` ov PRON; "todo recto" `todo` ov ADV. Glosses: billete (LatAm boleto/pasaje), bocadillo (LatAm sándwich).
- es-la-receta-de-la-abuela: narrator was never named in the text but summary and all quiz questions say "Sara". Added "Hoy vas a cocinar tú, Sara" (+ PROPN Sara). Dish made explicit: "su receta de tortilla de patatas" (quiz `why` quoted that exact sentence, which did not exist). `Solo necesitas` ov ADV "only"; "el domingo que viene" `que` ov PRON. patata gloss notes LatAm papa.
- es-un-dia-de-lluvia: logic hole. A customer "took it by mistake" yet the waiter still had the umbrella. Now "Un cliente lo tomó por error y lo devolvió" (+ `devolver`). Added a reason for the return visit ("volvió a la cafetería para preguntar por su paraguas", F preguntar infinitive). `fuerte` ov "heavy" (rain), personal `a` ov ("ver a su hermana"). EN "since last night".
- es-el-nuevo-compañero: summary named "Clara", who does not appear in the story (narrator is an unnamed woman); summary now neutral. Ovs: `mucho` -> ADV (x2), `todos` -> PRON "everyone" (x3), `comida` = "lunch", `mesa` = "desk (Spain; LatAm escritorio)".
- es-la-carta-de-mi-abuelo: the mother said "Tu abuelo nunca habló de ninguna Elena" about her own father; now "Mi padre nunca habló..." (+ F padre). Relative `que` (x4: pueblo, tía Pilar, recuerdos, "lo que decía") ov -> PRON. Quiz Q4 `why` claimed Elena "kept" the letters (text says she never sent them); corrected. Glosses: coche (carro/auto), sello (estampilla).
- es-un-pueblo-en-la-montana: summary "A overworked" -> "An overworked". Relative `que` x3 ov PRON. EN "encontró a un pastor" -> "came across". móvil gloss (LatAm celular).
- es-el-autobus: EN "in a big street" -> "on a big street"; "Este es el número doce" and "Esta no es la calle" `este/esta` ov PRON; quiz Q2 `why` now quotes the text; billete gloss (LatAm boleto/pasaje).
- es-mi-dia: EN "The class is English" -> "It is an English class"; "I am red" -> "I am red in the face"; `mucho` in "ríen mucho" ov ADV; "Hasta la profesora" `hasta` ov ADV "even".
- es-en-la-tienda-de-ropa: "una talla grande" (which in Spanish means "large") changed to "una talla más grande" to match "bigger size"; `este` in "¿Es este el precio?" ov PRON; quiz Q1/Q3 `why` quotes now match the text (previous Q3 quoted "Son cuarenta euros", not in text). chaqueta gloss (LatAm campera/chamarra).

## Checked, no change needed
- `tarde`: ADV in autobus/sevilla/lluvia ("llegar tarde", "era tarde"), NOUN "afternoon" in mi-dia/nuevo-compañero/carta/pueblo; carta already has ov ADV where needed. Correct.
- `lo/la/las/los` object-pronoun ovs (receta, lluvia, carta, pueblo) have correct token indices.
- `se rio` (pueblo) and `se rieron` are consistent with the sidecar F lines.
- Quiz answer indices verified against the text in all nine stories; inference questions in the B1 stories are genuine inferences.
- Sentence lengths and tense use within level limits (max 10 / 13 / 21 words).

## Notes / left as is
- Spain-leaning but understood everywhere, left: bocadillo, tapas, todo recto (LatAm "derecho"), "el domingo que viene", "me pasé de parada", "la comida" (lunch), "la sala", "macetas", "linterna".
- es-la-carta-de-mi-abuelo: assumes the grandfather is the mother's father (hence "mi padre"); Elena Ruiz sharing his surname is plausible but unexplained.
- es-un-dia-de-lluvia: the gift Julia carries is never mentioned again (harmless; she never reaches her sister on page).
- es-mi-dia: "Por la tarde como con mis amigos" (lunch in the afternoon) is Spain-style timing; fine.
- Unused L/F lines remain in several sidecars (e.g. mediodía, hora/horas in sevilla). Harmless.
