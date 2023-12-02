import { useEffect } from 'react';
import { supabase } from '../supabaseClient';
import { Auth } from '@supabase/auth-ui-react';
import { ThemeSupa } from '@supabase/auth-ui-shared';

function SignUp() {
    return (
        <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', width: '300px', height: '500px', margin: 'auto', position: 'absolute', top: 0, left: 0, bottom: 0, right: 0 }}>
            <h2>Sign Up</h2>
            <Auth
                supabaseClient={supabase}
                appearance={{ theme: ThemeSupa }}
                providers={['github', 'bitbucket', 'gitlab']}
            />
        </div>
    );
}

export default SignUp;