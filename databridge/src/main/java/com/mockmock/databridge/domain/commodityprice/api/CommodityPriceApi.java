package com.mockmock.databridge.domain.commodityprice.api;

import com.mockmock.databridge.domain.commodityprice.dto.CommodityPrice;
import com.mockmock.databridge.domain.commodityprice.service.CommodityPriceService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.Instant;
import java.util.ArrayList;
import java.util.List;

@RestController
@RequestMapping(value = "/commodity", produces="application/json; charset=UTF8")
public class CommodityPriceApi {
    private final CommodityPriceService commodityPriceService;

    public CommodityPriceApi(CommodityPriceService commodityPriceService) {
        this.commodityPriceService = commodityPriceService;
    }

    //    @Cacheable("memberCacheStore")
    @GetMapping("/current")
    public List<CommodityPrice> getCurrent() {
//        List<CommodityPrice> response = this.commodityPriceService.getCurrentAll();
        List<CommodityPrice> res = new ArrayList<>();
//        dummy return value
        String[] indices = {"crud_oil", "gold", "steel"};
        for (String ind : indices) {
            CommodityPrice item = new CommodityPrice();
            item.setValue(1.0);
            item.setItemCode(ind);
            item.setTime(Instant.ofEpochSecond(1676295896));

            res.add(item);
        }
        return res;
//        return response;
    }
}
