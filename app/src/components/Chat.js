import React, { useState, useEffect } from 'react';
import { FaPaperclip } from 'react-icons/fa';

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

function Chat() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);

  const handleClick = async () => {
    setIsTyping(true);
    const response = await query({ "inputs": input });
    const generated_text = response[0].generated_text.replace(/\\/g, '').split('\n').map((line, index) => <div key={index}>{line}</div>);
    setMessages([...messages, { text: input, position: 'right' }, { text: generated_text, position: 'left' }]);
    setInput('');
    setIsTyping(false);
  };

  const handleKeyPress = (event) => {
    if(event.key === 'Enter'){
      handleClick();
    }
  }

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    console.log(file);
    // Here you can handle the uploaded file (e.g., send it to a server)
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