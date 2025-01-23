const express = require('express');
const bodyParser = require('body-parser');
const bcrypt = require('bcrypt');
const mysql = require('mysql2');
const cors = require('cors');
const axios = require('axios');
//const deepl = require('deepl-node');

require('dotenv').config();


const app = express();
//app.set('trust proxy', true);
const PORT = 3001;

app.use(cors({origin: 'http://localhost:3000'}));
app.use(bodyParser.json());


/*********rate limit stolen from gpt**********/
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // Limit each IP to 100 requests per windowMs
    message: 'Too many requests, please try again later.',
});

app.use(limiter);
/*******************/

const db = mysql.createConnection({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME,
});

db.connect((err) => {
    if (err) {
        console.error('Error connecting to MySQL: ', err);
        return;
    }
    console.log('Connected to MySQL database.');
});

app.post('/register', async (req, res) => {
    const { username, email, password } = req.body;
    const hashedPassword = await bcrypt.hash(password, 10);
    
    const query = 'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)';

    db.query(query, [username, email, hashedPassword], (err, results) => {
        if (err) {
            if (err.code === 'ER_DUP_ENTRY') {
                return res.status(400).json({ message: "Username or email already in use. Please try again" });
            } else {
                return res.status(500).json({ message: "Generic database error.", error: err });
            }
        }
        res.status(201).json({ message: "User registered successfully!" });
    });
});

app.post('/login', async (req, res) => {
    const { email, password } = req.body;
    const query = 'SELECT * FROM users WHERE email = ?'
    db.query(query, [email], async (err, results) => {
        if (err) {
            return res.status(500).json({ message: "Database error signing in.", error: err });
        }
        if (results.length === 0) {
            return res.status(401).json({ message: "User not found" });
        }

        const user = results[0];
        try {
            const isValidPassword = await bcrypt.compare(password, user.password_hash);
            if (!isValidPassword) {
                return res.status(401).json({ message: "Invalid password" });
            }
            res.status(200).json({ 
                message: "Login successful!", 
                user: {
                    id: user.id,
                    username: user.username,
                    email: user.email 
                }
            });
        } catch (compareErr) {
            return res.status(500).json({ message: "Error verifying password.", error: compareErr });
        }
    });
});

/*
// somehow no english -> spanish 
const translator = new deepl.Translator(authKey);
const authKey = process.env.DEEPL_KEY;

const response = await translator.translateText(bodyText, 'en', targetLang);
*/

app.post('/translate', async(req, res) => {
    const { bodyText, sourceLanguage } = req.body;
    //console.log(`text: ${bodyText}`);
    //boolean toggle might be cleaner?     
    console.log(`input: ${sourceLanguage}`);
    let targetLanguage;
    if (sourceLanguage === "auto") {
        try {
            const language = await axios.post(
                "http://localhost:5000/detect", 
            {
                q: bodyText,
            },
            {headers:
                { "Content-Type": "application/json" }
            });

            const autoLanguage = language.data[0].language;

            if (autoLanguage === "en") {
                targetLanguage = "es";
            } else if (autoLanguage === "es") {
                targetLanguage = "en";
            }
        } catch (error) {
            //TODO: LMFAO 
            console.log("I still don't care");
        }
    } else{
        //TODO: this gotta be horrendous 
        if (sourceLanguage === "en") {
            targetLanguage = "es";
        } else if (sourceLanguage === "es") {
            targetLanguage = "en";
        }
    }

    console.log(`target: ${targetLanguage}`);

    if (targetLanguage) {
        try {
            const response = await axios.post(
                "http://localhost:5000/translate", 
            {
                q: bodyText,
                source: sourceLanguage,
                target: targetLanguage,
                format: "text",
                alternatives: "1",
                api_key: ""
            },
            {headers:
                { "Content-Type": "application/json" }
            });

            console.log(response.data.translatedText);
            res.json({ translation: response.data.translatedText });
        }
        catch(error) {
            console.log(":(");
            //console.error("Translation error:", error);
            res.status(500).json({ error: "failed to translate text" });
        }
    }
});

app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});


