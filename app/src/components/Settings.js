import React, { useState, useEffect } from 'react';
import ReactJson from 'react-json-view';

function Settings({ session }) {
    const [account, setAccount] = useState('');

    useEffect(() => {
        window.snowStorm.snowColor = '#99ccff'; // blue snow
        window.snowStorm.flakesMaxActive = 20;  // show more snowflakes
        window.snowStorm.useTwinkleEffect = true; // let the snow twinkle
        window.snowStorm.animationInterval = 10; // 30 FPS
        window.snowStorm.stop();
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
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh', fontSize: '20px' }}>
            <h2>Settings</h2>
            console.log(session);
            {session ? <ReactJson src={session} theme="codeschool" /> : <p>Loading session data...</p>}
            <p>Connected MetaMask Account: {account}</p>
            <button onClick={loadWeb3}>
                <img src="/mm_logo.png" alt="MetaMask Logo" style={{ width: '20px', height: '20px' }} />
                Connect MetaMask
            </button>
        </div>
    );
}

export default Settings;