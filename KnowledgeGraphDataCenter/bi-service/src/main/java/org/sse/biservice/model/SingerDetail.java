package org.sse.biservice.model;

import lombok.Data;

import java.io.Serializable;
import java.util.List;
import java.util.Map;

@Data
public class SingerDetail implements Serializable {
    private String name;
    private String imgUrl;
    private String desc;
    private String videoUrl;
    private Map<String, String> properties;
    private List<DataEntity> recList;
}
