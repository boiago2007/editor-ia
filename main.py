from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from PIL import Image
import io

app = FastAPI()

# Permitir requisições do frontend (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "API funcionando! Use /enhance/ para enviar a imagem."}

@app.post("/enhance/")
async def enhance_image(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))

    # Simples simulação de melhoria (aumenta a nitidez com um filtro)
    enhanced_image = image.resize((image.width * 2, image.height * 2), Image.LANCZOS)

    # Salvar a imagem em memória
    img_byte_arr = io.BytesIO()
    enhanced_image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    return StreamingResponse(img_byte_arr, media_type="image/png")
