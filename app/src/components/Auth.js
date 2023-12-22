import { useEffect } from 'react';
import { supabase } from '../supabaseClient';
import { Auth } from '@supabase/auth-ui-react';
import { ThemeSupa } from '@supabase/auth-ui-shared';
import styles from '../SignUp.module.css'; // Import the CSS file

function SignUp() {
    return (
        <div style={{
            display: 'flex', 
            flexDirection: 'column', 
            justifyContent: 'center', 
            alignItems: 'center', 
            width: '100%', 
            maxWidth: '40%', 
            height: '100vh', 
            margin: 'auto', 
            position: 'absolute', 
            top: 0, 
            left: 0, 
            bottom: 0, 
            right: 0,
        }}>
            <h2 style={{fontSize: '2em'}}>Login</h2>
            <div style={{ 
                width: '100%', 
                height: '600px',
            }}>
                <Auth
                    supabaseClient={supabase}
                    appearance={{ theme: ThemeSupa }}
                    providers={['github', 'bitbucket', 'gitlab', 'google','linkedin_oidc']}
                />
            </div>
        </div>
    );
}

export default SignUp;