from fastapi import FastAPI, HTTPException



GREETINGS: dict[str, str] = {
    "es": "¡Hola, {name}!",
    "en": "Hello, {name}!",
    "fr": "Bonjour, {name}!",
    "de": "Hallo, {name}!",
    "it": "Ciao, {name}!",
    "pt": "Olá, {name}!",
}

SUPPORTED_LANGUAGES = list(GREETINGS.keys())

app = FastAPI(
    title="Building Management API",
    description="API para administración de edificios",
    version="1.0.0"
)


building_CATALOG = {
    1: {"name": "Edificio Central", "location": "Bogotá"},
    2: {"name": "Torre Norte", "location": "Medellín"},
}

owner_DATA = {
    501: {"name": "Carlos Pérez", "unit": "A101"},
    502: {"name": "Ana Gómez", "unit": "B202"},
}

tenant_DATA = {
    101: {"name": "Luis Torres", "unit": "A101"},
    102: {"name": "Sofía Rojas", "unit": "B202"},
}


@app.get("/")
async def root():
    return {
        "name": "Building Management API",
        "version": "1.0.0",
        "domain": "building-management"
    }



@app.get("/{actor}/{name}")
async def welcome(actor: str, name: str, language: str = "es"):
    template = GREETINGS.get(language, GREETINGS["es"])

    if name.isdigit():
        id_value = int(name)

        if actor == "tenants":
            data = tenant_DATA.get(id_value)
        elif actor == "owner":
            data = owner_DATA.get(id_value)
        else:
            data = None

        if data:
            name = data["name"]

    greeting = template.format(name=name)

    message = f"{greeting} Bienvenido al sistema de administración de edificios."

    return {
        "message": message,
        "actor": actor,
        "name": name,
        "language": language
    }

@app.get("/buildingm/{buildingm_id}")
async def get_buildingm(buildingm_id: int):
    buildingm = building_CATALOG.get(buildingm_id)
    if not buildingm:
        raise HTTPException(status_code=404, detail="Edificio no encontrado")
    return {"id": buildingm_id, **buildingm}

@app.get("/owner/{owner_id}")
async def get_owner(owner_id: int):
    owner = owner_DATA.get(owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Propietario no registrado")
    return {"id": owner_id, **owner}

@app.get("/tenants/{tenant_id}")
async def get_tenant(tenant_id: int):
    tenant = tenant_DATA.get(tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Inquilino no encontrado")
    return {"id": tenant_id, **tenant}



def get_day_period(hour: int):
    if 6 <= hour < 12:
        return "Turno de mañana", "morning"
    elif 12 <= hour < 18:
        return "Turno de tarde", "afternoon"
    else:
        return "Turno de noche", "night"

@app.get("/service/schedule")
async def schedule(hour: int):
    if hour < 0 or hour > 23:
        raise HTTPException(status_code=400, detail="Hora inválida")

    message, period = get_day_period(hour)

    if period == "morning":
        services = ["maintenance", "cleaning"]
    elif period == "afternoon":
        services = ["administration", "payments"]
    else:
        services = ["security", "emergency"]

    return {
        "message": message,
        "hour": hour,
        "period": period,
        "available": services
    }



@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "domain": "building-management"
    }