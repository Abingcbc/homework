package org.sse.kgdatacenter.service;

import com.alibaba.fastjson.JSONObject;
import lombok.extern.java.Log;
import org.apache.http.HttpHost;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.config.RequestConfig;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;
import org.springframework.stereotype.Service;
import org.sse.kgdatacenter.model.ApiSinger;
import org.sse.kgdatacenter.model.Singer;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Log
@Service
public class SpiderService {
    public Singer getSingerInfo(String name) {
        Singer result = new Singer();
        result.setName(name.replace("_", "%20"));

        name = name.replace("_", "+");
        HttpClient client = HttpClients.createDefault();
        HttpHost proxy = new HttpHost("localhost", 1080);

        HttpGet get = new HttpGet("https://tastedive.com/api/similar?q=" + name + "&info=1&limit=3&k=375841-bi-HXS8BJI3&type=music");
        HttpResponse response = null;
        try {
            response = client.execute(get);
            String responseContent = EntityUtils.toString(response.getEntity());
            JSONObject apiSinger = JSONObject.parseObject(responseContent)
                    .getJSONObject("Similar").getJSONArray("Info").getJSONObject(0);
            result.setYoutubeUrl(apiSinger.getString("yUrl"));
            result.setDescription(apiSinger.getString("wTeaser"));
            name = name.replace("+", "%20");
        } catch (Exception e) {
            e.printStackTrace();
        }
        try {
            HttpGet getImage = new HttpGet("https://en.wikipedia.org/w/api.php?action=query&titles=" + name + "&prop=pageimages&format=json");
            getImage.setConfig(RequestConfig.custom()
                    .setProxy(proxy).build());
            response = client.execute(getImage);
            String responseContent = EntityUtils.toString(response.getEntity());
            String mode = "(http[s]?:\\/\\/([\\w-]+\\.)+[\\w-]+([\\w-./?%&*=]*))";
            Pattern p = Pattern.compile(mode);
            Matcher m = p.matcher(responseContent);
            if (m.find()) {
                String url = m.group();
                result.setImageUrl(url);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        try {
            HttpGet getProperty = new HttpGet("http://vmdbpedia.informatik.uni-leipzig.de:8080/api/1.0.0/values?entities="+
                    name.replace("%20", "_")+
                    "&property=dbo%3AbirthPlace&property=dbo%3AbirthDate&property=dbo%3Agenre&property=dbo%3Aoccupation" +
                    "&property=dbo%3ArecordLabel&property=dbo%3Abackground&property=dbo%3AactiveYearsStartYear" +
                    "&pretty=NONE&limit=100&offset=0&key=1234&oldVersion=false");
            getProperty.setHeader("Accept", "application/json");
            response = client.execute(getProperty);
            String responseContent = EntityUtils.toString(response.getEntity());
            JSONObject object = (JSONObject) JSONObject.parseObject(responseContent).getJSONObject("results")
                    .getJSONArray("bindings").get(0);
            result.setProperty(new HashMap<>());
            if (object.containsKey("dbobirthPlace")) {
                result.getProperty().put("birthPlace", object.getJSONObject("dbobirthPlace").getString("value"));
            }
            if (object.containsKey("dbobirthDate")) {
                result.getProperty().put("birthDate", object.getJSONObject("dbobirthDate").getString("value"));
            }
            if (object.containsKey("dbogenre")) {
                result.getProperty().put("genre", object.getJSONObject("dbogenre").getString("value"));
            }
            if (object.containsKey("dbooccupation")) {
                result.getProperty().put("occupation", object.getJSONObject("dbooccupation").getString("value"));
            }
            if (object.containsKey("dborecordLabel")) {
                result.getProperty().put("recordLabel", object.getJSONObject("dborecordLabel").getString("value"));
            }
            if (object.containsKey("dbobackground")) {
                result.getProperty().put("background", object.getJSONObject("dbobackground").getString("value"));
            }
            if (object.containsKey("dboactiveYearsStartYear")) {
                result.getProperty().put("activeYearsStartYear", object.getJSONObject("dboactiveYearsStartYear").getString("value"));
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return result;
    }

    public ArrayList<Double> getSimilarity(String name1, String name2) {
        ArrayList<Double> result = new ArrayList<>();
        result.add(0.);
        result.add(0.);
        String artist1 = "http://dbpedia.org/resource/"+name1;
        String artist2 = "http://dbpedia.org/resource/"+name2;
        HttpClient client = HttpClients.createDefault();
        HttpHost proxy = new HttpHost("localhost", 1080);
        HttpGet get = new HttpGet("http://sematch.cluster.gsi.dit.upm.es/api/entity_sim?e1=" + artist1 + "&e2=" + artist2);
        try {
            get.setConfig(RequestConfig.custom()
                    .setProxy(proxy).build());
            HttpResponse response = client.execute(get);
            String responseContent = EntityUtils.toString(response.getEntity());
            log.info(responseContent);
            result.set(0, JSONObject.parseArray(responseContent).getJSONObject(0).getDouble("sim"));
            result.set(1, JSONObject.parseArray(responseContent).getJSONObject(1).getDouble("sim"));
        } catch (IOException e) {
            e.printStackTrace();
        }
        return result;
    }
}
