import React, { useState, useRef, useEffect } from 'react';
import styles from './Chat.module.css';

const Chat = () => {
    const [inputValue, setInputValue] = useState("");
    const [messages, setMessages] = useState([]);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        if (messagesEndRef.current) {
            messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
        }
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);
    
    const handleSendButton = () => {
        if (inputValue.trim()) {
            setMessages([...messages, inputValue]);
            setInputValue("");
        }
    }

    const handleKeyPress = (event) => {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            if (inputValue.trim()) {
                setMessages([...messages, inputValue]);
                setInputValue("");
            }
        }
    };
    let isLeft = false;
    return (
        <div className={styles.messagesContainer}>

            <div className={styles.chatMessages}>
                {messages.map((message, index) => (
                    <div 
                        key={index} 
className={`${styles.chatBubble} ${isLeft ? styles.left : ''}`}
>
                            {message}
                    </div>
                ))}
                <div ref={messagesEndRef}></div>
            </div>

            <div className={styles.inputContainer}>
            <textarea 
                className={styles.chatBox} 
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={handleKeyPress}
                placeholder= "Type to start chatting" 
                
                >  </textarea>

            <button 
                className={styles.sendButton}
                onClick={handleSendButton}
            > Send
            </button>

            </div>
        </div>
    );
};

export default Chat;
