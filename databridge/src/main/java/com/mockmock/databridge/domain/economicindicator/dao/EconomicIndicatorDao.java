package com.mockmock.databridge.domain.economicindicator.dao;

import com.influxdb.client.InfluxDBClient;
import com.influxdb.client.QueryApi;
import com.mockmock.databridge.domain.economicindicator.dto.EconomicIndicator;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public class EconomicIndicatorDao {
    private final QueryApi queryApi;
    public EconomicIndicatorDao(InfluxDBClient influxDBClient){
        this.queryApi = influxDBClient.getQueryApi();
    }


    public List<EconomicIndicator> getCurrentAll() {
        return queryApi.query(EconomicIndicatorQuery.CurrentAll(), EconomicIndicator.class);
    }
}
