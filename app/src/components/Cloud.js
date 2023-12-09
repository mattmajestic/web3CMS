import React, { useState } from 'react';

function Cloud() {
    const [selectedOptions, setSelectedOptions] = useState({
        Azure: { Docker: false, Kubernetes: false },
        Google: { Docker: false, Kubernetes: false },
        AWS: { Docker: false, Kubernetes: false },
    });

    const handleCheckboxChange = (cloud, option) => {
        setSelectedOptions(prevState => ({
            ...prevState,
            [cloud]: { ...prevState[cloud], [option]: !prevState[cloud][option] }
        }));
    };

    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh', fontSize: '20px' }}>
            <h2>Cloud Deployment Options</h2>
            {['Azure', 'Google', 'AWS'].map(cloud => (
                <div key={cloud} style={{ margin: '20px', border: '1px solid black', padding: '20px' }}>
                    <h3>{cloud}</h3>
                    {['Docker', 'Kubernetes'].map(option => (
                        <div key={option}>
                            <label>
                                <input type="checkbox" checked={selectedOptions[cloud][option]} onChange={() => handleCheckboxChange(cloud, option)} />
                                {option}
                            </label>
                        </div>
                    ))}
                </div>
            ))}
        </div>
    );
}

export default Cloud;