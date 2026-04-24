from fastapi import FastAPI

GREETINGS: dict[str, str] = {
    "es": "¡Hola, {name}!",
    "en": "Hello, {name}!",
    "fr": "Bonjour, {name}!",
    "de": "Hallo, {name}!",
    "it": "Ciao, {name}!",
    "pt": "Olá, {name}!",
}

SUPPORTED_LANGUAGES = list(GREETINGS.keys())

app=FastAPI(  
    title="Building Management API",
    description="API para administración de edificios",
    version= "1.0.0")



@app.get("/")
async def root():
    return {"message": "¡Hola desde FastAPI!"}

@app.get ("/{actor}/{name}")

def 