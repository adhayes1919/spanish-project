import React from 'react';
//import styles from './Exercises.module.css';
import { BackButton } from '../../'

const Template = ({ exerciseNumber }) => {
    return (
        <div>
            <span> exercise {exerciseNumber} </span>
            <BackButton /> 
        </div>
    )
};

export default Template;
