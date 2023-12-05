// ApiPage.js
import React from 'react';
import { Container, Button } from 'react-bootstrap';

function ApiPage() {
    return (
        <Container className="mt-5 p-5 rounded" style={{backgroundColor: '#3B3A54'}}>
            <h1>Welcome to the API Playground</h1>
            <p>
                This is a Swagger-based interface for exploring and testing our API endpoints. 
                You can use this interface to try out different API calls, see what responses they return, 
                and understand how to use our API in your own applications.
            </p>
            <p>
                <Button variant="primary" href="/swagger-ui" target="_blank">Go to Swagger UI</Button>
            </p>
        </Container>
    );
}

export default ApiPage;