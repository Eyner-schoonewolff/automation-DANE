# API para la Creación de Reportes del DANE  

## Descripción  

Esta API automatiza la descarga, procesamiento y análisis de un archivo desde la página del **DANE**, generando un reporte con los **10 productos más vendidos** y enviándolo por correo electrónico.  

## Características  

- **Automatización**: Descarga y procesa automáticamente el archivo de datos del DANE.  
- **Procesamiento de datos**: Extrae información clave como nombre del producto, marca y precio.  
- **Generación de reportes**: Crea un archivo CSV con los 10 productos más vendidos.  
- **Análisis y resumen**: Calcula el total de productos vendidos y el porcentaje de los más vendidos.  
- **Notificación**: Envía un correo electrónico con el resumen y el reporte adjunto.  
- **Estructura modular**: Implementado con buenas prácticas de programación y arquitectura **DDD (Domain-Driven Design)**.  

---

## Instalación  

### Requisitos  

- **Python 3.11**  
- Instalar dependencias ejecutando:  

```bash
pip install -r requirements.txt
```

---

## Arquitectura (DDD)  

```
.api
├── app/
|    ├── Register_visit_order/     
|    │   ├── adapters/            
|    │   │   ├── calculate_file.py    
|    │   │   ├── email.py              
|    │   │   ├── localization_web_process.py              
|    │   │   ├── process_file.py             
|    │   │              
|    │   ├── entrypoints/         
|    │   │   ├── routers.py       
|    │   │   ├── dependencies.py
|    │   │
|    │   ├── services/            
|    │   │   ├── handler.py       
|    │   |
|    │   ├── templates/           
|    │   │   ├── body.html     
|    |
|    ├── dowloands/  **los archivos se guardaran aqui**
|    │     
|                        
├── requirements.txt               
├── .env                          
├── .env.example                   
├── main.py                        
└── README.md                      
```

---

## Stack Tecnológico  

- **Python**  
- **FastAPI** (Framework para la API)  
- **Selenium** (Automatización web para la descarga de datos)  
- **OpenPyXL** (Procesamiento de archivos Excel)  

---

## Endpoints  

### 📌 **[POST] /automation**  
- **Descripción**: Realiza el proceso de generación de documentos y envía el reporte por correo.  
- **Ejemplo de uso**:  

```bash
curl -X 'POST' 'http://localhost:8000/automation' \
     -H 'Content-Type: application/json' \
     -d '{"email": "usuario@example.com"}'
```

---

## Flujo de Ejecución  

1. **Descargar el archivo** desde el portal del **DANE**.  
2. **Procesar los datos** y extraer información clave:  
   - Nombre del producto  
   - Marca  
   - Precio  
3. **Generar un nuevo archivo CSV** con los 10 productos más vendidos.  
4. **Calcular estadísticas**:  
   - Total de productos vendidos  
   - Total de los 10 más vendidos  
   - Porcentaje que representan los 10 productos más vendidos sobre el total  
5. **Enviar un correo electrónico** con el resumen y el archivo adjunto.  

---

## Configuración y Ejecución  

### Activar el entorno virtual  

```bash
py -m venv venv
.\venv\Scripts\activate
```

### Instalar dependencias  

```bash
pip install -r requirements.txt
```

### Iniciar el servidor  

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload --log-level debug
```

### Acceder a la documentación interactiva  

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)  

---


---

## Criterios de Evaluación  

✅ **Funcionamiento completo**: El flujo debe ejecutarse correctamente.  
✅ **Calidad del código**: Implementación con buenas prácticas y uso correcto de OOP.  
✅ **Estructura del proyecto**: Código organizado y documentado.  
✅ **Automatización**: Desde la descarga hasta el envío del correo.  
✅ **Pruebas unitarias**: Cobertura adecuada de las funcionalidades clave.  

---

# 📌 Notas Finales  
# Muchas Gracias.  
# Att: Eyner Alfonso Schoonewolff. 🚀

