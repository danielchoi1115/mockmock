package com.mockmock.databridge.domain.economicindicator.service;

import com.mockmock.databridge.domain.economicindicator.dao.EconomicIndicatorDao;
import com.mockmock.databridge.domain.economicindicator.dto.EconomicIndicator;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class EconomicIndicatorService {
    private final EconomicIndicatorDao economicDao;
    public EconomicIndicatorService(EconomicIndicatorDao economicDao){
        this.economicDao = economicDao;
    }

    public List<EconomicIndicator> getCurrentAll(){
        return economicDao.getCurrentAll();

    }
}
