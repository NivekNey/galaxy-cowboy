use actix_web::{get, post, web, App, HttpResponse, HttpServer, Responder};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::Mutex;
use std::{
    fs::File,
    io::{self, BufRead},
    path::Path,
};

// IO structs

#[derive(Deserialize, Debug)]
struct Entry {
    value: String,
    weight: f64,
}

#[derive(Deserialize)]
struct Request {
    values: Vec<String>,
}

#[derive(Serialize)]
struct Respond {
    probability: f64,
}

// routes

#[get("/")]
async fn health() -> HttpResponse {
    HttpResponse::Ok().body("ok")
}

#[post("/predict")]
async fn predict(
    request: web::Json<Request>,
    data: web::Data<Mutex<HashMap<String, f64>>>,
) -> impl Responder {
    let wrapped_data = data.lock().unwrap();
    let mut logit: f64 = 0.0;
    for value in request.values.iter() {
        logit += wrapped_data.get(value).cloned().unwrap_or(0.0);
    }
    let probability = 1.0 / (1.0 + f64::exp(-logit));
    let response = Respond {
        probability: probability,
    };
    web::Json(response)
}

// main

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    // model
    let mut weights: HashMap<String, f64> = HashMap::new();
    if let Ok(lines) = read_lines("/app/models/model.jsonlines") {
        // Consumes the iterator, returns an (Optional) String
        for line in lines {
            if let Ok(entry_str) = line {
                let entry: Entry = serde_json::from_str(&entry_str).unwrap();
                weights.insert(entry.value, entry.weight);
            }
        }
    }
    let data = web::Data::new(Mutex::new(weights));
    println!("model loaded");
    // server
    HttpServer::new(move || {
        App::new()
            .app_data(web::Data::clone(&data))
            .service(health)
            .service(predict)
    })
    .bind(("0.0.0.0", 9001))?
    .run()
    .await
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
