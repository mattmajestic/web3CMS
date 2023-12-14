import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

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
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh', fontSize: '24px', padding: '50px' }}>
            <h2 style={{ marginBottom: '40px', fontSize: '36px' }}>Bid on Branch</h2>
            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '30px', width: '60%', fontSize: '20px' }}>
                <input type="text" name="username" placeholder="GitHub Username" value={form.username} onChange={handleChange} required style={{ padding: '10px', fontSize: '20px' }} />
                <select name="repository" value={form.repository} onChange={handleChange} required style={{ padding: '10px', fontSize: '20px' }}>
                    {repos.map(repo => (
                        <option key={repo.name} value={repo.name}>{repo.name}</option>
                    ))}
                </select>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '24px', marginBottom: '20px' }}>
                    <div>
                        <label>
                            <input type="radio" name="proposalType" value="feature" checked={form.proposalType === 'feature'} onChange={handleChange} />
                            Feature
                        </label>
                        <label style={{ marginLeft: '10px' }}>
                            <input type="radio" name="proposalType" value="bug" checked={form.proposalType === 'bug'} onChange={handleChange} />
                            Bug
                        </label>
                    </div>
                    <div>
                        <label>
                            Bid Amount: $
                            <input type="number" name="bid" min="50" max="1500" step="50" value={form.bid} onChange={handleChange} />
                        </label>
                    </div>
                </div>
                <p>We do not authorize any one branch of over $1500.</p>
                <div style={{ display: 'flex', alignItems: 'center', marginBottom: '20px' }}>
                    <input type="checkbox" id="terms" name="terms" value={form.terms} onChange={handleChange} required />
                    <label htmlFor="terms" style={{ marginLeft: '10px' }}>
                        I agree to the <Link to="/terms" style={{ color: '#D8BFD8' }}>Terms and Conditions</Link>
                    </label>
                </div>
                <button type="submit" style={{ 
                    padding: '20px', 
                    fontSize: '24px', 
                    width: '30%', 
                    backgroundColor: '#D8BFD8', 
                    color: 'black', 
                    margin: '0 auto', 
                    display: 'block' 
                }}>Submit Bid</button>
            </form>
        </div>
    );
}

export default Request;