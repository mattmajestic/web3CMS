import React, { useState } from 'react';
import { Container, Button, Row, Col, Alert,Nav,Dropdown } from 'react-bootstrap';
import { useNavigate, Link } from 'react-router-dom';
import { FaSignInAlt, FaPencilAlt, FaBook, FaComments, FaCodeBranch,FaGithub, FaRocket, FaCloud } from 'react-icons/fa';
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
        <Container className="mt-5 p-5 rounded d-flex flex-column align-items-center" style={{backgroundColor: '#3B3A54'}}>
            <h1>Welcome to CodePay</h1>
            <br></br>

            <div style={{ textAlign: 'center' }}>
                <img src="/codepay.png" alt="CodePay Logo" style={{width: '180px', height: '180px', borderRadius: '50%', objectFit: 'cover', border: '18px solid transparent', borderImageSource: 'linear-gradient(to bottom, grey, white)', borderImageSlice: 1}}/>
                <h5>CodePay is a platform that connects coders with those who need coding tasks done.</h5>
                <h3>CodePay is the place for you.</h3>
            </div>
            <br></br>
            <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '20px' }}>
                <Button variant="dark" href='/auth' style={{backgroundColor: 'white',color: 'green', fontWeight: 'bold', fontSize: '30px', margin: '5px', border: '3px solid #2c003e', padding: '10px', textAlign: 'center'}}>
                    <FaSignInAlt /> Login
                </Button>
            </div>
            <Dropdown className="mr-2 dropdown-hover">
                        <Dropdown.Toggle variant="secondary" id="dropdown-basic" style={{ backgroundColor: 'white' }}>
                            <FaRocket color="#4B0082" size="2em" /> <span style={{ fontSize: '1.5em', color: '#4B0082' }}>CodePay Products</span>
                        </Dropdown.Toggle>
                        <Dropdown.Menu>
                            <Dropdown.Item href="/request">
                                <span style={{ fontSize: '1.5em', color: '#4B0082' }}><FaPencilAlt color="#4B0082" size="1.5em" /> Projects</span>
                            </Dropdown.Item>
                            <Dropdown.Item href="/workspace">
                                <span style={{ fontSize: '1.5em', color: '#4B0082' }}><FaCodeBranch color="#4B0082" size="1.5em" /> Workspace</span>
                            </Dropdown.Item>
                            <Dropdown.Item href="/deploy">
                                <span style={{ fontSize: '1.5em', color: '#4B0082' }}><FaRocket color="#4B0082" size="1.5em" /> Deployments</span>
                            </Dropdown.Item>
                            <Dropdown.Item href="/database">
                                <span style={{ fontSize: '1.5em', color: '#4B0082' }}><FaCloud color="#4B0082" size="1.5em" /> Databases</span>
                            </Dropdown.Item>
                        </Dropdown.Menu>
                    </Dropdown>  
        </Container>
    );
}

export default Home;