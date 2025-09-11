package org.linlinjava.litemall;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import okhttp3.sse.EventSource;
import okhttp3.sse.EventSourceListener;
import okhttp3.sse.EventSources;
import org.apache.commons.lang3.time.DateUtils;
import org.joda.time.Days;

import java.util.Date;
import java.util.concurrent.TimeUnit;

public class TTT {
    private static final String EVENT_STREAM_URL = "http://127.0.0.1:8080/api/mp/unauth/ai/chat/completions";

    public static void main(String[] args) {
        Date start = new Date(2025, 11, 16);
        Date x = DateUtils.addDays(start, 60);
        System.out.println(start);
        System.out.println(x);

        // 9.8 ~ 12.15  98天
        // 12.16 ~ 2.14 60天    顺延元旦一天 , 所以是2.15 结束，2.16上班
    }
}