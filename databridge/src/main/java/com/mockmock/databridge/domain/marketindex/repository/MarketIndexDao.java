package com.mockmock.databridge.domain.marketindex.repository;


import com.mockmock.databridge.domain.marketindex.dto.MarketIndex;
import com.influxdb.client.InfluxDBClient;
import com.influxdb.client.QueryApi;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public class MarketIndexDao {
    private final QueryApi queryApi;
    public MarketIndexDao(InfluxDBClient influxDBClient){
        this.queryApi = influxDBClient.getQueryApi();
    }


    public  List<MarketIndex> getCurrentAll() {
        return queryApi.query(MarketIndexQuery.CurrentAll(), MarketIndex.class);
    }
    public  List<MarketIndex> getCurrentItem(String code) {
        return queryApi.query(MarketIndexQuery.CurrentItem(code), MarketIndex.class);
    }
}
