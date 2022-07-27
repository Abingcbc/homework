package org.sse.tjmall.controller;

import lombok.extern.slf4j.Slf4j;
import org.apache.ibatis.annotations.Param;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.sse.tjmall.dto.CartItem;
import org.sse.tjmall.mapper.CartMapper;
import org.sse.tjmall.service.CartService;

import javax.servlet.http.HttpServletResponse;
import java.util.List;

@Slf4j
@RestController
public class CartController {

    @Autowired
    CartService cartService;

    @Autowired
    CartMapper cartMapper;

    @PostMapping("/add")
    public void addNewItemToCart(@RequestBody CartItem cartItem, HttpServletResponse response) {
        if (!cartService.addNewItemToCart(cartItem)) {
            response.setStatus(HttpServletResponse.SC_CONFLICT);
        }
    }

    @GetMapping("/cart")
    public List<CartItem> getAllCartItemByUsername(@Param("username") String username) {
        return cartMapper.getAllByUsername(username);
    }

    @PostMapping("/remove")
    public void removeCartItem(@RequestBody CartItem cartItem) {
        cartService.removeItem(cartItem);
    }
}
