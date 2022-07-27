package org.sse.biservice.controller;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.sse.biservice.model.Entity;
import org.sse.biservice.model.SingerCompare;
import org.sse.biservice.model.SingerDetail;
import org.sse.biservice.service.ESservice;
import org.sse.biservice.service.RedisService;
import org.sse.biservice.service.RestService;

import java.util.List;

@Slf4j
@CrossOrigin
@RestController
public class SearchController {

    @Autowired
    ESservice eSservice;
    @Autowired
    RestService restService;
    @Autowired
    RedisService redisService;

    @PostMapping("/search/searchResult/{keyword}")
    public List<Entity> searchEntity(@PathVariable String keyword) {
        return eSservice.searchSinger(keyword);
    }

    @PostMapping("/search/singerDetail/{name}")
    public SingerDetail getSingerDetail(@PathVariable String name) {
        SingerDetail singerDetail = (SingerDetail) redisService.get("singerDetail-"+name);
        if (singerDetail != null) {
            log.info("use cache");
            return singerDetail;
        }
        singerDetail = restService.requestSingerDetail(name);
        redisService.set("singerDetail-"+name, singerDetail);
        return singerDetail;
    }

    @GetMapping("/search/singerCompare/{name1}/{name2}")
    public SingerCompare getSingerCompare(@PathVariable String name1,
                                          @PathVariable String name2) {
        SingerCompare singerCompare = (SingerCompare) redisService.get("singerCompare-"+name1+name2);
        if (singerCompare != null) {
            log.info("use cache");
            return singerCompare;
        }
        singerCompare = restService.requestSingerCompare(name1, name2);
        redisService.set("singerDetail-"+name1+name2, singerCompare);
        return singerCompare;
    }
}
