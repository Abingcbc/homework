package org.sse.webcraft.mapper;

import org.apache.ibatis.annotations.*;
import org.springframework.stereotype.Component;
import org.sse.webcraft.model.GameFile;
import org.sse.webcraft.model.ShareFile;

import java.util.List;

@Component
@Mapper
public interface GameFileMapper {

    @Insert("insert into GameFile(username, filename, createTime, updateTime, fileContent, worldSize)\n" +
            "value (#{username}, #{filename}, NOW(), NOW(), #{fileContent}, #{worldSize});")
    @Options(useGeneratedKeys = true, keyProperty = "fileId", keyColumn = "fileId")
    int createNewGameFile(GameFile gameFile);

    @Insert("insert into ShareFile(filename, fileContent, worldSize)\n" +
            "value (#{filename}, #{fileContent}, #{worldSize});")
    @Options(useGeneratedKeys = true, keyProperty = "fileId", keyColumn = "fileId")
    int createShareFile(ShareFile shareFile);

    @Select("select * from ShareFile\n" +
            "where fileId = #{fileId};")
    ShareFile getShareFileByFileId(@Param("fileId") int fileId);

    @Select("select * from GameFile\n" +
            "where fileId = #{fileId};")
    GameFile getGameFileByFileId(@Param("fileId") int fileId);

    @Select("select fileId, username, filename, createTime, updateTime, worldSize from GameFile\n" +
            "where username = #{username};")
    List<GameFile> getGameFileListWithoutContent(@Param("username") String username);

    @Update("update GameFile\n" +
            "set fileContent = #{fileContent} , updateTime = NOW()\n" +
            "where fileId = #{fileId};")
    int updateGameFileContent(@Param("fileContent") String fileContent,
                              @Param("fileId") int fileId);

    @Delete("delete from GameFile\n" +
            "where fileId = #{fileId};")
    int deleteGameFile(@Param("fileId") int fileId);
}
