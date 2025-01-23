//TODO: headers and also import vs require?
import React, { useState } from 'react';
import axios from 'axios';
import styles from './Home.module.css';

const franc = require('franc');
const whitelist = ['eng', 'spa'];

// add a submit button too but sue me


const Translate = () => {

    const [inputText, setInputText] = useState('');
    const [translatedText, setTranslatedText] = useState('aqui');
    const [inputLanguage, setInputLanguage] = useState('auto');
    const [languageButton, setLanguageButton] = useState('Set Automatically');

    //TODO: >>
    const accentMap = {
        a: "á",
        e: "é",
        i: "í",
        o: "ó",
        n: "ñ",
    };    

    const handleKeyDown = async (event) => {
        const key = event.key.toLowerCase();

        //submit, probably should go into another function?
        if (key == "enter"  && !event.shiftKey) {
            event.preventDefault();
            await handleTranslate();
            setInputText('');
            event.target.value=''; // TODO: I don't think this is a perfect system
        }
    }; 

    const handleKeyUp = (event) => { 
        const key = event.key.toLowerCase();
    };

    const handleChange = (event) => {
        // Allow the user to type normally for keys outside the accent map
        setInputText(event.target.value);
    };
    const handleTranslate = async () => {
        try { 
            console.log(`preparing to send with: ${inputLanguage}`)
            const response = await axios.post('/translate', {
                bodyText: inputText,
                sourceLanguage: inputLanguage
            } 
            );
            setTranslatedText(response.data.translation);
        }
        catch (error) {
            console.error("Error translating text:", error);
        }
    }

    const toggleLanguage = () => {
        console.log(`Before toggle: inputLanguage = ${inputLanguage}`);

        setInputLanguage((prevLang) => {
            const nextLang = prevLang === "en" ? "es" :
                             prevLang === "es" ? "auto" : 
                             "en";

            setLanguageButton(
                nextLang === "en" ? "English to Spanish" :
                nextLang === "es" ? "Spanish to English" :
                "Set Automatically"
            );

            console.log(`After toggle: inputLanguage = ${nextLang}`);
            return nextLang;
        });
    };


    return (
        <div> 
        <button 
            onClick={toggleLanguage}> 
                {languageButton}
        </button>
        <textarea 
            className={styles.textBox}
            placeholder="Translate here:"  
            onKeyDown={handleKeyDown}
            onKeyUp={handleKeyUp}
            onChange={handleChange}
            value={inputText}
            >
        </textarea>

        <h1> Translation: </h1>
        <p> {translatedText} </p>
        </div>
    );
}

const AboutSection = () => {
    const [isExpanded, setIsExpanded] = useState(false);
    
    const toggleSection = () => {
        setIsExpanded((prev) => !prev);
    };

    return ( 
        <div className={styles.mainDiv}>
        <button className={styles.aboutButton} onClick={toggleSection} >
        {isExpanded ? "Close About Section" : "Open About Section"}             </button>
        
        {isExpanded && (
            <div className={styles.aboutExpanded}>
            <h2> About: </h2>
            <ul> 
                <li> I wanted to create an app that helps me both learn reactjs and help me learn spanish </li>
                <li> I make no claim to revolutionize learning </li>
                <li> I make no claim about pretty much anything </li>
                <li> Instead, I wanted to make an app specifically catering towards my own style of learning </li>
                <li> Here, I found a few things that I wanted to focus on 
                    <ol> 
                        <li> First: integration with a flashcard app. I personally use anki a lot but wanted something that would automate my process for me  </li>
                        <li> Second: progress tracking. I have a personal goal to get to at least a B2 in spanish and possibly at least C1. I wanted some way to measure this and gauge how close i was. I find this sort of studying motivating. </li>

                        <li> Third: I wanted to focus on spoken spanish rather than just vocab </li>
                    </ol>    
                </li>
                <li> Similarly, I was simultaneously working on learning react and chose this project to be my pet project for a while. With it, I have a number of side projects that may accompany it:
                    <ol>
                        <li> At the top I'm sure you notice an "exercises" tab. Here I want to create a series of comprehension based tests to structure my learning. For example, simply "translate this sentence" with feedback, which can help me identify words I'm missing. "choose the best response" and "fill in the blank" to gauge comprehension and learn vocab through context clues etc. </li>
                        <li> Similarly, a lofty goal involves the fun little "chat" tab you may notice alongside it. Here, I hope to create a AI based chatbot that can practice answer and responses. This sort've thing absolutely exists and I make no claim that its revolutionary. This is where the project begins stepping further into the "learning CS" category as I wanted to train it myself. </li>
                        <li> Train it yourself? Yup! As I said, theres a number of subprojects running around on this site and one involves my own AI. I plan to scrape spanish speaking subreddits with my own bot to create my own corpus which will hopefully (in theory) become the basis of all the exercises mentioned above. </li>
                        <li> Finally, I plan to integrate learning sql into my project by having databases for both login info (see "account") as well as for the exercises/missed words etc. This will also be how I gauge progress (which I will hopefully do by creating my own judgement system I can then roughly map to a CEFR scale) </li>
                    </ol>
                </li>
            </ul>
        </div>
    )}
    </div>
    );
}

const Home = () => {
    return (
        <div>
            <h1> Hi! </h1>
            <Translate />
            <AboutSection />
        </div>
    );
};

export default Home;

