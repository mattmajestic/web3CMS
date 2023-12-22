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
        if (data && data.user) {
            return (
                <div style={{ position: 'fixed', top: '0', left: '0', width: '50%', height: '50%', backgroundColor: 'grey', overflow: 'auto' }}>
                    <strong>User:</strong>
                    <ReactJson src={data.user} />
                </div>
            );
        }
        return '';
    }

    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh', fontSize: '20px' }}>
            <h2>Settings</h2>
            <div>
                <h3>Supabase Session Data:</h3>
                <p>{DisplayObjectProperties({ data: session })}</p>
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