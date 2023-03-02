package com.mockmock.databridge.domain.marketindex.api;

import com.mockmock.databridge.domain.marketindex.dto.MarketIndex;
import com.mockmock.databridge.domain.marketindex.service.MarketIndexService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.Instant;
import java.util.ArrayList;
import java.util.List;

@RestController
@RequestMapping(value = "/market", produces="application/json; charset=UTF8")
public class MarketIndexApi {

    private final MarketIndexService marketIndexService;

    public MarketIndexApi(MarketIndexService marketIndexService){
        this.marketIndexService = marketIndexService;
    }

//    @Cacheable("memberCacheStore")
    @GetMapping("/current")
    public List<MarketIndex> getCurrent(){
//        List<MarketIndex> response = this.marketIndexService.getCurrentAll();

//        dummy return value
        List<MarketIndex> res = new ArrayList<>();
        String[] indices = {"kospi", "kosdaq", "nasdaq", "sp500", "dowjones"};
        for (String ind: indices) {
            MarketIndex item = new MarketIndex();
            item.setValue(1.0);
            item.setItemCode(ind);
            item.setTime(Instant.ofEpochSecond(1676295896));
            res.add(item);
        }
        return res;
//        return response;
    }
    @GetMapping("/current/{item_code}")
    public List<MarketIndex> getCurrentByItem(@PathVariable String item_code){
        return this.marketIndexService.getCurrentItem(item_code);
    }
}
