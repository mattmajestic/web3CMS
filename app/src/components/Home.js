import React, { useState } from 'react';
import { Container, Button, Row, Col, Alert } from 'react-bootstrap';
import { useNavigate, Link } from 'react-router-dom';
import { FaSignInAlt, FaPencilAlt, FaBook, FaComments, FaCodeBranch,FaGithub } from 'react-icons/fa';
import Chat from './Chat';
import Request from './Request'; 
import Auth from './Auth'; 

function Home() {
    const mermaidUrl = "https://mermaid.ink/img/pako:eNpVkM1ugzAQhF9ltYeeSMRPgoFDpRIatYdIVZJeWnqwsJOggo2MaZIS3r02iVrVJ2tn_I13eiwk45jgrpLH4kCVhm2WCzDn4T2lLYeV0asPmEzu4fLacgXPoul0e4H0ZoOb1lSSMs5gRTVXJa2spd8qWgo7tJTh_4tFJTsGGy0V3XNYlhX_o6ZXSyaLruZCt3AHW97a2KxfGJa6sdLR9nhqKpMDVrnAsl_zr5Iff03ZFTb-pYWMagpajmZ4WRvkk0WWYg-p1AM6WHNV05KZVnoLyFEfeM1zTMyVUfWZYy6sj3Zabs6iwESrjjvYNczsnpV0r2iNyc50YKaclWbF1bXmsW0HGyow6fGEiecGUy8MfDKPg9AP48B38IyJ70bTmRv4czcOiefFXjg4-C2lwXpTl8SEhH5EXBJFczIbeW-jOGYOP72vkcc?type=png";
    const [showDiagram, setShowDiagram] = useState(false);
    const [showChat, setShowChat] = useState(false);
    const [showRequestForm, setShowRequestForm] = useState(false);
    const [showAuth, setShowAuth] = useState(false);

    return (
        <Container className="mt-5 p-5 rounded" style={{backgroundColor: '#3B3A54'}}>
            <h1>Welcome to CodePay</h1>
            <br></br>
            <h5>
                CodePay is a platform that connects coders with those who need coding tasks done. 
                Whether you're a coder looking for projects, or you need a coder to complete a task, 
                CodePay is the place for you.
            </h5>
            <br></br>
            <Alert variant="info">
                Get started getting paid for your Code!  Start by <Link to="/auth">Logging in</Link> via Github, Gitlab or Bitbucket
            </Alert>
            <br></br>
            {showAuth && <Auth />}
            <Row className="justify-content-md-center mt-4">
                <Col xs lg="2">
                    <Button variant="dark" onClick={() => setShowChat(!showChat)} style={{backgroundColor: '#4B0082', fontWeight: 'bold', width: '200px', height: '60px', fontSize: '20px', margin: '10px', border: '3px solid #2c003e'}}>
                        <FaComments /> Chat
                    </Button>
                </Col>
                <Col xs lg="2">
                    <Button variant="dark" onClick={() => window.open('https://codepaycloud.github.io/docs', '_blank')} style={{backgroundColor: '#4B0082', fontWeight: 'bold', width: '200px', height: '60px', fontSize: '20px', margin: '10px', border: '3px solid #2c003e'}}>
                        <FaGithub /> Docs
                    </Button>
                </Col>
                <Col xs lg="2">
                    <Button onClick={() => setShowDiagram(!showDiagram)} style={{backgroundColor: '#4B0082', fontWeight: 'bold', width: '200px', height: '60px', fontSize: '20px', margin: '10px', border: '3px solid #2c003e'}}>
                        { showDiagram ? 'Hide' : 'Show'}  MLOps <FaBook />
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