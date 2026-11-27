# Spanish A1 review (8 stories)

Stories: es-ana-en-madrid, es-en-el-mercado, es-mi-familia, es-la-cafeteria, es-el-perro-de-luis, es-un-dia-en-la-playa, es-mi-casa, es-el-cumpleanos. All pass `build.py --check` (clean) after the fixes. `cover` fields and JSON indent preserved.

Overall: Spanish is natural, A1-level, present tense only, neutral. English translations are accurate. Quizzes are correct (answer indices verified against the text).

## Fixed
- es-el-cumpleanos: "nadie dice nada" / "no dice nada" had `nada` glossed as the verb "to swim" (F nada -> nadar). Added ov to lemma `nada` PRON "nothing" on both occurrences (the playa story keeps nada = nadar, which is correct there).
- es-el-cumpleanos: `todos` (pronoun use: "todos olvidan", "gritan todos", "Gracias a todos", "Todos están") overridden to PRON "everyone".
- es-el-cumpleanos: gloss notes for Spain/LatAm variants: pastel "cake (Spain also: tarta)", coche "car (Spain; LatAm: carro, auto)". pastel is understood everywhere, kept.
- es-la-cafeteria: `mañana` F line was ADV (tomorrow) while the lemma is NOUN "morning"; F set to NOUN so POS matches "las ocho de la mañana". (es-en-el-mercado "Mañana llevo yo el pan" is correctly ADV "tomorrow"; es-mi-casa and es-el-cumpleanos "por la mañana" are NOUN.)
- es-mi-casa: ending logic. Key was singular all story ("la llave") but "¡Las llaves están en la puerta!" -> "¡La llave está en la puerta!" (EN "The key is in the door!"). The key left in the front door from the opening line ("Abro la puerta con la llave") works as a payoff; Marta's hint kept.
- es-mi-casa: the narrator's gender is never marked in the text, but summary and quiz said "man". Summary now neutral ("A proud new home-owner shows their friend Marta..."); quiz Q2 reworded to "En el jardín, ¿qué quiere abrir?" / "...does the host want to open?"; quiz Q3 reworded to singular key (answer unchanged).
- es-mi-casa: "Me gusta mucho" -> `mucho` ov ADV "a lot"; "este es el dormitorio" -> `este` ov PRON; "para todos" -> PRON.
- es-mi-familia: "Zanahoria" (the rabbit, EN "Carrot") was resolved as the common noun; ov to new L PROPN `Zanahoria`. "orejas" note "feminine plural" -> "plural" (a noun, gender is on the lemma). "Esta es mi familia": `esta` ov PRON "this".
- es-un-dia-en-la-playa: quiz Q2 "¿Quién se lleva el sombrero?" had q_en "What takes..." (wind is not a "who"); now "¿Quién o qué se lleva el sombrero?" / "Who or what takes the hat away?". "para todos" -> PRON.
- es-un-dia-en-la-playa, es-el-perro-de-luis: `detrás` is always used as a preposition ("detrás del gato / de Pablo"); F and L POS changed ADV -> PREP, gloss "behind, after".
- Personal "a" (not translatable) had gloss "to, at"; added ov "(personal a, not translated)" on: ana ("mira a Ana" x2), mercado ("mira a Mateo"), perro ("busca a Toby", "ve al perro", "ve a Toby", "toma a Toby", "mira al gato"), cumpleanos ("llama a Elena").
- Lemma glosses for gendered forms that show the masculine gloss only: señor "man, gentleman, Mr (fem. señora: lady, Mrs)" (ana, mercado, cafeteria); abuelo "(fem. abuela: grandmother)" (mercado); camarero "(fem. camarera: waitress)" (cafeteria). es-mi-casa sala "living room (Spain also: salón)".

## Checked, no change needed
- 'solo' (cafeteria "café solo" ADJ black, cumpleanos "es solo una cena" ADV just): correct.
- clitics/pronouns: me/te/se/lo/me gusta/le gusta/me llamo/se llama handled as phrases or tokens correctly; imperatives (entra, mira, ven) tagged imperative (tú).
- 'piso' (flat/floor), 'señora mayor', 'ya', 'cerca de', 'debajo' (adverb/prep use both fine as ADV).
- mercado: prices consistent ("Dos euros el kilo", "un euro el kilo", five euros given); bag breaks, ten oranges counted; plot logic fine.
- ana: second-floor neighbour, flat on the third, logic fine. Calle de la Luna fine.
- cafeteria: mixed-up orders resolved; "misma mesa" ending coherent.
- perro: cat up the tree, dog underneath; logic fine.
- cumpleanos: Javier phones, then they drive together; surprise logic fine; "Cumpleaños feliz" is the common Spain wording (LatAm also "Feliz cumpleaños").

## Notes / left as is
- Spain-leaning but widely understood words, left: coche, sala (Spain "salón"), dormitorio (LatAm also "recámara"/"cuarto"), tostada, mermelada, bolsillo, marido, galletas.
- mi-casa: "Ahora vamos al jardín" then the garden is described before the closed door is mentioned; read as looking through the door, acceptable.
- Unused F lines remain in some sidecars (e.g. churros/feliz in cafeteria). Harmless.
- The shared-quirk: lemma `mañana` is NOUN in cafeteria/mi-casa/cumpleanos sidecars but ADV in mercado, per-story, so no clash.
