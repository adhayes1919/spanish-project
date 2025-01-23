import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import conjugations from "./assets/conjugations.json" with { type: "json" };
//NOTE: "(node:48608) ExperimentalWarning: Importing JSON modules is an experimental feature and might change at any time"

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const spanishWordsTxt = fs.readFileSync(
        path.resolve(__dirname, "./assets/es.txt"),
        "utf8");
const spanishWordsArray = spanishWordsTxt.split("\n").map(word => word.trim());
const spanishWordSet = new Set(spanishWordsArray);
export function isSpanishWord(word){
    return spanishWordSet.has(word.toLowerCase());
}
//CONJUGATION ISSUES:
//TODO: regional conjugations, make this not just "usted"

//TODO: participles are irregular in different ways than the normal verbs, yes? 
//      * so separate database for irregular participles, which will be fine because I will already be doing extra overhead on these verbs 
//TODO: note that future subjunctive is archaic?
//TODO: imperfect subjunctive has two forms, im only choosing one for right now
//TODO: technically conditional need not strip verb? but probably easiest tbh
//  also conditional is the same regardless of verb?

//
export function containsInvalidCharacters(verb) {
    return /[^.!¡?¿A-Za-záéíóúüñÁÉÍÓÚÜÑ]/.test(verb);
}

//TODO: check if word is spanish word. Ngrams?
export function classifyVerb(inputVerb) {
// ensure verb
    // then check what the ending of the verb is 
    // if not valid, quit
    if (typeof(inputVerb) !== "string") {
        console.error(`Error: inputVerb must be string. Got: ${typeof(inputVerb)}`);
        return null;
    }
    else if ((inputVerb.length < 2) || (containsInvalidCharacters(inputVerb))) {
        console.error(`Error: inputVerb must only contain 2 or more alphabetic characters)`);
        return null;
    }
    else if (!isSpanishWord(inputVerb)) {
        console.error(`Error: inputVerb not in local dictionary. NOTE: this could be an error`);
        return null;
    }
    
    let verb = inputVerb.toLowerCase();
    let verbEnding = verb.slice(-2);
    const validVerbEndings = new Set(["ar", "er", "ir"]);

    let verbType; //TODO: ensure only AR ER IR are valid options? 
    if (validVerbEndings.has(verbEnding)) {
        return verbEnding;
    } else {
        console.error(`Error: inputVerb not a verb. Does not end in "ar", "er", or, "ir")`);
        return null;
    }
}

//TODO: handle multiple pronouns 
//TODO: handle compound verbs (verbs with haber or estar)
//  if (tenses that are compound) { 
//      fetch relevant participle then 
//          conjugateVerb(either haber or estar)
//      return both 
//  }
export function conjugateVerb(inputVerb, mood, tense, pronoun) { 
    //TODO: could reasonably check if any of their types are not strings, but i think my later code handles that anyway
    if (!(inputVerb) || (!mood) || (!tense) || !(pronoun)) {
        console.error("Error: One or more parameters null");
        return null;
    }

    const verbEnding = classifyVerb(inputVerb);
    if (!verbEnding) {
        console.error(`Error: input cannot be conjugated`);
        return null;
    }
    const conjugationChart = conjugations[verbEnding];
        if (!Object.hasOwn(conjugationChart, mood)) {
        console.error(`Error: Invalid mood "${mood}". Valid moods are: ${Object.keys(conjugationChart).join(", ")}`);
        return null;
    }

    const moodConjugations = conjugationChart[mood];

    // Validate tense
    if (!Object.hasOwn(moodConjugations, tense)) {
        console.error(`Error: Invalid tense "${tense}" for mood "${mood}". Valid tenses are: ${Object.keys(moodConjugations).join(", ")}`);
        return null;
    }

    const tenseConjugations = moodConjugations[tense];

    // Validate pronoun
    if (!Object.hasOwn(tenseConjugations, pronoun)) {
        console.error(`Error: Invalid pronoun "${pronoun}" for mood "${mood}" and tense "${tense}". Valid pronouns are: ${Object.keys(tenseConjugations).join(", ")}`);
        return null;
    }

    // Retrieve and construct the conjugated verb
    const conjugation = tenseConjugations[pronoun];
    const conjugatedVerb = inputVerb.slice(0, -2) + conjugation;

    console.log(`Conjugated Verb: ${conjugatedVerb}`);
    return conjugatedVerb;
}
//TODO: add "fetch entire table" function
