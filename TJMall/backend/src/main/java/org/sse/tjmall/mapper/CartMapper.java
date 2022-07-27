package org.sse.tjmall.mapper;

import org.apache.ibatis.annotations.*;
import org.springframework.stereotype.Component;
import org.sse.tjmall.dto.CartItem;

import java.util.List;

@Component
@Mapper
public interface CartMapper {

    @Insert("insert into MallCart(username, productId, number)\n" +
            "value (#{username}, #{productId}, 1);")
    void addNewItemToCart(@Param("username") String username,
                          @Param("productId") int productId);

    @Select("select * from MallCart\n" +
            "where MallCart.username = #{username} and MallCart.productId = #{productId};")
    CartItem isItemAdded(@Param("username") String username,
                         @Param("productId") int productId);

    @Update("update MallCart\n" +
            "set MallCart.number = MallCart.number + 1\n" +
            "where MallCart.username = #{username} and MallCart.productId = #{productId};")
    void addExistItemToCart(@Param("username") String username,
                            @Param("productId") int productId);

    @Update("update MallCart\n" +
            "set MallCart.number = MallCart.number - 1\n" +
            "where cart.username = #{username} and MallCart.productId = #{productId};")
    void removeExistItemOne(@Param("username") String username,
                            @Param("productId") int productId);

    @Delete("delete from MallCart\n" +
            "where username = #{username} and productId = #{productId};")
    void removeExistItemAll(@Param("username") String username,
                            @Param("productId") int productId);

    @Select("select username, number, MallCart.productId, name, originalPrice, newPrice, imageUrl, detailUrls\n" +
            "from MallCart left join MallProduct p on MallCart.productId = p.productId\n" +
            "where username = #{username};")
    List<CartItem> getAllByUsername(@Param("username") String username);
}
