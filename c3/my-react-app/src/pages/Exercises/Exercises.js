import React from 'react';
import { Link } from 'react-router-dom';
import styles from './Exercises.module.css';

const ExerciseCard = ({ name }) => {
    let exercisePath = `/${name}`;
    return (
            <div className={styles.card}> 
                <Link to={exercisePath} className={styles.cardLink}> 
                    {`Exercise ${name}`}
                </Link>
            </div>
    )
}

const Exercises = () => {

    return (
        <div className={styles.grid}>
            <ExerciseCard name="e1"/>
            <ExerciseCard name="e2"/>
            <ExerciseCard name="e3"/>
            <ExerciseCard name="e4"/>
        </div>
    );
};

export default Exercises;
