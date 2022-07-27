package org.sse.webcraft.service;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;
import org.sse.webcraft.mapper.UserMapper;
import org.sse.webcraft.model.UserAuthInfo;

@Slf4j
@Service
public class UserService {

    @Autowired
    UserMapper userMapper;

    private BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

    public int register(String username, String password) {
        if (userMapper.getUserAuthInfoByUsername(username) != null) {
            return 0;
        } else {
            password = passwordEncoder.encode(password);
            if (userMapper.createNewUser(username, password) == 1) {
                return 1;
            } else {
                return -1;
            }
        }
    }

    public boolean checkTokenPermission(Authentication authentication,
                                           String username) {
        log.info(authentication.getPrincipal().toString());
        return ((UserAuthInfo) authentication.getPrincipal()).getUsername().equals(username);
    }
}
