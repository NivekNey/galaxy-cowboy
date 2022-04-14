package net.kevinyen;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

import com.google.gson.Gson;
import com.google.gson.JsonSyntaxException;

import io.jooby.Jooby;

public class App extends Jooby {

    Gson gson = new Gson();
    Request request;
    Map<String, Double> weights = new HashMap<>();
    Double logit;
    Response response;

    {
        // load model to map
        File file = new File("/app/models/model.jsonlines");
        try (Scanner input = new Scanner(file)) {
            String line;
            Entry entry;

            while (input.hasNextLine()) {
                line = input.nextLine();
                entry = gson.fromJson(line, Entry.class);
                weights.put(entry.value, entry.weight);
            }
        } catch (JsonSyntaxException | FileNotFoundException e) {
            e.printStackTrace();
        }

        // routes

        get("/", ctx -> "ok");

        post("/predict", ctx -> {
            request = gson.fromJson(ctx.body().value(), Request.class);
            logit = 0.0;
            for (int i = 0; i < request.values.length; i++) {
                logit += weights.getOrDefault(request.values[i], 0.0);
            }

            response = new Response(1 / (1 + Math.exp(-logit)));
            return gson.toJson(response);
        });
    }

    public static void main(String[] args) {
        runApp(args, App::new);
    }
}
