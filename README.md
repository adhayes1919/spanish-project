# Interactive Spanish Learning Platform

This project is designed as my learning playground for web dev and machine learning. It encompasses two smaller projects. Due to currently being away studying ecology in Costa Rica, this repository is quite messy but will be cleaned up and devloped further in the future. Just about everything present here was learned for this project specifically. 

An interactive language-learning site built from scratch using React and Express. Designed to provide engaging Spanish-learning exercises, translation tools, and a chatbot for practice. The backend tracks user progress, stores common errors, and dynamically adjusts lessons. 

## /my-react-app 
- web dev component 

## /corpus 
- machine learning component 

## 🚀 Features

### Frontend (React.js)
- **Home Tab:** Displays project information and provides a translation field powered by LibreTranslate. Auto-detects English/Spanish but allows manual selection.
- **Exercises Tab:** Planned to contain dynamic exercises such as sentence completion and fill-in-the-blank activities.
- **Chat Tab:** Will include an AI-powered chatbot for conversational Spanish practice.
- **Settings Tab:** Placeholder for user preferences, account settings, and progress tracking.


### Backend (Express.js + MySQL)
- **User Authentication:** Stores user login information securely.
- **Adaptive Learning System:** Plans to track common errors, frequently missed words, and provide personalized exercises.
- **Irregular Verb Database:** Will store verb conjugations to enhance learning tools.
- **API Calls:** Backend endpoints to support translation, exercise generation, and chatbot interactions.

### Machine Learning & Corpus Development
- **Reddit-Based Spanish Corpus:** Scraped millions of Spanish sentences from Reddit to create a large dataset for training language models.
- **Data Processing:** Cleaned and tokenized sentences, filtering out non-Spanish content.
- **Transformer Model:** In development for predicting missing words in sentences (currently limited by GPU constraints).

## 🛠️ Installation

### Prerequisites
- Node.js
- MySQL
- Python (for NLP preprocessing)

### Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/spanish-learning-app.git
   cd spanish-learning-app
   ```
2. **Install dependencies:**
   ```bash
   npm install
   cd backend && npm install
   ```
3. **Start the development servers:**
   ```bash
   cd frontend && npm start
   cd backend && node server.js
   ```
4. **Set up MySQL Database:**
   ```sql
   CREATE DATABASE spanish_learning;
   ```
   Run the database schema provided in `/backend/database/schema.sql`.

## 📅 Future Plans
- **Expand Dataset:** Scrape more Spanish-language sources beyond Reddit.
- **Improve Chatbot:** Enhance interactivity and accuracy of responses.
- **Advanced User Tracking:** Store user progress, common mistakes, and learning patterns.
- **Gamification:** Implement badges, achievements, and leaderboards.
- **Browser Extension:** Enable users to highlight words on any webpage and add them to their study bank.
- **Offline Mode:** Support downloadable lessons and exercises.
- **Cloud-Based AI Training:** Seek resources for model training on a more powerful GPU.

## 🙌 Acknowledgments
- LibreTranslate for open-source translation support.
- Reddit communities for providing a vast corpus of Spanish text.
- Various online resources for helping with web scraping and NLP techniques.

---
This project is a work in progress and serves as both a learning experience and a practical tool for language acquisition. Contributions and feedback are welcome!
