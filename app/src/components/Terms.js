import React from 'react';
import { Link } from 'react-router-dom';
import { FaHome } from 'react-icons/fa';

const Terms = () => {
    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh', fontSize: '24px', padding: '50px', backgroundColor: '#17072B', color: 'white' }}>
            <h1>Terms and Conditions</h1>
            <ul style={{ textAlign: 'left' }}>
                <li>You must not use this software for any illegal or unauthorized purpose.</li>
                <li>You agree not to reproduce, duplicate, copy, sell, resell or exploit any portion of the software without express written permission by us.</li>
                <li>We may, but have no obligation to, remove content and accounts containing content that we determine in our sole discretion are unlawful, offensive, threatening, libelous, defamatory, pornographic, obscene or otherwise objectionable or violates any party’s intellectual property or these Terms of Service.</li>
                <li>Verbal, physical, written or other abuse (including threats of abuse or retribution) of any customer, employee, member, or officer will result in immediate account termination.</li>
                <li>You understand that the technical processing and transmission of the Service, including your content, may be transferred unencrypted and involve (a) transmissions over various networks; and (b) changes to conform and adapt to technical requirements of connecting networks or devices.</li>
            </ul>
            <Link to="/" style={{ marginTop: '20px', color: 'white', textDecoration: 'underline' }}>
                <FaHome /> Back to Home
            </Link>
        </div>
    );
};

export default Terms;