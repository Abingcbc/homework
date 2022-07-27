package org.sse.tjmall.controller;

import lombok.extern.slf4j.Slf4j;
import org.apache.ibatis.annotations.Param;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.sse.tjmall.dto.Product;
import org.sse.tjmall.mapper.ProductMapper;

import java.util.List;

@Slf4j
@RestController
public class ProductController {

    @Autowired
    ProductMapper productMapper;

    @GetMapping("/detail")
    Product getProductDetail(@Param("productId") Integer productId) {
        if (productId == null || productId <= 0) {
            return null;
        } else {
            return productMapper.getProductById(productId);
        }
    }

    @GetMapping("/search")
    List<Product> getProduct(@Param("keyword") String keyword) {
        log.info(keyword);
        if (keyword == null || keyword.length() == 0) {
            return productMapper.getAllProduct();
        } else {
            return productMapper.getProductByKeyword('%' + keyword + '%');
        }
    }

    @GetMapping("/all")
    List<Product> getAllProduct() {
        return productMapper.getAllProduct();
    }
}
