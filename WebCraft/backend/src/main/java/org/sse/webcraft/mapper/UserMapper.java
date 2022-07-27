package org.sse.webcraft.mapper;

import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.springframework.stereotype.Component;
import org.sse.webcraft.model.UserAuthInfo;

/**
 * @author cbc
 */
@Component
@Mapper
public interface UserMapper {

    @Select("select username, password from GameUser where username = #{username}")
    UserAuthInfo getUserAuthInfoByUsername(@Param("username") String username);

    @Insert("insert into GameUser\n" +
            "value (#{username}, #{password});")
    int createNewUser(@Param("username") String username,
                       @Param("password") String password);

}
