package com.mockmock.databridge.domain.marketindex.dto;

import com.influxdb.annotations.Column;
import com.influxdb.annotations.Measurement;
import com.mockmock.databridge.global.entity.Point;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@Measurement(name = "stock")
public class MarketIndex extends Point {
    @Column(name = "item_code")
    public String itemCode;

    @Column()
    public Double value;

}
