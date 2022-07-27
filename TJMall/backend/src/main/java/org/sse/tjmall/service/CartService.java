package org.sse.tjmall.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.sse.tjmall.dto.CartItem;
import org.sse.tjmall.mapper.CartMapper;

import java.util.List;

@Service
public class CartService {

    @Autowired
    CartMapper cartMapper;

    @Transactional(rollbackFor = Exception.class)
    public boolean addNewItemToCart(CartItem cartItem) {
        if (cartMapper.isItemAdded(cartItem.getUsername(), cartItem.getProductId()) == null) {
            cartMapper.addNewItemToCart(cartItem.getUsername(), cartItem.getProductId());
        } else {
            cartMapper.addExistItemToCart(cartItem.getUsername(), cartItem.getProductId());
        }
        return true;
    }

    @Transactional(rollbackFor = Exception.class)
    public boolean removeItem(CartItem cartItem) {
        if (cartMapper.isItemAdded(cartItem.getUsername(), cartItem.getProductId()).getNumber() == 1) {
            cartMapper.removeExistItemAll(cartItem.getUsername(), cartItem.getProductId());
        } else {
            cartMapper.removeExistItemOne(cartItem.getUsername(), cartItem.getProductId());
        }
        return true;
    }
}
