import React, { useState } from 'react';
import { Container, Button, Row, Col, Alert,Nav,Dropdown } from 'react-bootstrap';
import { useNavigate, Link } from 'react-router-dom';
import { FaSignInAlt, FaPencilAlt, FaBook, FaComments, FaCodeBranch,FaGithub, FaRocket, FaCloud,FaLinkedin } from 'react-icons/fa';
import Chat from './Chat';
import Request from './Request'; 
import Auth from './Auth'; 
import { isMobile } from 'react-device-detect';
import Modal from 'react-modal';

function Home() {
    const mermaidUrl = "https://mermaid.ink/img/pako:eNpVkM1ugzAQhF9ltYeeSMRPgoFDpRIatYdIVZJeWnqwsJOggo2MaZIS3r02iVrVJ2tn_I13eiwk45jgrpLH4kCVhm2WCzDn4T2lLYeV0asPmEzu4fLacgXPoul0e4H0ZoOb1lSSMs5gRTVXJa2spd8qWgo7tJTh_4tFJTsGGy0V3XNYlhX_o6ZXSyaLruZCt3AHW97a2KxfGJa6sdLR9nhqKpMDVrnAsl_zr5Iff03ZFTb-pYWMagpajmZ4WRvkk0WWYg-p1AM6WHNV05KZVnoLyFEfeM1zTMyVUfWZYy6sj3Zabs6iwESrjjvYNczsnpV0r2iNyc50YKaclWbF1bXmsW0HGyow6fGEiecGUy8MfDKPg9AP48B38IyJ70bTmRv4czcOiefFXjg4-C2lwXpTl8SEhH5EXBJFczIbeW-jOGYOP72vkcc?type=png";
    const [showDiagram, setShowDiagram] = useState(false);
    const [showChat, setShowChat] = useState(false);
    const [showRequestForm, setShowRequestForm] = useState(false);
    const [showAuth, setShowAuth] = useState(false);
    const [modalIsOpen, setModalIsOpen] = useState(isMobile);

  const closeModal = () => {
    setModalIsOpen(false);
  };


    return (
        <Container className="mt-5 p-5 rounded d-flex flex-column align-items-center" style={{backgroundColor: '#3B3A54'}}>
        <Modal
          isOpen={modalIsOpen}
          onRequestClose={closeModal}
          style={{
            overlay: { backgroundColor: 'rgba(0, 0, 0, 0.5)' },
            content: {
              color: 'white',
              backgroundColor: '#17072B',
              padding: '20px',
              borderRadius: '10px',
              width: '50%',
              height: '50%',
              position: 'absolute',
              top: '25%',
              left: '25%'
            }
          }}
          contentLabel="Mobile Warning"
        >
          <h2>Mobile Optimization Coming Soon.</h2>
          <button 
            onClick={closeModal} 
            style={{ 
              backgroundColor: 'white', 
              color: '#17072B', 
              padding: '10px', 
              borderRadius: '5px', 
              border: 'none', 
              cursor: 'pointer' 
            }}
          >
            Proceed
          </button>
        </Modal>
            <h1>Welcome to CodePay</h1>
            <div style={{ textAlign: 'center' }}>
                <img src="/codepay.png" alt="CodePay Logo" className="fade-animation" style={{width: '240px', height: '240px', borderRadius: '50%', objectFit: 'cover', border: '18px solid transparent'}}/>
                <br></br>
                <h4>We help you monetize your code.</h4>
            </div>
            <br></br>
            <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '3px' }}>
                <Button variant="dark" href='/auth' className="fade-animation" style={{backgroundColor: 'white',color: '#17072B', fontWeight: 'bold', fontSize: '30px', margin: '5px', border: '3px solid #2c003e', padding: '10px', textAlign: 'center'}}>
                    <FaSignInAlt /> Login
                </Button>   
            </div>
            <div className="fade-animation" style={{ display: 'flex', justifyContent: 'center', marginBottom: '20px' }}>
                <a href="https://www.github.com/codepaycloud" className="fade-animation" style={{color: 'white', fontWeight: 'bold', fontSize: '60px', margin: '5px', textAlign: 'center'}}>
                    <FaGithub />
                </a>
                <a href="https://www.linkedin.com/company/codepay-cloud" target="_blank" className="fade-animation" style={{color: 'white', fontWeight: 'bold', fontSize: '60px', margin: '5px', textAlign: 'center'}}>
                    <FaLinkedin />
                </a>
            </div>
        </Container>
    );
}

export default Home;