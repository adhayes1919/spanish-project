import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './styles.css'
import { Menu } from './components/';
import { Account, Chat, Exercises, Home } from './pages';
import { E1, E2, E3, E4 } from './pages/Exercises/';

function App() {
    return (
        <Router>
        <Menu />
            <Routes>
                <Route path="/" element= {<Home />} />
                <Route path="/chat" element= {<Chat />} />
                <Route path="/exercises" element= {<Exercises />} />
                <Route path="/account" element = {<Account />} />


                <Route path="/e1" element = {<E1 />} />
                <Route path="/e2" element = {<E2 />} />
                <Route path="/e3" element = {<E3 />} />
                <Route path="/e4" element = {<E4 />} />
            </Routes>
        </Router>
    );
}

export default App;
