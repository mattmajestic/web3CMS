import React from 'react';
import { Container } from 'react-bootstrap';

function About() {
    const mermaidUrl = "https://mermaid.ink/img/pako:eNpNkM-KwkAMxl8l5LQL9gV6ENQiHlYQ3ZvjIXQyWpg_Os2wSNt332mrYE7h-35fQtJhHTRjicaGv_pGUeC3Uh5yrc4_4dr4CxTFEtZfR34kbgVMiLDJme8XBZPfb4K7WxZu4ZCshRfdw64b4TjM9HqCq-5AT_jUq1HvT-w1ZMuxz8nt2VBpqNDBWopv_TIHttOgHS7QcXTU6HxCN1oK5caOFZa51WwoWVGo_JBRShJOT19jKTHxAtNdk3DV0DWSw7zLtlll3UiI-_kt03eGf4v8XqU?type=png";

    return (
        <Container className="mt-5 p-5 rounded" style={{backgroundColor: '#3B3A54'}}>
            <h1>Welcome to CodePay</h1>
            <p>
                CodePay is a platform that connects coders with those who need coding tasks done. 
                Whether you're a coder looking for projects, or you need a coder to complete a task, 
                CodePay is the place for you.
            </p>
            <h2 className="text-center">User Flow</h2>
            <div className="d-flex justify-content-center">
                <img src={mermaidUrl} alt="Mermaid diagram" />
            </div>
        </Container>
    );
}

export default About;