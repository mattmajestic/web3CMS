import React, { useState, useEffect } from 'react';

function Request() {
    const [form, setForm] = useState({
        username: 'mattmajestic',
        repository: '',
        proposalType: 'feature',
        bid: 25,
    });
    const [repos, setRepos] = useState([]);

    useEffect(() => {
        fetch(`https://api.github.com/users/${form.username}/repos`)
            .then(response => response.json())
            .then(data => setRepos(data))
            .catch(error => console.error(error));
    }, [form.username]);

    const handleChange = (e) => {
        setForm({
            ...form,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        alert('Bid submitted!');
        // Add your form submission logic here
        console.log(form);
    };

    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh', fontSize: '20px', padding: '50px' }}>
            <h2 style={{ marginBottom: '20px' }}>Request Form</h2>
            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '20px', width: '50%' }}>
                <input type="text" name="username" placeholder="GitHub Username" value={form.username} onChange={handleChange} required />
                <select name="repository" value={form.repository} onChange={handleChange} required>
                    {repos.map(repo => (
                        <option key={repo.name} value={repo.name}>{repo.name}</option>
                    ))}
                </select>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '24px', marginBottom: '10px' }}>
                    <label>
                        <input type="radio" name="proposalType" value="feature" checked={form.proposalType === 'feature'} onChange={handleChange} />
                        Feature
                    </label>
                    <label>
                        <input type="radio" name="proposalType" value="bug" checked={form.proposalType === 'bug'} onChange={handleChange} />
                        Bug
                    </label>
                </div>
                <div>
                    <label>
                        Bid Amount: ${form.bid} for Project
                        <input type="range" name="bid" min="25" max="2000" value={form.bid} onChange={handleChange} />
                    </label>
                </div>
                <button type="submit">Submit Bid</button>
            </form>
        </div>
    );
}

export default Request;