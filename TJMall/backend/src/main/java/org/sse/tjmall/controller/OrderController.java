package org.sse.tjmall.controller;

import org.apache.ibatis.annotations.Param;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.sse.tjmall.dto.Order;
import org.sse.tjmall.mapper.CartMapper;
import org.sse.tjmall.mapper.OrderMapper;

import java.util.List;

@RestController
public class OrderController {

    @Autowired
    OrderMapper orderMapper;

    @Autowired
    CartMapper cartMapper;

    @Transactional()
    @PostMapping("/order")
    public void createNewOrder(@RequestBody Order order) {
        if (order.getNumber() != -1) {
            cartMapper.removeExistItemAll(order.getUsername(), order.getProductId());
            orderMapper.createNewOrder(order.getUsername(), order.getProductId(), order.getNumber());
        } else {
            orderMapper.createNewOrder(order.getUsername(), order.getProductId(), 1);
        }
    }

    @GetMapping("/order")
    public List<Order> getAllOrderByUsername(@Param("username") String username) {
        return orderMapper.getOrderByUsername(username);
    }
}
