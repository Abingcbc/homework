package org.sse.biservice.service;

import com.alibaba.fastjson.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.sse.biservice.model.SingerCompare;
import org.sse.biservice.model.SingerDetail;

@Service
public class RestService {
    @Autowired
    RestTemplateBuilder builder;

    public SingerDetail requestSingerDetail(String name) {
        RestTemplate restTemplate = builder.build();
        String url = "http://localhost:9100/data-service/info/"+name;
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<String> entity = new HttpEntity<>(headers);
        String response = restTemplate.exchange(url, HttpMethod.GET, entity, String.class).getBody();
        return JSONObject.parseObject(response, SingerDetail.class);
    }

    public SingerCompare requestSingerCompare(String name1, String name2) {
        RestTemplate restTemplate = builder.build();
        String url = "http://localhost:9100/data-service/info/"+name1+"/"+name2;
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<String> entity = new HttpEntity<>(headers);
        String response = restTemplate.exchange(url, HttpMethod.GET, entity, String.class).getBody();
        return JSONObject.parseObject(response, SingerCompare.class);
    }
}
