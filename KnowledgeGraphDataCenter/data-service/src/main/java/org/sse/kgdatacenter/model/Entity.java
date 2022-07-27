package org.sse.kgdatacenter.model;

import lombok.Data;
import org.neo4j.ogm.annotation.Id;
import org.neo4j.ogm.annotation.NodeEntity;

import java.io.Serializable;
import java.util.List;
import java.util.Map;

@Data
public class Entity implements Serializable {
    private String id;
    private List<String> labels;
    private Map<String, String> properties;
}
