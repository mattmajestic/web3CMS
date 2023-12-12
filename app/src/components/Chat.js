import React, { useState, useEffect } from 'react';

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

  const handleClick = async () => {
    const response = await query({ "inputs": input });
    const generated_text = response[0].generated_text.replace(/\\/g, '').split('\n').map((line, index) => <div key={index}>{line}</div>);
    setMessages([...messages, { text: input, position: 'right' }, { text: generated_text, position: 'left' }]);
    setInput('');
  };

  const handleKeyPress = (event) => {
    if(event.key === 'Enter'){
      handleClick();
    }
  }

  useEffect(() => {
    window.snowStorm.stop();
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'flex-start', height: '100vh', padding: '20px' }}>
      <div style={{ display: 'flex', alignItems: 'center', marginBottom: '20px' }}>
        <img src='./codepay.png' alt="Logo" style={{ width: '50px', marginRight: '10px' }} />
        <h2>BizOpti AI Chatbot</h2>
      </div>
      <div style={{ width: '50%', maxHeight: '80vh', overflowY: 'auto', marginBottom: '20px', backgroundColor: 'grey', padding: '20px', borderRadius: '10px' }}>
        {messages.map((message, index) => (
          <div key={index} style={{ textAlign: message.position, fontSize: '24px', margin: '10px 0', color: 'white' }}>
            {message.text}
          </div>
        ))}
      </div>
      <div style={{ width: '50%', display: 'flex', justifyContent: 'space-between' }}>
        <input type="text" value={input} onChange={e => setInput(e.target.value)} onKeyPress={handleKeyPress} style={{ flex: 1, height: '50px', fontSize: '18px', marginRight: '10px' }} />
        <button onClick={handleClick} style={{ height: '70px', fontSize: '24px' }}>Send</button>
      </div>
    </div>
  );
}

export default Chat;