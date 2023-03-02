package com.mockmock.databridge.global.config;

import org.springframework.cache.CacheManager;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.cache.concurrent.ConcurrentMapCacheManager;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@EnableCaching
public class CacheConfig {
    @Bean
    public CacheManager cacheManager() {
        return new ConcurrentMapCacheManager("memberCacheStore");
    }
}

    // 여러 개의 저장소를 추가할 경우
//    @Bean
//    public CacheManager cacheManager() {
//        SimpleCacheManager simpleCacheManager = new SimpleCacheManager();
//        simpleCacheManager.setCaches(
//                Arrays.asList(new ConcurrentMapCache("cacheStore1"), new ConcurrentMapCache("cacheStore2")));
//        return simpleCacheManager;
//    }
//}


