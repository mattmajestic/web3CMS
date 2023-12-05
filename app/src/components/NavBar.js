// NavBar.js
import { Navbar, Nav, Button } from 'react-bootstrap';
import { NavLink } from 'react-router-dom';
import ThemeContext from '../ThemeContext';
import { useContext } from 'react';
import { FaSun, FaMoon, FaHome, FaBook, FaCloud, FaSignInAlt } from 'react-icons/fa';

function NavBar() {
    const { theme, toggleTheme } = useContext(ThemeContext);

    return (
        <Navbar bg={theme} variant={theme} expand="lg">
            <Navbar.Brand as={NavLink} to="/">
                <img src="/codepay.png" alt="Your Logo" height="80" style={{borderRadius: '50%'}} />
            </Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="ml-auto">
                    <Nav.Link as={NavLink} to="/" className="nav-link-custom" end><FaHome /> Home</Nav.Link>
                    <Nav.Link href="/docs" className="nav-link-custom"><FaBook /> Docs</Nav.Link>
                    <Nav.Link href="/api" className="nav-link-custom"><FaCloud /> API</Nav.Link>
                </Nav>
                <div className="d-flex ms-auto">
                    <Nav.Link href="/auth" className="nav-link-custom"><FaSignInAlt /> Login</Nav.Link>
                    <Button variant="secondary" onClick={toggleTheme} className="ml-2">
                        {theme === 'dark' ? <FaSun /> : <FaMoon />}
                    </Button>
                </div>
            </Navbar.Collapse>
        </Navbar>
    );
}

export default NavBar;