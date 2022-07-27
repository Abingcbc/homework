package org.sse.tjmall.mapper;

import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.springframework.stereotype.Component;
import org.sse.tjmall.dto.User;

@Component
@Mapper
public interface UserMapper {

    @Select("select * from MallUser where username = #{username}")
    User getUserByUsername(@Param("username") String username);

    @Insert("insert into MallUser(username, password)" +
            " values(#{username}, #{password});")
    int createNewUser(@Param("username") String username,
                      @Param("password") String password);
}
