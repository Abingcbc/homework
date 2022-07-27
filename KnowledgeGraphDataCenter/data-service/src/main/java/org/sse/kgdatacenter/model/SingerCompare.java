package org.sse.kgdatacenter.model;

import lombok.Data;

import java.io.Serializable;

@Data
public class SingerCompare implements Serializable {
    private Singer singer1;
    private Singer singer2;
    private double relatedness;
    private double similarity;
}
