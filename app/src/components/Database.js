import React, { useState, useEffect } from 'react';
import Table from 'react-bootstrap/Table';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import Image from 'react-bootstrap/Image';
import { FaCodeBranch, FaFolderOpen, FaTrash } from 'react-icons/fa';

const Database = () => {
    const [form, setForm] = useState({ username: '', repository: '', branch: '' });
    const [workspaces, setWorkspaces] = useState([]);
    const [showModal, setShowModal] = useState(false);

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        const newWorkspace = {
            id: Date.now(),
            name: form.name,
            database: form.database,
        };
        setWorkspaces(prevWorkspaces => [...prevWorkspaces, newWorkspace]);
        setShowModal(false);
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
            <h1>CodePay Databases</h1>
            <br />
            <Modal show={showModal} onHide={() => setShowModal(false)}>
                <Modal.Header closeButton>
                    <Modal.Title>Create Database</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', color: '#800080' }}>
                            <h1 style={{ fontSize: '2em', marginBottom: '20px' }}>Select Type of Database</h1>
                            <label style={{ fontSize: '1.2em' }}>
                                <input type="radio" name="database" value="Redis" onChange={handleChange} required />
                                Redis
                            </label>
                            <label style={{ fontSize: '1.2em' }}>
                                <input type="radio" name="database" value="MySQL" onChange={handleChange} required />
                                MySQL
                            </label>
                            <label style={{ fontSize: '1.2em' }}>
                                <input type="radio" name="database" value="MongoDB" onChange={handleChange} required />
                                MongoDB
                            </label>
                            <label style={{ fontSize: '1.2em' }}>
                                <input type="radio" name="database" value="Supabase" onChange={handleChange} required />
                                Supabase
                            </label>
                        </div>
                        <input type="text" name="name" placeholder="Name of Databases" value={form.name} onChange={handleChange} required style={{ padding: '10px', fontSize: '16px', width: '60%', margin: '0 auto' }} />
                        <Button type="submit" style={{ backgroundColor: '#17072B', color: 'white', fontSize: '20px', padding: '10px 20px', width: '50%', margin: '0 auto' }}>Create Database</Button>
                    </form>
                </Modal.Body>
            </Modal>
            <br />
            <Table striped bordered hover style={{ width: '50%' }}>
                <thead>
                    <tr>
                        <th>Database Name</th>
                        <th>Type</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {workspaces.map((workspace, index) => (
                        <tr key={workspace.id}>
                            <td>{workspace.name}</td>
                            <td>{workspace.database}</td>
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
                        <td colSpan="4" style={{ textAlign: 'center' }}>
                            <Button onClick={() => setShowModal(true)} disabled={workspaces.length >= 1} style={{ width: '50%', backgroundColor: '#17072B', color: 'white', fontSize: '20px', padding: '10px 20px', border: '2px solid white' }}>
                                <FaCodeBranch /> Create Database
                            </Button>
                        </td>
                    </tr>
                </tbody>
            </Table>
            <div style={{ marginTop: '20px', fontSize: '18px', color: 'white' }}>
                Note: Free accounts are limited to 1 database. Please visit <a href="/pricing">our pricing page</a> to view premium options with up to 5 databases.
            </div>
        </div>
    );
};

export default Database;