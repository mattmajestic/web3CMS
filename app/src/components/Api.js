import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { solarizedlight } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { Collapse, Button } from 'react-bootstrap';

const components = {
    code({node, inline, className, children, ...props}) {
        const match = /language-(\w+)/.exec(className || '')
        return !inline && match ? (
            <SyntaxHighlighter style={solarizedlight} language={match[1]} PreTag="div" children={String(children).replace(/\n$/, '')} {...props} />
        ) : (
            <code className={className} {...props}>
                {children}
            </code>
        )
    }
}

const Api = () => {
    const [open, setOpen] = useState([true, false, false]);

    const toggleOpen = (index) => {
        const newOpen = [...open];
        newOpen[index] = !newOpen[index];
        setOpen(newOpen);
    };

    const sections = [
        {
            title: 'Workspace API',
            endpoint: '/api/workspace',
            method: 'GET',
            description: 'This endpoint retrieves the workspace data.',
            response: 'A JSON object containing the workspace data.',
            example: `
import requests

response = requests.get('https://codepay.cloud/api/workspace')
data = response.json()

print(data)
            `
        },
        {
            title: 'Bids API',
            endpoint: '/api/bids',
            method: 'GET',
            description: 'This endpoint retrieves the bids data.',
            response: 'A JSON array containing the bids data.',
            example: `
import requests

response = requests.get('https://codepay.cloud/api/bids')
data = response.json()

print(data)
            `
        },
        {
            title: 'Chat API',
            endpoint: '/api/chat',
            method: 'GET',
            description: 'This endpoint retrieves the chat data.',
            response: 'A JSON array containing the chat data.',
            example: `
import requests

response = requests.get('https://codepay.cloud/api/chat')
data = response.json()

print(data)
            `
        }
    ];

    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            {sections.map((section, index) => (
                <div key={index}>
                    <Button onClick={() => toggleOpen(index)} aria-controls={`section-${index}`} aria-expanded={open[index]} variant="outline-primary" className="mb-2">
                        {section.title}
                    </Button>
                    <Collapse in={open[index]}>
                        <div id={`section-${index}`}>
                            <ReactMarkdown components={components}>
                                {`
## ${section.title}

**Endpoint:** \`${section.endpoint}\`

**Method:** \`${section.method}\`

**Description:** ${section.description}

**Response:** ${section.response}

**Example Request (Python):**

\`\`\`python
${section.example}
\`\`\`
                                `}
                            </ReactMarkdown>
                        </div>
                    </Collapse>
                </div>
            ))}
        </div>
    );
};

export default Api;