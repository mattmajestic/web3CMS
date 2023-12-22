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

    function DisplayObjectProperties({ data, indentLevel = 0 }) {
        return (
            <div style={{ paddingLeft: `${indentLevel * 20}px` }}>
                {Object.entries(data).map(([key, value], index) => {
                    if (typeof value === 'object' && value !== null) {
                        return (
                            <div key={index}>
                                <strong>{key}:</strong>
                                <DisplayObjectProperties data={value} indentLevel={indentLevel + 1} />
                            </div>
                        );
                    } else {
                        return (
                            <div key={index}>
                                <strong>{key}:</strong> {JSON.stringify(value)}
                            </div>
                        );
                    }
                })}
            </div>
        );
    }

    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh', fontSize: '20px' }}>
            <h2>Settings</h2>
            <div>
                <h3>Supabase Session Data:</h3>
                <DisplayObjectProperties data={session} />
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