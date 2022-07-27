package org.sse.tjmall.dto;

import lombok.Data;

import java.sql.Timestamp;

@Data
public class Order {
    private int orderId;
    private String username;
    private int productId;
    private String name;
    private double originalPrice;
    private double newPrice;
    private String imageUrl;
    private String detailUrls;
    private int number;
    private String createTime;
}
