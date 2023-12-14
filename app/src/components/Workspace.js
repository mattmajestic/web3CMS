import React, { useState, useEffect } from 'react';
import Table from 'react-bootstrap/Table';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import Image from 'react-bootstrap/Image';
import { FaCodeBranch, FaFolderOpen, FaTrash } from 'react-icons/fa';

const Workspace = () => {
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
            name: form.username,
            repository: form.repository,
            branch: form.branch
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
            <h1>CodePay Workspaces</h1>
            <br />
            <Modal show={showModal} onHide={() => setShowModal(false)}>
                <Modal.Header closeButton>
                    <Modal.Title>Create Workspace</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                        <input type="text" name="username" placeholder="GitHub Username" value={form.username} onChange={handleChange} required style={{ padding: '10px', fontSize: '16px' }} />
                        <input type="text" name="repository" placeholder="GitHub Repository" value={form.repository} onChange={handleChange} required style={{ padding: '10px', fontSize: '16px' }} />
                        <input type="text" name="branch" placeholder="Branch" value={form.branch} onChange={handleChange} required style={{ padding: '10px', fontSize: '16px' }} />
                        <Button type="submit" style={{ backgroundColor: '#17072B', color: 'white', fontSize: '20px', padding: '10px 20px' }}>Create Workspace</Button>
                    </form>
                </Modal.Body>
            </Modal>
            <br />
            <Table striped bordered hover style={{ width: '50%' }}>
                <thead>
                    <tr>
                        <th>Workspace Name</th>
                        <th>Repository</th>
                        <th>Branch</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {workspaces.map((workspace, index) => (
                        <tr key={workspace.id}>
                            <td>{workspace.name}</td>
                            <td>{workspace.repository}</td>
                            <td>{workspace.branch}</td>
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
                                <FaCodeBranch /> Create Workspace
                            </Button>
                        </td>
                    </tr>
                </tbody>
            </Table>
            <div style={{ marginTop: '20px', fontSize: '18px', color: 'white' }}>
                Note: Free accounts are limited to 1 workspace. Please visit <a href="/pricing">our pricing page</a> to view premium options with up to 5 workspaces.
            </div>
        </div>
    );
};

export default Workspace;