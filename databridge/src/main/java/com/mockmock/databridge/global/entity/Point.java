package com.mockmock.databridge.global.entity;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.influxdb.annotations.Column;
import lombok.Getter;
import lombok.Setter;

import java.time.Instant;

@Getter
@Setter
public class Point {
    @Column(timestamp = true)
    @JsonProperty
    public Instant time;
}
