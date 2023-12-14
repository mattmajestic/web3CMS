import React, { useState, useEffect } from 'react';
import Table from 'react-bootstrap/Table';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import Image from 'react-bootstrap/Image';

const Workspace = () => {
    const [form, setForm] = useState({ username: '', repository: '' });
    const [workspaces, setWorkspaces] = useState([{ id: 1, name: 'Example Workspace', repository: 'example-repo', branch: 'main' }]);
    const [showModal, setShowModal] = useState(false);

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (workspaces.length >= 1) {
            alert('You get 1 workspace for free. Go to /pricing to see premium features.');
        } else {
            // Handle workspace creation here
            setShowModal(false);
        }
    };

    const handleOpen = (workspaceId) => {
        // Handle workspace opening here
    };

    const handleDelete = (workspaceId) => {
        // Handle workspace deletion here
    };

    useEffect(() => {
        // Fetch active workspaces here and set them to the state
    }, []);

    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh' }}>
            <Image src="codepay.png" rounded style={{ width: '100px', height: '100px', marginBottom: '20px' }} />
            <h1>CodePay Workspaces</h1>
            <br />
            <br />
            <Button onClick={() => setShowModal(true)} style={{ marginBottom: '20px', backgroundColor: '#17072B', color: 'white', fontSize: '20px', padding: '10px 20px' }}>Create Workspace</Button>
            <br />
            <Modal show={showModal} onHide={() => setShowModal(false)}>
                <Modal.Header closeButton>
                    <Modal.Title>Create Workspace</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <form onSubmit={handleSubmit}>
                        <input type="text" name="username" placeholder="GitHub Username" value={form.username} onChange={handleChange} required />
                        <input type="text" name="repository" placeholder="GitHub Repository" value={form.repository} onChange={handleChange} required />
                        <Button type="submit">Create Workspace</Button>
                    </form>
                </Modal.Body>
            </Modal>
            <br />
            <Table striped bordered hover style={{ width: '80%' }}>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Workspace Name</th>
                        <th>Repository</th>
                        <th>Branch</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {workspaces.map((workspace, index) => (
                        <tr key={workspace.id}>
                            <td>{index + 1}</td>
                            <td>{workspace.name}</td>
                            <td>{workspace.repository}</td>
                            <td>{workspace.branch}</td>
                            <td>
                                <Button variant="success" onClick={() => handleOpen(workspace.id)} style={{ marginRight: '10px' }}>Open</Button>
                                <Button variant="danger" onClick={() => handleDelete(workspace.id)}>Delete</Button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </Table>
        </div>
    );
};

export default Workspace;