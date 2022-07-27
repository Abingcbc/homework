package org.sse.biservice.model;

import lombok.Data;

import java.io.Serializable;
import java.util.List;
import java.util.Map;

@Data
public class DataEntity implements Serializable {
    private String id;
    private List<String> labels;
    private Map<String, String> properties;
}
