import { classifyVerb, isSpanishWord, conjugateVerb } from "../regular.js";


function classifcationTest() {
    function testClassify(verb) {
        console.log(`Preparing to test classification with: ${verb}`);
        console.log(`Result: ${classifyVerb(verb)}`);
    }

    console.log("Testing valid words");
    let validWords = ["hablar", "comer", "ir"];
    validWords.forEach((verb) => testClassify(verb));

    console.log("Testing same words but capitalized");
    let capitalLetters = ["HABLAR", "COMER", "IR"];
    capitalLetters.forEach((verb) => testClassify(verb));

    /*
    // testing the following: 
     words that don't end in proper stems - manzana,
     words that aren't spanish (but end in er or ir) - fear/sir
     words that contain invalid characters
     invalid types
     invalid lengths (0 characters, 1 character)
    */

    let invalidWords = ["manzana", "adios", "fear", "sir", "est@r", "es9ar", "99", "{}", 49, "", "a", "e", "i"]
    invalidWords.forEach((verb) => testClassify(verb));
}

function conjugationTest() {
    function testConjugation(verb, mood, tense, pronoun) {
        try {
            console.log(`Testing with: verb="${verb}", mood="${mood}", tense="${tense}", pronoun="${pronoun}"`);
            const result = conjugateVerb(verb, mood, tense, pronoun);
            console.log(`Result: ${result}`);
        } catch (error) {
            console.error(`Error: ${error.message}`);
        }
    }

    // Valid verbs, moods, tenses, and pronouns
    const validVerbs = ["hablar", "comer", "vivir"];
    const validMoods = ["indicative", "subjunctive", "imperative"];
    const validTenses = {
        indicative: ["present", "preterite", "imperfect", "conditional", "future"],
        subjunctive: ["present", "imperfect", "future"],
        imperative: ["affirmative", "negative"]
    };
    const validPronouns = ["yo", "tú", "usted", "nosotros", "ustedes"];

    console.log("Testing valid input...");
    validVerbs.forEach((verb) => {
        validMoods.forEach((mood) => {
            validTenses[mood].forEach((tense) => {
                validPronouns.forEach((pronoun) => {
                    testConjugation(verb, mood, tense, pronoun);
                });
            });
        });
    });

    // Invalid input tests
    // TODO: could've made this auto validate invalid inputs but little use now
    const invalidVerbs = [
        "manzana",    // Not a verb
        "fear",       // Not a Spanish word
        "sir",        // Not a valid infinitive
        "est@r",      // Contains invalid character
        "es9ar",      // Contains number
        123,          // Not a string
        {},           // Not a string
        "",           // Empty string
        "a",          // One character
        "e"           // One character
    ];
    const invalidMoods = ["future-perfect", "random", 42, "", null];
    const invalidTenses = ["past-perfect", "undefined", {}, null];
    const invalidPronouns = ["we", "they", 123, null, ""];

    console.log("Testing invalid verbs...");
    invalidVerbs.forEach((verb) => {
        testConjugation(verb, "indicative", "present", "yo");
    });

    console.log("Testing invalid moods...");
    validVerbs.forEach((verb) => {
        invalidMoods.forEach((mood) => {
            testConjugation(verb, mood, "present", "yo");
        });
    });

    console.log("Testing invalid tenses...");
    validVerbs.forEach((verb) => {
        validMoods.forEach((mood) => {
            invalidTenses.forEach((tense) => {
                testConjugation(verb, mood, tense, "yo");
            });
        });
    });

    console.log("Testing invalid pronouns...");
    validVerbs.forEach((verb) => {
        validMoods.forEach((mood) => {
            validTenses[mood].forEach((tense) => {
                invalidPronouns.forEach((pronoun) => {
                    testConjugation(verb, mood, tense, pronoun);
                });
            });
        });
    });

    console.log("Testing complete!");
}

//classificationTest();
conjugationTest();

