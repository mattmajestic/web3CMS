// DocsPage.js
import React from 'react';
import { Container, Button } from 'react-bootstrap';

function Docs() {
    return (
        <Container className="mt-5 p-5 rounded" style={{backgroundColor: '#3B3A54'}}>
            <h1>Welcome to the Project Documentation</h1>
            <p>
                Here you can find comprehensive documentation for our project. This includes detailed descriptions of all features, step-by-step guides, and references to help you understand and use our project effectively.
            </p>
            <p>
                <Button variant="primary" href="/docs-pdf" target="_blank">Download PDF Documentation</Button>
            </p>
        </Container>
    );
}

export default Docs;