// NavBar.js
import { Navbar, Nav, Button, Dropdown } from 'react-bootstrap';
import { NavLink, Link } from 'react-router-dom';
import ThemeContext from '../ThemeContext';
import { useContext } from 'react';
import { FaSun, FaMoon,FaBoxOpen,FaDollarSign, FaHome, FaBook, FaCloud,FaList, FaSignInAlt,FaRocket, FaComment,FaPencilAlt, FaCog,FaCodeBranch,FaGithub, FaLinkedin,FaBitbucket,FaGitlab } from 'react-icons/fa';
import '../App.css'; 


function NavBar({ session }) {
    const { theme, toggleTheme } = useContext(ThemeContext);

    return (
        <Navbar bg={theme} variant={theme} expand="lg">
            <Navbar.Brand as={NavLink} to="/">
                <img src="/codepay.png" alt="Your Logo" height="80" className="fade-animation" style={{borderRadius: '50%'}} />
            </Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="ml-auto">
                    <Nav.Link as={NavLink} to="/" className="nav-link-custom nav-link-large" end> </Nav.Link>
                    
                    {/* <Nav.Link href="/request" className="nav-link-custom"><FaPencilAlt /> Projects</Nav.Link>
                    <Nav.Link href="/workspace" className="nav-link-custom"><FaCodeBranch /> Workspace</Nav.Link> 
                    <Nav.Link href="/deploy" className="nav-link-custom"><FaRocket /> Deployments</Nav.Link>  */}
                </Nav>
                <div className="d-flex ms-auto">
                <div style={{ display: 'flex', alignItems: 'center', padding: '10px' }}>
                <Dropdown className="mr-2 dropdown-hover">
                        <Dropdown.Toggle variant="secondary" id="dropdown-basic">
                            <FaBoxOpen color="white" size="1.5em" /> <span style={{ fontSize: '1.5em' }}>Products</span>
                        </Dropdown.Toggle>
                        <Dropdown.Menu alignLeft>
                            <Dropdown.Item href="/request">
                                <span style={{ fontSize: '1.5em', color: '#17072B' }}><FaDollarSign color="#17072B" size="1.5em" /> Bids</span>
                            </Dropdown.Item>
                            <Dropdown.Item href="/workspace">
                                <span style={{ fontSize: '1.5em', color: '#17072B' }}><FaCodeBranch color="#17072B" size="1.5em" /> Workspace</span>
                            </Dropdown.Item>
                            <Dropdown.Item href="/deploy">
                                <span style={{ fontSize: '1.5em', color: '#17072B' }}><FaRocket color="#17072B" size="1.5em" /> Deployments</span>
                            </Dropdown.Item>
                            <Dropdown.Item href="/database">
                                <span style={{ fontSize: '1.5em', color: '#17072B' }}><FaCloud color="#17072B" size="1.5em" /> Databases</span>
                            </Dropdown.Item>
                            <Dropdown.Item href="/chat">
                                <span style={{ fontSize: '1.5em', color: '#17072B' }}><FaComment color="#17072B" size="1.5em" /> AI Chat</span>
                            </Dropdown.Item>
                        </Dropdown.Menu>
                    </Dropdown>
                    </div>
                    <div className="d-flex flex-row align-items-center">
                        <Dropdown className="mr-2 dropdown-hover">
                            <Dropdown.Toggle variant="secondary" id="dropdown-basic">
                                <FaGithub color="white" size="2.2em" />
                            </Dropdown.Toggle>
                            <Dropdown.Menu>
                                <Dropdown.Item href="https://github.com/CodePayCloud" target="_blank">
                                    <span style={{ fontSize: '1em', color: '#4B0082' }}><FaGithub color="#4B0082" size="1.5em" /> GitHub</span>
                                </Dropdown.Item>
                                <Dropdown.Item href="https://bitbucket.org/CodePayCloud" target="_blank">
                                    <span style={{ fontSize: '1em', color: '#4B0082' }}><FaBitbucket color="#4B0082" size="1.5em" /> Bitbucket</span>
                                </Dropdown.Item>
                                <Dropdown.Item href="https://gitlab.com/CodePayCloud" target="_blank">
                                    <span style={{ fontSize: '1em', color: '#4B0082' }}><FaGitlab color="#4B0082" size="1.5em" /> GitLab</span>
                                </Dropdown.Item>
                            </Dropdown.Menu>
                        </Dropdown>
                        {session ? (
                        <Button 
                            href="/settings"
                            variant="dark" 
                            className="fade-animation" 
                            style={{backgroundColor: 'white',color: '#17072B', fontWeight: 'bold', fontSize: '18px', margin: '5px', border: '3px solid #2c003e', padding: '10px', textAlign: 'center'}}
                        >
                            <FaCog /> Settings
                        </Button>
                    ) : (
                        <Button 
                            href="/auth"
                            variant="dark" 
                            className="fade-animation" 
                            style={{backgroundColor: 'white',color: '#17072B', fontWeight: 'bold', fontSize: '18px', margin: '5px', border: '3px solid #2c003e', padding: '10px', textAlign: 'center'}}
                        >
                            <FaSignInAlt /> Login
                        </Button>
                    )}
                        {/* <Button variant="secondary" onClick={toggleTheme} className="ml-3" style={{ marginLeft: '10px' }}>
                            {theme === 'dark' ? <FaSun size="2em" /> : <FaMoon size="2em" />}
                        </Button> */}
                    </div>
                </div>
            </Navbar.Collapse>
        </Navbar>
    );
}

export default NavBar;