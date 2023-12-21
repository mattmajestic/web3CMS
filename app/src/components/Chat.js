import React, { useState, useEffect } from 'react';
import { FaPaperclip } from 'react-icons/fa';
import { supabase } from '../supabaseClient';
import { v4 as uuidv4 } from 'uuid';

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
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'flex-start', height: '100vh', padding: '20px' }}>
      <div style={{ display: 'flex', alignItems: 'center', marginBottom: '20px' }}>
        <img src='./codepay.png' alt="Logo" style={{ width: '100px', height: '100px', borderRadius: '50%', marginRight: '10px', animation: 'fadein 2s' }} />
        <h2>CodePay Chat</h2>
        </div>
        <div style={{ width: '50%', maxHeight: '80vh', overflowY: 'auto', marginBottom: '20px', backgroundColor: 'grey', padding: '20px', borderRadius: '10px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', color: 'white', marginBottom: '10px',fontSize: '24px' }}>
            <div>AI</div>
            <div>User</div>
          </div>
          {messages.map((message, index) => (
            <div key={index} style={{ textAlign: message.position, fontSize: '24px', margin: '10px 0', color: message.position === 'right' ? 'white' : '#17072B', backgroundColor: message.position === 'right' ? '#17072B' : '#D3D3D3', padding: '10px', borderRadius: '10px' }}>
              {message.text}
              <div style={{ fontSize: '12px', textAlign: 'right' }}>{message.timestamp}</div>
            </div>
          ))}
          {isTyping && <div style={{ color: '#17072B', fontSize: '24px', textAlign: 'right' }}>Typing...</div>}
        </div>
        <div style={{ width: '50%', display: 'flex', alignItems: 'center' }}>
          <label htmlFor="file-upload" style={{ cursor: 'pointer', marginRight: '10px' }}>
            <FaPaperclip size={30} />
          </label>
          <input id="file-upload" type="file" accept=".csv,audio/*" onChange={handleFileUpload} style={{ display: 'none' }} />
          <input type="text" value={input} onChange={e => setInput(e.target.value)} onKeyPress={handleKeyPress} style={{ flex: 1, height: '50px', fontSize: '18px', marginRight: '10px' }} />
          <button onClick={handleClick} style={{ height: '70px', fontSize: '24px' }}>Send</button>
        </div>
        </div>
        );
        }

export default Chat;