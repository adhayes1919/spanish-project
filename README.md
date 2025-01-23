
# Interactive Spanish Language Learning Platform

## Overview
This project is an interactive language-learning site built from scratch using **React and Express**, designed to provide an engaging experience for learning Spanish. It offers various exercises, translation tools, and a chatbot for conversational practice. The backend tracks user progress, identifies common errors, and dynamically adjusts lessons to improve learning outcomes.

This project serves as a **personal learning playground**, where most components have been manually implemented to deepen understanding of full-stack web development. It integrates **LibreTranslate** for real-time translations and **MySQL** for user authentication and data storage. Though it is still a work in progress, the foundation has been laid for future improvements.

## Features
### Web Interface
- **Translation and Conjugation Tools:** Users can access a translation feature powered by **LibreTranslate**, as well as verb conjugation exercises designed for self-guided learning.
- **Graded Exercises:** Users can practice structured exercises, including fill-in-the-blank, sentence translations, and comprehension-based questions.
- **User Progress Tracking:** The backend stores user data, tracks commonly missed words, and adjusts future exercises based on personal performance.

### Machine Learning Component
- **Corpus-Based AI Model:** A machine learning model was developed using millions of scraped Spanish sentences from **Reddit**, processed into a structured dataset.
- **Bash Preprocessing:** Due to **GPU limitations**, data preprocessing was handled using **Bash scripts** instead of Python to maximize efficiency.
- **Transformer Model Development:** The beginnings of a **transformer-based model** were implemented, with the goal of predicting missing words in exercises and simulating interactive chatbot conversations.
- **Current Roadblock:** Model training was halted due to computational constraints, as training transformers locally without access to high-performance GPUs proved impractical.

## Project Structure
As of now, the project is maintained remotely due to my studies in **Costa Rica**, leading to a somewhat messy file structure:
- **Top-Level Directory:** Contains one main folder, `c3`.
- **`c3/my-react-app/`** - The **JavaScript-based front-end**, built with **React**.
- **`c3/corpus/`** - The **Python-based backend**, handling NLP processes and data management.
- **`corpus2.ipynb`** - The current version of the machine learning model, representing the latest iteration of the transformer-based approach.

## Future Work
### **1. Enhancing the Web Application**
- Improve **UI/UX** to make the interface more user-friendly.
- Expand **translation functionalities**, allowing real-time sentence breakdown and grammar analysis.
- Implement **more complex exercises**, including contextual sentence completion and listening comprehension.

### **2. Advancing the Machine Learning Model**
- **Refine corpus preprocessing**, ensuring cleaner sentence segmentation and tokenization.
- Secure access to **GPU computing resources**, either via cloud providers or institutional research clusters, to continue model training.
- Improve **word prediction accuracy**, enabling adaptive sentence completion exercises.
- Implement **chatbot interactivity**, allowing learners to engage in AI-powered Spanish conversations.

### **3. Backend and Data Optimization**
- Optimize **MySQL database structure** for improved query efficiency.
- Develop an **API for external integrations**, allowing external applications to leverage the translation and conjugation functionalities.
- Store **user engagement metrics**, creating data-driven improvements for lesson personalization.

## Conclusion
This project represents a **self-driven learning initiative**, integrating full-stack web development, machine learning, and NLP techniques. While significant progress has been made, it remains an ongoing development effort with numerous opportunities for refinement and expansion. Future work will focus on addressing computational limitations, improving AI-based exercises, and making the system more robust and scalable.
