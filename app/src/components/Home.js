import React, { useState } from 'react';
import { Container, Button, Row, Col, Alert } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { FaSun, FaSignInAlt, FaPencilAlt, FaBook, FaComments } from 'react-icons/fa';
import Chat from './Chat';
import Request from './Request'; 
import Settings from './Settings'; 

function Home() {
    const mermaidUrl = "https://mermaid.ink/img/pako:eNpNkM-KwkAMxl8l5LQL9gV6ENQiHlYQ3ZvjIXQyWpg_Os2wSNt332mrYE7h-35fQtJhHTRjicaGv_pGUeC3Uh5yrc4_4dr4CxTFEtZfR34kbgVMiLDJme8XBZPfb4K7WxZu4ZCshRfdw64b4TjM9HqCq-5AT_jUq1HvT-w1ZMuxz8nt2VBpqNDBWopv_TIHttOgHS7QcXTU6HxCN1oK5caOFZa51WwoWVGo_JBRShJOT19jKTHxAtNdk3DV0DWSw7zLtlll3UiI-_kt03eGf4v8XqU?type=png";
    const [showDiagram, setShowDiagram] = useState(false);
    const [showChat, setShowChat] = useState(false);
    const [showRequestForm, setShowRequestForm] = useState(false); // New state variable
    const navigate = useNavigate();

    return (
        <Container className="mt-5 p-5 rounded" style={{backgroundColor: '#3B3A54'}}>
            <h1>Welcome to CodePay</h1>
            <p>
                CodePay is a platform that connects coders with those who need coding tasks done. 
                Whether you're a coder looking for projects, or you need a coder to complete a task, 
                CodePay is the place for you.
            </p>
            <Alert variant="info">
                Hey, you need to <Alert.Link onClick={() => navigate('/auth')}>login</Alert.Link> then use the settings button to customize.
            </Alert>
            <Row className="justify-content-md-center mt-4">
                <Col xs lg="2">
                    <Button variant="dark" onClick={() => navigate('/settings')} style={{backgroundColor: '#6C3483', fontWeight: 'bold', width: '150px', margin: '10px'}}>
                        <FaSun /> Settings
                    </Button>
                </Col>
                <Col xs lg="2">
                    <Button variant="dark" onClick={() => setShowChat(!showChat)} style={{backgroundColor: '#6C3483', fontWeight: 'bold', width: '150px', margin: '10px'}}>
                        <FaComments /> Chat
                    </Button>
                </Col>
                <Col xs lg="2">
                    <Button variant="dark" onClick={() => setShowRequestForm(!showRequestForm)} style={{backgroundColor: '#6C3483', fontWeight: 'bold', width: '150px', margin: '10px'}}>
                        <FaPencilAlt /> Request Form
                    </Button>
                </Col>
                <Col xs lg="2">
                    <Button onClick={() => setShowDiagram(!showDiagram)} style={{backgroundColor: '#FFFFFF', color: '#6C3483', fontWeight: 'bold', width: '150px', margin: '10px'}}>
                        { showDiagram ? 'Hide' : 'Show'}  User Journey <FaBook />
                    </Button>
                </Col>
            </Row>
            {showChat && (
                <Row className="justify-content-md-center mt-4">
                    <Col xs={12}>
                        <div style={{maxHeight: '200px', overflowY: 'auto'}}>
                            <Chat />
                        </div>
                    </Col>
                </Row>
            )}
            {showRequestForm && (
                <Row className="justify-content-md-center mt-4">
                    <Col xs={12}>
                        <div style={{maxHeight: '200px', overflowY: 'auto'}}>
                            <Request />
                        </div>
                    </Col>
                </Row>
            )}
            {showDiagram && (
                <Row className="justify-content-md-center mt-4">
                    <Col xs={12}>
                        <div className="d-flex justify-content-center">
                            <img src={mermaidUrl} alt="Mermaid diagram" />
                        </div>
                    </Col>
                </Row>
            )}
        </Container>
    );
}

export default Home;