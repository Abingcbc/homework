package org.sse.tjmall.controller;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.sse.tjmall.dto.User;
import org.sse.tjmall.service.UserService;

import javax.servlet.http.HttpServletResponse;

@RestController
@Slf4j
public class UserController {

    @Autowired
    UserService userService;

    @PostMapping("/login")
    public void login(@RequestBody User user, HttpServletResponse response) {
        log.info("login: " + user);
        if (!userService.login(user)) {
            log.info("login fail!");
            response.setStatus(HttpServletResponse.SC_FORBIDDEN);
        }
    }

    @PostMapping("/register")
    public void register(@RequestBody User user, HttpServletResponse response) {
        log.info("register: " + user);
        if (!userService.register(user)) {
            response.setStatus(HttpServletResponse.SC_CONFLICT);
        }
    }
}
