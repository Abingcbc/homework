package org.sse.webcraft.model;

import lombok.Data;

@Data
public class ShareFile {
    private int fileId;
    private String filename;
    private String fileContent;
    private int worldSize;
}
