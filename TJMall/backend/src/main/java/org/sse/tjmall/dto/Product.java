package org.sse.tjmall.dto;

import lombok.Data;

@Data
public class Product {
    private int productId;
    private String name;
    private double originalPrice;
    private double newPrice;
    private String imageUrl;
    private String detailUrls;
}
