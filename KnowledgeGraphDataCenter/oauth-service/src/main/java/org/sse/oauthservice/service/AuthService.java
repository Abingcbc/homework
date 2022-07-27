package org.sse.oauthservice.service;

import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;
import org.sse.oauthservice.model.UserAuthInfo;

@Service
public class AuthService implements UserDetailsService {

    private BCryptPasswordEncoder encoder = new BCryptPasswordEncoder();
    @Override
    public UserDetails loadUserByUsername(String s) throws UsernameNotFoundException {
        UserAuthInfo userAuthInfo = new UserAuthInfo();
        userAuthInfo.setUsername(s);
        userAuthInfo.setPassword(encoder.encode(s));
        return userAuthInfo;
    }
}
