package com.mockmock.databridge.domain.commodityprice.service;

import com.mockmock.databridge.domain.commodityprice.dao.CommodityPriceDao;
import com.mockmock.databridge.domain.commodityprice.dto.CommodityPrice;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class CommodityPriceService {
    private final CommodityPriceDao commodityDao;
    public CommodityPriceService(CommodityPriceDao commodityDao){
        this.commodityDao = commodityDao;
    }

    public List<CommodityPrice> getCurrentAll(){
        return commodityDao.getCurrentAll();

    }
}
