// About.js
import React from 'react';
import { Table } from 'react-bootstrap';

const About = () => {
    const features = [
        { module: 'Invoice', function: 'Create invoices in USD, BTC, or ETH', link: 'https://web3cms.majesticcoding.com/?page=invoice' },
        { module: 'CRM', function: 'Setup a basic CRM', link: 'https://web3cms.majesticcoding.com/?page=crm' },
        { module: 'AI Chat', function: 'GPT-style chat with your business data', link: 'https://web3cms.majesticcoding.com/?page=ai_chat' },
        { module: 'Dev Docs', function: 'Access web3bms via API, CLI, or Python Package', link: 'https://web3cms.majesticcoding.com/?page=developer_docs' },
        { module: 'Dev Request', function: 'Request software development via a form', link: 'https://web3cms.streamlit.app/?page=developer_request' },
        { module: 'ML Ops', function: 'Model deployment for Linear Regression, Random Forest, Neural Network', link: 'https://web3cms.majesticcoding.com/?page=ml_ops' },
        { module: 'Marketing Mix', function: 'Marketing Mix Modeling with Prophet from Meta', link: 'https://web3cms.majesticcoding.com/?page=mmm' },
        { module: 'BlockSurvey.io', function: 'Integrate User Feedback with BlockSurvey.io', link: 'https://web3cms.majesticcoding.com/?page=block_survey' },
        { module: 'Settings', function: 'Update User, Add Crypto Account & Download App Data as XLSX', link: 'https://web3cms.majesticcoding.com/?page=account_settings' },
    ];

    return (
        <div>
            <h1>web3CMS 💾</h1>
            <p>A web3 Code Management Solution</p>
            <h3>Software Features</h3>
            <Table striped bordered hover>
                <thead>
                    <tr>
                        <th>Module</th>
                        <th>Function</th>
                    </tr>
                </thead>
                <tbody>
                    {features.map((feature, index) => (
                        <tr key={index}>
                            <td><a href={feature.link}>{feature.module}</a></td>
                            <td>{feature.function}</td>
                        </tr>
                    ))}
                </tbody>
            </Table>
        </div>
    );
};

export default About;