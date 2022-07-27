package org.sse.biservice.model;

import lombok.Data;

import java.io.Serializable;

@Data
public class Entity implements Serializable {
    private String name;
    private String url;
    private String type;
}
