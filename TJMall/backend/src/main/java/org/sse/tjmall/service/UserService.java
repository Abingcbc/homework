package org.sse.tjmall.service;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.sse.tjmall.dto.User;
import org.sse.tjmall.mapper.UserMapper;

@Service
@Slf4j
public class UserService {

    @Autowired
    UserMapper userMapper;

    public boolean login(User unValidUser) {
        User user = userMapper.getUserByUsername(unValidUser.getUsername());
        return user != null && user.getPassword().equals(unValidUser.getPassword());
    }

    public boolean register(User newUser) {
        if (userMapper.getUserByUsername(newUser.getUsername()) == null) {
            userMapper.createNewUser(newUser.getUsername(),
                    newUser.getPassword());
            return true;
        } else {
            return false;
        }
    }
}
