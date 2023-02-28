package com.mockmock.databridge.domain.economicindicator.api;

import com.mockmock.databridge.domain.economicindicator.dto.EconomicIndicator;
import com.mockmock.databridge.domain.economicindicator.service.EconomicIndicatorService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.Instant;
import java.util.ArrayList;
import java.util.List;

@RestController
@RequestMapping(value = "/economy", produces="application/json; charset=UTF8")
public class EconomicIndicatorApi {

    private final EconomicIndicatorService economicIndicatorService;

    public EconomicIndicatorApi(EconomicIndicatorService economicIndicatorService) {
        this.economicIndicatorService = economicIndicatorService;
    }

    //    @Cacheable("memberCacheStore")
    @GetMapping("/current")
    public List<EconomicIndicator> getCurrent() {
//        List<EconomicIndicator> response = this.economicIndicatorService.getCurrentAll();
        //        dummy return value
        List<EconomicIndicator> res = new ArrayList<>();
        String[] indices = {"usd_krw", "interest", "unemployment"};
        for (String ind : indices) {
            EconomicIndicator item = new EconomicIndicator();
            item.setValue(1.0);
            item.setItemCode(ind);
            item.setTime(Instant.ofEpochSecond(1676295896));

            res.add(item);
        }
        return res;
//        return response;
    }
}