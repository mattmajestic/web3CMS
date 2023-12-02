// NavBar.js
import { Navbar, Nav, Button } from 'react-bootstrap';
import { NavLink } from 'react-router-dom';
import ThemeContext from '../ThemeContext';
import { useContext } from 'react';
import { FaSun, FaMoon } from 'react-icons/fa';

function NavBar() {
    const { theme, toggleTheme } = useContext(ThemeContext);

    return (
        <Navbar bg={theme} variant={theme} expand="lg">
            <Navbar.Brand as={NavLink} to="/">
                <img src="/codepay.png" alt="Code Pay" height="80" style={{borderRadius: '50%'}} />
            </Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="mr-auto">
                    <Nav.Link as={NavLink} to="/" end>Home</Nav.Link>
                    <Nav.Link as={NavLink} to="/auth">Login</Nav.Link>
                </Nav>
                <Button variant="secondary" onClick={toggleTheme} className="ml-auto">
                    {theme === 'dark' ? <FaSun /> : <FaMoon />}
                </Button>
            </Navbar.Collapse>
        </Navbar>
    );
}

export default NavBar;