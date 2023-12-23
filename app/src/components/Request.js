import React, { useState, useEffect } from 'react';
import Table from 'react-bootstrap/Table';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import Image from 'react-bootstrap/Image';
import { FaCodeBranch, FaFolderOpen, FaTrash } from 'react-icons/fa';
import axios from 'axios';
import { ToastContainer,toast } from 'react-toastify';
import { supabase } from '../supabaseClient';

const Workspace = ({ session }) => {
    const [workspaces, setWorkspaces] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const [form, setForm] = useState({ username: '', repository: '', branch: '', type: '', bid: 100 });
    const newWorkspace = {
        id: Date.now(),
        name: form.username,
        repository: form.repository,
        branch: form.branch,
        type: form.type,
        bid: form.bid,
        created_at: new Date().toISOString()
    };

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
    
        try {
            const response = await axios.get(`https://api.github.com/repos/${form.username}/${form.repository}`);
            if (response.status === 200) {
                const newWorkspace = {
                    id: Date.now(),
                    name: form.username,
                    repository: form.repository,
                    branch: form.branch,
                    type: form.type,
                    bid: form.bid,
                    created_at: new Date().toISOString(),
                    user: session && session.root ? session.root.email : null
                };
                
                const { data, error } = await supabase
                .from('bid')
                .insert([newWorkspace]);

                toast('GitHub Repository Found... Creating your Bid...');
    
                if (error) {
                    console.error('Error inserting data: ', error);
                } else {
                    setWorkspaces(prevWorkspaces => [...prevWorkspaces, newWorkspace]);
                    setShowModal(false);
                }
            }
        } catch (error) {
            if (error.response && error.response.status === 404) {
                alert('GitHub repository not found');
            } else {
                alert('An error occurred');
            }
        }
    };

    const handleOpen = (workspaceId) => {
        // Handle workspace opening here
    };

    const handleDelete = (workspaceId) => {
        setWorkspaces(workspaces.filter(workspace => workspace.id !== workspaceId));
    };

    useEffect(() => {
        // Fetch active workspaces here and set them to the state
    }, []);

    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center',  height: '100vh' }}>
            <br />
            <Image src="codepay.png" rounded style={{ width: '100px', height: '100px', marginBottom: '10px' }} />
            <h1>CodePay Bids</h1>
            <br />
            <Modal show={showModal} onHide={() => setShowModal(false)}>
            <ToastContainer />
                <Modal.Body>
                    <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                            <input type="text" name="username" placeholder="GitHub Username" value={form.username} onChange={handleChange} required style={{ padding: '10px', fontSize: '16px', flex: 1, marginRight: '10px' }} />
                            <input type="text" name="repository" placeholder="GitHub Repository" value={form.repository} onChange={handleChange} required style={{ padding: '10px', fontSize: '16px', flex: 1 }} />
                        </div>

                        <input type="text" name="branch" placeholder="Branch" value={form.branch} onChange={handleChange} required style={{ padding: '10px', fontSize: '16px' }} />

                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <div style={{ display: 'flex', alignItems: 'center', color: '#17072B' }}>
                                <input type="radio" id="bug" name="type" value="Bug" onChange={handleChange} />
                                <label for="bug">Bug</label>
                                <input type="radio" id="feature" name="type" value="Feature" onChange={handleChange} />
                                <label for="feature">Feature</label>
                            </div>

                            <div style={{ display: 'flex', alignItems: 'center' }}>
                                <span style={{color:'#17072B'}}>$</span>
                                <input type="number" name="bid" placeholder="Bid Amount" min="100" max="1500" step="50" value={form.bid} onChange={handleChange} required style={{ padding: '5px', fontSize: '16px' }} />
                            </div>
                        </div>

                        <Button type="submit" style={{ backgroundColor: '#17072B', color: 'white', fontSize: '20px', padding: '10px 20px' }}>Submit Bid</Button>
                    </form>
                </Modal.Body>
            </Modal>
            <br />
            <Table striped bordered hover style={{ width: '50%' }}>
                <thead>
                    <tr>
                        <th>Bid Name</th>
                        <th>Repository</th>
                        <th>Branch</th>
                        <th>Type</th> {/* Add this line */}
                        <th>Bid</th> {/* Add this line */}
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {workspaces.map((workspace, index) => (
                        <tr key={workspace.id}>
                            <td>{workspace.name}</td>
                            <td>{workspace.repository}</td>
                            <td>{workspace.branch}</td>
                            <td>{workspace.type}</td> {/* Add this line */}
                            <td>{workspace.bid}</td> {/* Add this line */}
                            <td>
                                <Button variant="success" onClick={() => handleOpen(workspace.id)} style={{ marginRight: '10px' }} disabled>
                                    <FaFolderOpen /> Open
                                </Button>
                                <Button variant="danger" onClick={() => handleDelete(workspace.id)} >
                                    <FaTrash /> Delete
                                </Button>
                            </td>
                        </tr>
                    ))}
                    <tr>
                        <td colSpan="6" style={{ textAlign: 'center' }}> {/* Update this line */}
                            <Button onClick={() => setShowModal(true)} disabled={workspaces.length >= 1} style={{ width: '50%', backgroundColor: '#17072B', color: 'white', fontSize: '20px', padding: '10px 20px', border: '2px solid white' }}>
                                <FaCodeBranch /> Create Bid
                            </Button>
                        </td>
                    </tr>
                </tbody>
            </Table>
            <div style={{ marginTop: '20px', fontSize: '18px', color: 'white' }}>
                Note: Free accounts are limited to 3 projects. Please visit <a href="/pricing">our pricing page</a> to view premium options with up to unlimited projects.
            </div>
        </div>
    );
};

export default Workspace;