package org.sse.kgdatacenter.model;

import lombok.Data;

import java.util.List;
import java.util.Map;

@Data
public class SingerDetail {
    private String name;
    private String imgUrl;
    private String desc;
    private String videoUrl;
    private Map<String, String> properties;
    private List<Entity> recList;
}
