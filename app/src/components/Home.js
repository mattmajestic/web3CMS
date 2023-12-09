import React, { useState } from 'react';
import { Container, Button, Row, Col } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { FaSun, FaSignInAlt, FaPencilAlt, FaBook } from 'react-icons/fa';

function About() {
    const mermaidUrl = "https://mermaid.ink/img/pako:eNpNkM-KwkAMxl8l5LQL9gV6ENQiHlYQ3ZvjIXQyWpg_Os2wSNt332mrYE7h-35fQtJhHTRjicaGv_pGUeC3Uh5yrc4_4dr4CxTFEtZfR34kbgVMiLDJme8XBZPfb4K7WxZu4ZCshRfdw64b4TjM9HqCq-5AT_jUq1HvT-w1ZMuxz8nt2VBpqNDBWopv_TIHttOgHS7QcXTU6HxCN1oK5caOFZa51WwoWVGo_JBRShJOT19jKTHxAtNdk3DV0DWSw7zLtlll3UiI-_kt03eGf4v8XqU?type=png";
    const [showDiagram, setShowDiagram] = useState(false);
    const navigate = useNavigate();

    return (
        <Container className="mt-5 p-5 rounded" style={{backgroundColor: '#3B3A54'}}>
            <h1>Welcome to CodePay</h1>
            <p>
                CodePay is a platform that connects coders with those who need coding tasks done. 
                Whether you're a coder looking for projects, or you need a coder to complete a task, 
                CodePay is the place for you.
            </p>
            <Row className="justify-content-md-center mt-4">
                <Col xs lg="2">
                    <Button variant="dark" onClick={() => navigate('/settings')} style={{backgroundColor: '#6C3483', fontWeight: 'bold', width: '150px', margin: '10px'}}>
                        <FaSun /> Settings
                    </Button>
                </Col>
                <Col xs lg="2">
                    <Button variant="dark" onClick={() => navigate('/login')} style={{backgroundColor: '#6C3483', fontWeight: 'bold', width: '150px', margin: '10px'}}>
                        <FaSignInAlt /> Login
                    </Button>
                </Col>
                <Col xs lg="2">
                    <Button variant="dark" onClick={() => navigate('/request')} style={{backgroundColor: '#6C3483', fontWeight: 'bold', width: '150px', margin: '10px'}}>
                        <FaPencilAlt /> Request Form
                    </Button>
                </Col>
            </Row>
            <Row className="justify-content-md-center mt-4">
                <Col xs lg="2">
                <Button onClick={() => setShowDiagram(!showDiagram)} style={{backgroundColor: '#FFFFFF', color: '#6C3483', fontWeight: 'bold', width: '150px', margin: '10px'}}>
                { showDiagram ? 'Hide' : 'Show'}  User Journey <FaBook />
            </Button>
            {showDiagram && (
                <div className="d-flex justify-content-center">
                    <img src={mermaidUrl} alt="Mermaid diagram" />
                </div>
            )}
                </Col>
            </Row>
        </Container>
    );
}

export default About;