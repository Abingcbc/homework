package org.sse.kgdatacenter.model;

import lombok.Data;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;

@Data
public class BasicQueryDto implements Serializable {

    private ArrayList<BasicQueryObject> results;

    @Data
    public static class BasicQueryObject implements Serializable {
        private ArrayList<String> columns;
        private ArrayList<BasicQueryGraph> data;
    }

    @Data
    public static class BasicQueryGraph implements Serializable {
        private BasicQueryPath graph;
    }

    @Data
    public static class BasicQueryPath implements Serializable {
        private Set<Entity> nodes;
        private Set<Relation> relationships;
    }
}

