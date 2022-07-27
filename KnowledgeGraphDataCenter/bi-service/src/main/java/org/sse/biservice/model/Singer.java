package org.sse.biservice.model;

import lombok.Data;

import java.io.Serializable;
import java.util.Map;

@Data
public class Singer implements Serializable {
    private String name;
    private String description;
    private String youtubeUrl;
    private String imageUrl;
    private Map<String, String> property;
}
