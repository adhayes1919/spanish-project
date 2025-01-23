import styles from './Menu.module.css';
import React from 'react';
import { Link } from 'react-router-dom';

const Menu = () => {
    return (
        <nav className={styles.nav}> 
            <ul>
                <li><Link to="/">Home</Link></li>
                <li><Link to="/exercises">Exercises</Link></li>
                <li><Link to="/chat">Chat</Link></li>
                <li><Link to="/account">Account</Link></li>
            </ul>
        </nav>
    );
};

export default Menu;
