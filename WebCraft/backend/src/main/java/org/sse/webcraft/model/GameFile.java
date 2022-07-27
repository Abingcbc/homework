package org.sse.webcraft.model;

import lombok.Data;

@Data
public class GameFile {
    private int fileId;
    private String username;
    private String filename;
    private String createTime;
    private String updateTime;
    private String fileContent;
    private int worldSize;
}
