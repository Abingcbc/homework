package org.sse.kgdatacenter.model;

import lombok.Data;

import java.io.Serializable;
import java.util.Map;

@Data
public class Relation implements Serializable {

    private String id;
    private String type;
    private String startNode;
    private String endNode;
    private Map<String, String> properties;
}
