// NavBar.js
import { Navbar, Nav, Button } from 'react-bootstrap';
import { NavLink } from 'react-router-dom';
import ThemeContext from '../ThemeContext';
import { useContext } from 'react';
import { FaSun, FaMoon, FaHome, FaBook, FaCloud, FaSignInAlt, FaComment,FaPencilAlt, FaCog,FaCodeBranch,FaGithub } from 'react-icons/fa';

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
                    <Nav.Link as={NavLink} to="/" className="nav-link-custom nav-link-large" end> <FaHome /> Code Pay</Nav.Link>
                    <Nav.Link href="/request" className="nav-link-custom"><FaPencilAlt /> Bid on Branch</Nav.Link>
                    <Nav.Link href="/workspace" className="nav-link-custom"><FaCodeBranch /> Workspace</Nav.Link>
                    <div className="d-flex flex-column mb-2">
                        <Nav.Link href="/chat" className="nav-link-custom"><FaComment /> Chat</Nav.Link>
                    </div>
                    <div className="d-flex flex-column mb-2">
                        {session ? (
                            <Nav.Link href="/settings" className="nav-link-custom"><FaCog /> Settings</Nav.Link>
                        ) : (
                            <Nav.Link href="/auth" className="nav-link-custom"><FaSignInAlt /> Login</Nav.Link>
                        )}
                    </div>
                </Nav>
                <div className="d-flex ms-auto">
                <div className="d-flex flex-row align-items-center">
                    <Navbar.Brand href="https://github.com/CodePayCloud" target="_blank" className="ml-2">
                        <FaGithub color="white" size="2em" />
                    </Navbar.Brand>
                    <Button variant="secondary" onClick={toggleTheme} className="ml-2">
                        {theme === 'dark' ? <FaSun size="2em" /> : <FaMoon size="2em" />}
                    </Button>
                </div>
                </div>
            </Navbar.Collapse>
        </Navbar>
    );
}

export default NavBar;