import React, { useState, useEffect } from 'react';
import ReactJson from 'react-json-view';

function Settings({ session }) {
    const [account, setAccount] = useState('');

    async function loadWeb3() {
        if (window.ethereum) {
            await window.ethereum.request({ method: 'eth_requestAccounts' });
            loadBlockchainData();
        }
        else {
            window.alert('Non-Ethereum browser detected. You should consider trying MetaMask!');
        }
    }

    async function loadBlockchainData() {
        const accounts = await window.ethereum.request({ method: 'eth_accounts' });
        setAccount(accounts[0]);
    }

    function DisplayObjectProperties({ data }) {
        const keysToShow = ['expires_at', 'refresh_token', 'token_type', 'user'];
        return data ? keysToShow.map((key, index) => {
            if (data[key]) {
                const formattedKey = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                const value = typeof data[key] === 'object' ? JSON.stringify(data[key]) : data[key];
                return (
                    <div key={index}>
                        <strong>{formattedKey}:</strong> {value}
                    </div>
                );
            }
            return null;
        }) : '';
    }

    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh', fontSize: '20px' }}>
            <h2>Settings</h2>
            <div>
                <h3>Supabase Session Data:</h3>
                <p>{DisplayObjectProperties({ session })}</p>
            </div>
            <p>Connected MetaMask Account: {account}</p>
            <button onClick={loadWeb3}>
                <img src="/mm_logo.png" alt="MetaMask Logo" style={{ width: '20px', height: '20px' }} />
                Connect MetaMask
            </button>
        </div>
    );
}

export default Settings;