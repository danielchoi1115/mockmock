package com.mockmock.databridge.domain.marketindex.service;

import com.mockmock.databridge.domain.marketindex.repository.MarketIndexDao;
import com.mockmock.databridge.domain.marketindex.dto.MarketIndex;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class MarketIndexService {
    private final MarketIndexDao marketDao;
    public MarketIndexService(MarketIndexDao marketDao){
        this.marketDao = marketDao;
    }

    public List<MarketIndex> getCurrentAll(){
        return marketDao.getCurrentAll();

    }
    public List<MarketIndex> getCurrentItem(String code){
        return marketDao.getCurrentItem(code);

    }


}
