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
                <div style={{ position: 'fixed', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', width: '100%', height: '100%', backgroundColor: 'grey', overflow: 'auto' }}>
                    <strong>User:</strong>
                    <ReactJson src={data.user} theme="monokai" style={{ fontSize: '22px' }} />
                </div>
            );
        }
        return '';
    }

    return (
        <div style={{ position: 'fixed', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '50vh', width: '50%', fontSize: '20px' }}>
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