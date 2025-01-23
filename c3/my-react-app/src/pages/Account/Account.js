import React, { useState } from 'react';
import { register, login } from '../../services/api'
import styles from './Account.module.css';

const Welcome = ({ setCurrentStatus }) => {
    return (
            //TODO: add actual welcome message, context, etc
        <div>
            <span> Hi (FILL USERNAME HERE) </span>    
            <Signout setCurrentStatus={setCurrentStatus}/>
        </div>
    )
}

const Signout = ({ setCurrentStatus }) => {
    return (
        <div>
            <button type="button" onClick={ () => {
                setCurrentStatus("Signin");
            }}> Sign out? </button>

        </div>
    )
}

const Signin = ({ setCurrentStatus }) => {
    /* NEWWWW */
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');


    const handleSubmit = async (e) => {
        e.preventDefault(); // Prevent page reload
        // Update the UI or handle login success
        try {
            if (email) { //TODO: better handling
                const data = await login(email, password);
                setCurrentStatus("Welcome"); //TODO: or welcome?
            }
        } catch(error) {
            alert(`Registration failed: ` + (error.response?.data?.message || error.message)); 
        }
    };
    /* NEWWWW */


    return (
        <div className={styles.signinDiv}>
        <h1> Sign in Here! </h1>
        <form className={styles.signinForm} onSubmit={handleSubmit}>
                <input type="email" 
                placeholder="email"
                onChange={(e) => setEmail(e.target.value)}
                /> 
                <input type="password" 
                placeholder="password"
                onChange={(e) => setPassword(e.target.value)}
                />

                <button type="submit" style = {{ width:"200px" }} > Submit </button>

                <div>
                    <span> No account? Register here </span>
                    <button type="button"
                        onClick={ () => {
                            setCurrentStatus("Register");  
                        }}
                        
                    > Register </button>
                </div>
        </form>
        </div>
    )
}

const Register = ({ setCurrentStatus }) => {

    const [email, setEmail] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (password !== confirmPassword) {
            alert("Passwords do not match");
            return;
        }
        try {
            await register(username, email, password);
            setCurrentStatus("Signin"); //TODO: or welcome?
        } catch(error) {
            alert(`Registration failed: ` + (error.response?.data?.message || error.message)); //TODO: lmao?
        }
    }


    return (
        <div className={styles.signinDiv}>
        <h1> Register Here! </h1>
        <form className={styles.signinForm} onSubmit={handleSubmit}>
                <input type="text" 
                 placeholder="username"
                    onChange={(e) => setUsername(e.target.value)}
                /> 
                <input type="email" 
                 placeholder="email"
                    onChange={(e) => setEmail(e.target.value)}
                /> 
                <input type="password" 
                 placeholder="password"
                    onChange={(e) => setPassword(e.target.value)}
                /> 
                <input type="password" 
                 placeholder="confirmPassword"
                    onChange={(e) => setConfirmPassword(e.target.value)}
                /> 
                <button type="submit" style = {{ width:"200px" }} > Submit </button>

                <div>
                    <span> Already have an account? Sign in here </span>
                    <button type="button" onClick={ () => {
                        setCurrentStatus("Signin");
                    }}
                    > Sign in </button>
                </div>
        </form>
        </div>
    )
}

const SigninStatus = new Map([
    ["Signin", Signin],
    ["Register", Register],
    ["Welcome", Welcome],
]);



let signedIn = false;
let defaultStatus; 
if (signedIn) {
    defaultStatus = "Welcome";
} else {
    defaultStatus = "Signin";
}

const Account = () => {
    const [currentStatus, setCurrentStatus] = useState(defaultStatus);
    const ComponentToRender = SigninStatus.get(currentStatus);

    return ComponentToRender ? (
        <ComponentToRender setCurrentStatus={setCurrentStatus}/> 
    ) : (
        <div> Invalid Status </div>
    )
};

export default Account;
