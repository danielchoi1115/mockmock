package com.mockmock.databridge.global.config;

import com.influxdb.client.InfluxDBClient;
import com.influxdb.client.InfluxDBClientFactory;
import com.influxdb.client.InfluxDBClientOptions;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;


@Configuration
public class InfluxDBConfig {

    @Value("${spring.influx.url}")
    private String influxURL;
    @Value("${spring.influx.token}")
    private String influxToken;
    @Value("${spring.influx.org}")
    private String influxOrg;

    @Bean
    public InfluxDBClient influxDBClient(){
        InfluxDBClientOptions options = InfluxDBClientOptions.builder()
                .url(this.influxURL)
                .authenticateToken(this.influxToken.toCharArray())
                .org(this.influxOrg)
                .bucket(null)
                .build();

        return InfluxDBClientFactory.create(options);
    }
}

