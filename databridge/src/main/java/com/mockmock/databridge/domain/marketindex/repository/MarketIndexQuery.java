package com.mockmock.databridge.domain.marketindex.repository;
import com.influxdb.query.dsl.Flux;
import com.influxdb.query.dsl.functions.restriction.Restrictions;
import org.springframework.stereotype.Repository;

import java.time.temporal.ChronoUnit;

@Repository
public class MarketIndexQuery {


    private static final String bucket = "econ_indicator";


    public static String CurrentAll(){
        String tag = "item_code";
        String measurement = "econ";
        Restrictions restriction = Restrictions.and(
                Restrictions.measurement().equal(measurement),
                Restrictions.or(
                        Restrictions.tag(tag).equal("A001"),
                        Restrictions.tag(tag).equal("010103000")
                )
        );

        return Flux.from(bucket)
                .range(-2L, -1L, ChronoUnit.YEARS)
                .filter(restriction)
                .last()
                .toString();
    }
    public static String CurrentItem(String code){
        String tag = "item_code";
        String measurement = "econ";
        Restrictions restriction = Restrictions.and(
                Restrictions.measurement().equal(measurement),
                Restrictions.tag(tag).equal(code)
        );

        return Flux.from(bucket)
                .range(-2L, -1L, ChronoUnit.YEARS)
                .filter(restriction)
                .last()
                .toString();
    }

}
