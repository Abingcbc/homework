package org.sse.webcraft.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;
import org.sse.webcraft.mapper.UserMapper;
import org.sse.webcraft.model.UserAuthInfo;

/**
 * @author cbc
 */
@Service
public class AuthService implements UserDetailsService {

    @Autowired
    private UserMapper userMapper;

    @Override
    public UserDetails loadUserByUsername(String s) throws UsernameNotFoundException {
        UserAuthInfo info = userMapper.getUserAuthInfoByUsername(s);
        if (info == null) {
            throw new UsernameNotFoundException(s);
        } else {
            return info;
        }
    }
}
