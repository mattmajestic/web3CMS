// NavBar.js
import { Navbar, Nav, Button, Dropdown } from 'react-bootstrap';
import { NavLink, Link } from 'react-router-dom';
import ThemeContext from '../ThemeContext';
import { useContext } from 'react';
import { FaSun, FaMoon, FaHome, FaBook, FaCloud,FaList, FaSignInAlt,FaRocket, FaComment,FaPencilAlt, FaCog,FaCodeBranch,FaGithub, FaLinkedin,FaBitbucket,FaGitlab } from 'react-icons/fa';
import '../App.css'; // Import the CSS file

function NavBar({ session }) {
    const { theme, toggleTheme } = useContext(ThemeContext);

    return (
        <Navbar bg={theme} variant={theme} expand="lg">
            <Navbar.Brand as={NavLink} to="/">
                <img src="/codepay.png" alt="Your Logo" height="80" style={{borderRadius: '50%'}} />
            </Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="ml-auto">
                    <Nav.Link as={NavLink} to="/" className="nav-link-custom nav-link-large" end> </Nav.Link>
                    <Dropdown className="mr-2 dropdown-hover">
                        <Dropdown.Toggle variant="secondary" id="dropdown-basic">
                            <FaRocket color="white" size="2em" /> <span style={{ fontSize: '1.5em' }}>CodePay Products</span>
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
                        </Dropdown.Menu>
                    </Dropdown>
                    {/* <Nav.Link href="/request" className="nav-link-custom"><FaPencilAlt /> Projects</Nav.Link>
                    <Nav.Link href="/workspace" className="nav-link-custom"><FaCodeBranch /> Workspace</Nav.Link> 
                    <Nav.Link href="/deploy" className="nav-link-custom"><FaRocket /> Deployments</Nav.Link>  */}
                </Nav>
                <div className="d-flex ms-auto">
                    <div className="d-flex flex-row align-items-center">
                        {session ? (
                            <Nav.Link href="/settings" className="nav-link-custom" style={{ paddingRight: '20px' }}><FaCog /> Settings</Nav.Link>
                        ) : (
                            <Nav.Link href="/auth" className="nav-link-custom" style={{ paddingRight: '20px' }}><FaSignInAlt /> Login</Nav.Link>
                        )}
                    <Navbar.Brand as={Link} to="/chat" className="ml-2">
                        <FaComment color="white" size="2em" />
                    </Navbar.Brand>
                        <Navbar.Brand href="https://www.linkedin.com/company/codepay-cloud" target="_blank" className="ml-2">
                            <FaLinkedin color="white" size="2em" />
                        </Navbar.Brand>
                        <Dropdown className="mr-2 dropdown-hover">
                            <Dropdown.Toggle variant="secondary" id="dropdown-basic">
                                <FaGithub color="white" size="2em" /> Code
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
                        <Button variant="secondary" onClick={toggleTheme} className="ml-3" style={{ marginLeft: '10px' }}>
                            {theme === 'dark' ? <FaSun size="2em" /> : <FaMoon size="2em" />}
                        </Button>
                    </div>
                </div>
            </Navbar.Collapse>
        </Navbar>
    );
}

export default NavBar;