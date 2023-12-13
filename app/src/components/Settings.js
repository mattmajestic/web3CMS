import React, { useState, useEffect } from 'react';
import ReactJson from 'react-json-view';

function Settings({ session }) {
    const [account, setAccount] = useState('');

    useEffect(() => {
        if (window.ethereum) {
            loadWeb3();
        } else {
            alert('Ethereum object not found. You should consider trying MetaMask!');
        }
    }, []);

    async function loadWeb3() {
        window.ethereum.request({ method: 'eth_requestAccounts' });
        loadBlockchainData();
    }

    async function loadBlockchainData() {
        const accounts = await window.ethereum.request({ method: 'eth_accounts' });
        setAccount(accounts[0]);
    }

    let sessionObject;
    try {
        sessionObject = JSON.parse(JSON.stringify(session));
    } catch (error) {
        console.error('Failed to convert session to a JSON object:', error);
    }

    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh', fontSize: '20px' }}>
            <h2>Settings</h2>
            <p>Supabase Session Data:</p>
            <ReactJson src={sessionObject || {}} theme="chalk" />
            <p>Connected MetaMask Account: {account}</p>
            <button onClick={loadWeb3}>
                <img src="/mm_logo.png" alt="MetaMask Logo" style={{ width: '20px', height: '20px' }} />
                Connect MetaMask
            </button>
        </div>
    );
}

export default Settings;