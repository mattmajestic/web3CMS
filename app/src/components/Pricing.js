import React from 'react';

const Pricing = () => {
    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh' }}>
            <h1 style={{ fontSize: '48px' }}>Pricing</h1>
            <div style={{ display: 'flex', justifyContent: 'space-around', width: '80%', marginTop: '50px' }}>
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '40px', border: '1px solid black', borderRadius: '10px' }}>
                    <h2 style={{ fontSize: '36px' }}>Free</h2>
                    <p style={{ fontSize: '24px' }}>1 Workspace</p>
                    <p style={{ fontSize: '24px' }}>Standard Docker Image</p>
                    <p style={{ fontSize: '24px' }}>1 CPU</p>
                    <p style={{ fontSize: '24px' }}>2 GB RAM</p>
                    <p style={{ fontSize: '24px' }}>10 GB Storage</p>
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '40px', border: '1px solid black', borderRadius: '10px' }}>
                    <h2 style={{ fontSize: '36px' }}>Premium</h2>
                    <p style={{ fontSize: '24px' }}>5 Workspaces</p>
                    <p style={{ fontSize: '24px' }}>Standard Docker Image</p>
                    <p style={{ fontSize: '24px' }}>2 CPUs</p>
                    <p style={{ fontSize: '24px' }}>4 GB RAM</p>
                    <p style={{ fontSize: '24px' }}>20 GB Storage</p>
                </div>
            </div>
        </div>
    );
};

export default Pricing;