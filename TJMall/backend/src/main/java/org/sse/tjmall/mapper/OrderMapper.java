package org.sse.tjmall.mapper;

import org.apache.ibatis.annotations.*;
import org.springframework.stereotype.Component;
import org.sse.tjmall.dto.Order;

import java.util.List;

@Component
@Mapper
public interface OrderMapper {

    @Select("select orderId, username, number, createTime, MallOrder.productId, name, originalPrice, newPrice, imageUrl, detailUrls\n" +
            "from MallOrder left join MallProduct p on MallOrder.productId = p.productId\n" +
            "where MallOrder.username = #{username};")
    List<Order> getOrderByUsername(@Param("username") String username);

    @Insert("insert into MallOrder(username, productId, number, createTime)\n" +
            "value (#{username}, #{productId}, #{number}, NOW());")
    void createNewOrder(@Param("username") String username,
                        @Param("productId") int productId,
                        @Param("number") int number);
}
