import React, { useState, useEffect } from 'react';

function Settings({ session }) {
    const [account, setAccount] = useState('');

    useEffect(() => {
        loadWeb3();
    }, []);

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

    return (
        <div>
            <h2>Settings</h2>
            <p>Supabase Session Data: {JSON.stringify(session)}</p>
            <p>Connected MetaMask Account: {account}</p>
            <button onClick={loadWeb3}>Connect MetaMask</button>
        </div>
    );
}

export default Settings;