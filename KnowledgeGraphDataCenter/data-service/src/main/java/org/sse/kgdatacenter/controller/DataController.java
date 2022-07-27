package org.sse.kgdatacenter.controller;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.web.bind.annotation.*;
import org.sse.kgdatacenter.model.BasicQueryDto;
import org.sse.kgdatacenter.model.Singer;
import org.sse.kgdatacenter.model.SingerCompare;
import org.sse.kgdatacenter.model.SingerDetail;
import org.sse.kgdatacenter.service.BasicRepository;
import org.sse.kgdatacenter.service.RedisService;
import org.sse.kgdatacenter.service.SpiderService;

import javax.ws.rs.PathParam;
import java.util.ArrayList;
import java.util.Collections;

@Slf4j
@CrossOrigin
@RestController()
public class DataController {

    @Autowired
    SpiderService spiderService;
    @Autowired
    RedisService redisService;
    @Autowired
    BasicRepository basicRepository;
    @Autowired
    KafkaTemplate<String, Object> kafkaTemplate;

    @GetMapping("/one")
    public BasicQueryDto getOneEntityRelations(String entity, int jump, int limit) {
        BasicQueryDto cache = (BasicQueryDto) redisService.get(entity+jump+limit);
        if ( cache != null) {
            log.info("use cache");
            return cache;
        }
        BasicQueryDto result = basicRepository.queryOneEntity(entity, jump, limit);
        redisService.set(entity+jump+limit, result);
        return result;
    }

    @GetMapping("/two")
    public BasicQueryDto getTwoEntityRelations(String name1, String name2, int type, int limit) {
        BasicQueryDto cache = (BasicQueryDto) redisService.get(name1+name2+type+limit);
        if ( cache != null) {
            log.info("use cache");
            return cache;
        }
        BasicQueryDto result = basicRepository.queryTwoEntity(name1, name2, type, limit);
        redisService.set(name1+name2+type+limit, result);
        return result;
    }

    @GetMapping("/info/{name1}/{name2}")
    public SingerCompare getSingerInfo(@PathVariable String name1,
                                @PathVariable String name2) {
        name1 = name1.replace(" ", "_");
        name2 = name2.replace(" ", "_");
        SingerCompare cache = (SingerCompare) redisService.get(name1+name2);
        if (cache != null) {
            log.info("use cache");
            return cache;
        }
        SingerCompare singerCompare = new SingerCompare();
        singerCompare.setSinger1(spiderService.getSingerInfo(name1));
        singerCompare.setSinger2(spiderService.getSingerInfo(name2));
        singerCompare.getSinger1().setName(singerCompare.getSinger1().getName().replace("%20", " "));
        singerCompare.getSinger2().setName(singerCompare.getSinger2().getName().replace("%20", " "));
        log.info("singerInfo");
        ArrayList<Double> similarity = spiderService.getSimilarity(name1, name2);
        singerCompare.setRelatedness(similarity.get(0));
        singerCompare.setSimilarity(similarity.get(1));
        log.info("similar");
        redisService.set(name1+name2, singerCompare);
        return singerCompare;
    }

    @PostMapping("/insert/{type}/{name}")
    public void insertNewEntity(@PathVariable String type,
                                @PathVariable String name) {
        basicRepository.insertNewEntity(name, type);
        kafkaTemplate.send("biTopic", type+"/"+name);
    }

    @GetMapping("/info/{name}")
    public SingerDetail getSingerDetail(@PathVariable String name) {
        SingerDetail singerDetail = (SingerDetail) redisService.get("info"+name);
        if (singerDetail != null) {
            log.info("use cache");
            return singerDetail;
        }
        String searchName = name.replace(" ", "_");
        Singer singer = spiderService.getSingerInfo(searchName);
        singerDetail = new SingerDetail();
        singerDetail.setName(name);
        singerDetail.setDesc(singer.getDescription());
        singerDetail.setImgUrl(singer.getImageUrl());
        singerDetail.setVideoUrl(singer.getYoutubeUrl());
        singerDetail.setProperties(singer.getProperty());
        BasicQueryDto basicQueryDto = basicRepository.queryOneEntity(searchName, 2, 10);
        singerDetail.setRecList(new ArrayList<>(basicQueryDto.getResults().get(0).getData().get(0).getGraph().getNodes()));
        redisService.set("info"+name, singerDetail);
        return singerDetail;
    }
}
