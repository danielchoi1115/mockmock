package com.mockmock.databridge.domain.commodityprice.dao;

import com.influxdb.client.InfluxDBClient;
import com.influxdb.client.QueryApi;
import com.mockmock.databridge.domain.commodityprice.dto.CommodityPrice;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public class CommodityPriceDao {

    private final QueryApi queryApi;
    public CommodityPriceDao(InfluxDBClient influxDBClient){
        this.queryApi = influxDBClient.getQueryApi();
    }


    public List<CommodityPrice> getCurrentAll() {
        return queryApi.query(CommodityPriceQuery.CurrentAll(), CommodityPrice.class);
    }
}
