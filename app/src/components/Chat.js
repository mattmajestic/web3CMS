import React, { useState, useEffect } from 'react';
import { FaPaperclip } from 'react-icons/fa';
import { supabase } from '../supabaseClient';
import { v4 as uuidv4 } from 'uuid';
import '../Chat.css';

const API_URL = "https://api-inference.huggingface.co/models/gpt2";
const headers = { "Authorization": "Bearer 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" };

async function query(payload) {
  const response = await fetch(API_URL, {
    headers: headers,
    method: "POST",
    body: JSON.stringify(payload),
  });
  const result = await response.json();
  return result;
}

function Chat({ session }) {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);

  const generateId = () => {
    return uuidv4();
  };

  const handleClick = async () => {
    if (input.trim() !== '') {
      setIsTyping(true);

      const userId = generateId();
      const newMessage = {
        text: input,
        created_at: new Date().toISOString(),
        user_id: userId,
      };

      // Save the user's message in the Supabase database
      const { error } = await supabase
        .from('chat')
        .insert([newMessage]);

      if (error) {
        console.error('Error saving message:', error);
      }

      // Generate the chatbot's response
      const response = await query({ "inputs": input });
      const generated_text = response[0].generated_text.replace(/\\/g, '').split('\n').map((line, index) => <div key={index}>{line}</div>);

      // Add the user's message and the chatbot's response to the messages state
      setMessages(prevMessages => [...prevMessages, { text: input, position: 'right' }, { text: generated_text, position: 'left' }]);

      // Clear the input
      setInput('');

      setIsTyping(false);
    }
  };

  const handleKeyPress = (event) => {
    if(event.key === 'Enter'){
      handleClick();
    }
  }

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    console.log(file);

    const fileExtension = file.name.split('.').pop();
    const fileName = `${generateId()}.${fileExtension}`;

    const { data, error } = await supabase
      .storage
      .from('codepay')
      .upload(fileName, file, {
        cacheControl: '3600',
        upsert: false
      });

    if (error) {
      console.error('Error uploading file:', error);
    } else {
      console.log('File uploaded successfully');
    }
  };

  useEffect(() => {
    if (input.length > 0) {
      setIsTyping(true);
    } else {
      setIsTyping(false);
    }
  }, [input]);

  return (
    <div className="chat-container">
      <div className="chat-header">
        <img src='./codepay.png' alt="Logo" className="chat-logo" />
        <h1>CodePay Chat</h1>
      </div>
      <div className="chat-messages">
      <div className="chat-labels">
          <div><span role="img" aria-label="robot">🤖</span> AI</div>
          <div><span role="img" aria-label="user">👤</span> User</div>
      </div>
        {messages.map((message, index) => (
          <div key={index} className={`chat-message ${message.position}`}>
            {message.text}
            <div className="chat-timestamp">{message.timestamp}</div>
          </div>
        ))}
        {isTyping && <div className="typing-indicator">Typing...</div>}
      </div>
      <div className="chat-inputs">
        <label htmlFor="file-upload" className="file-upload-label">
          <FaPaperclip size={30} />
        </label>
        <input id="file-upload" type="file" accept=".csv,audio/*" onChange={handleFileUpload} className="file-upload-input" />
        <input type="text" value={input} onChange={e => setInput(e.target.value)} onKeyPress={handleKeyPress} className="chat-text-input" />
        <button onClick={handleClick} className="send-button">Send</button>
      </div>
    </div>
  );
        }

export default Chat;