package com.mockmock.databridge.domain.economicindicator.dao;

import com.influxdb.query.dsl.Flux;
import com.influxdb.query.dsl.functions.restriction.Restrictions;
import org.springframework.stereotype.Repository;

import java.time.temporal.ChronoUnit;

@Repository
public class EconomicIndicatorQuery {
    private static final String bucket = "stocks";
    public static String CurrentAll(){
        String tag = "symbol";
        String measurement = "stock";
        Restrictions restriction = Restrictions.and(
                Restrictions.measurement().equal(measurement),
                Restrictions.or(
                        Restrictions.tag(tag).equal("005930")
                )
        );

        return Flux.from(bucket)
                .range(-2L, -1L, ChronoUnit.YEARS)
                .filter(restriction)
                .last()
                .toString();
    }
}
